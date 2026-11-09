"""
code.py  -  runs on the Raspberry Pi Pico 2 W (CircuitPython 9).

Copy to the CIRCUITPY drive together with turnlogic.py.
Needs in CIRCUITPY/lib:  adafruit_lsm6ds, adafruit_register, adafruit_bus_device, neopixel.mpy

Wiring
    LSM6DS3TR-C  ->  Grove I2C0 port   (SDA = GP8, SCL = GP9)
    NeoPixel DIN ->  GP16              (power from 3V3 and GND)
    PAM8302 A+   ->  GP18              (A- to GND, Vin to 3V3)
    Button       ->  GP20 and GND

What the ring shows
    Green, emptying like a clock   time left until the next turn is due (16 lights = full interval)
    Amber, slow pulse + 3 beeps    turn due within 15 minutes
    Red, flashing + 10 beeps       interval expired with no effective turn
    Red, steady                    acknowledged, still waiting for an effective turn
    Cyan, one light circling       check the patch (detached, motionless or sensor fault)
    White flash                    button press registered
    Two green flashes              effective turn recorded

The button silences whatever sound is playing, straight away.
"""
import json
import math
import time

import board
import busio
import digitalio
import neopixel
import pwmio
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC

from turnlogic import Config, Monitor, Stillness, angles

cfg = Config()
cfg.TIME_SCALE = 1.0        # set to 60.0 for a demo: 2 hours pass in 2 minutes

SAMPLE_HZ = 20
ALPHA = 0.15                # low-pass filter weight for each new sample
VOLUME = 6000               # PWM duty, 0 to 65535 (about 9%). Also use the trim pot on the amp
N_PIX = 16
BRIGHTNESS = 0.15

OFF = (0, 0, 0)
GREEN = (0, 255, 0)
AMBER = (255, 140, 0)
RED = (255, 0, 0)
CYAN = (0, 170, 255)
WHITE = (255, 255, 255)

# (frequency Hz, on seconds, off seconds) and how often the pattern repeats
PATTERNS = {
    "advisory": ([(880, 0.20, 0.20)] * 3, 30.0),
    "critical": ([(1200, 0.15, 0.10)] * 10, 5.0),
    "technical": ([(600, 0.08, 0.0), (900, 0.08, 0.0)], 20.0),
}

# ------------------------------------------------------------------ hardware
pixels = neopixel.NeoPixel(board.GP16, N_PIX, brightness=BRIGHTNESS, auto_write=False)
speaker = pwmio.PWMOut(board.GP18, frequency=440, duty_cycle=0, variable_frequency=True)
button = digitalio.DigitalInOut(board.GP20)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

i2c = busio.I2C(scl=board.GP9, sda=board.GP8)
sensor = None


def connect_sensor():
    global sensor
    try:
        sensor = LSM6DS3TRC(i2c)
    except Exception:
        sensor = None


class Beeper:
    """Plays tone patterns without blocking the main loop."""

    def __init__(self):
        self.steps = []
        self.i = 0
        self.t_next = 0.0
        self.sounding = False
        self.repeat = 0.0
        self.t_repeat = 0.0
        self.name = None

    def set(self, name, now):
        if name == self.name:
            return
        self.name = name
        speaker.duty_cycle = 0          # any change stops the current tone at once
        self.sounding = False
        if name in PATTERNS:
            self.steps, self.repeat = PATTERNS[name]
            self.i = 0
            self.t_next = now
            self.t_repeat = now + self.repeat
        else:
            self.steps = []

    def tick(self, now):
        if not self.steps:
            return
        if self.i >= len(self.steps):
            if now >= self.t_repeat:
                self.i = 0
                self.t_next = now
                self.t_repeat = now + self.repeat
            return
        if now < self.t_next:
            return
        freq, on_s, off_s = self.steps[self.i]
        if not self.sounding:
            speaker.frequency = freq
            speaker.duty_cycle = VOLUME
            self.sounding = True
            self.t_next = now + on_s
        else:
            speaker.duty_cycle = 0
            self.sounding = False
            self.t_next = now + off_s
            self.i += 1


def dim(colour, k):
    return (int(colour[0] * k), int(colour[1] * k), int(colour[2] * k))


def render(now, state, acked, frac_left, flash_until, confirm_until):
    """Draw one frame of the ring. Called every loop, so patterns animate."""
    if now < flash_until:
        pixels.fill(WHITE)
    elif now < confirm_until:
        on = int((confirm_until - now) / 0.25) % 2 == 1
        pixels.fill(GREEN if on else OFF)
    elif state == "normal":
        lit = max(1, math.ceil(N_PIX * frac_left))
        for i in range(N_PIX):
            pixels[i] = GREEN if i < lit else OFF
    elif state == "advisory":
        k = 0.2 + 0.8 * (0.5 + 0.5 * math.sin(now * math.pi))     # one breath every 2 s
        pixels.fill(dim(AMBER, k))
    elif state == "critical":
        if acked:
            pixels.fill(RED)
        else:
            pixels.fill(RED if int(now * 4) % 2 == 0 else OFF)     # flashing twice a second
    else:
        head = int(now * N_PIX) % N_PIX                             # one turn per second
        for i in range(N_PIX):
            d = (head - i) % N_PIX
            pixels[i] = dim(CYAN, 1.0 if d == 0 else 0.35 if d == 1 else 0.1 if d == 2 else 0.0)
    pixels.show()


# ---------------------------------------------------------------------- main
connect_sensor()
monitor = Monitor(cfg)
still = Stillness(cfg)
beeper = Beeper()

fx = fy = fz = None
sum_x = sum_y = sum_z = 0.0
n_sum = 0
events_out = []
last_state = None
last_button = False
last_press_t = -10.0
silenced = None             # the alarm state whose sound the nurse has silenced
flash_until = 0.0
confirm_until = 0.0
send_now = False
period = 1.0 / SAMPLE_HZ
t_prev = time.monotonic()
t_report = t_prev
t_still = t_prev
t_retry = t_prev
roll = pitch = 0.0
still_value = None

while True:
    now = time.monotonic()
    dt = now - t_prev
    t_prev = now

    # ---- read the sensor
    ok = False
    if sensor is None:
        if now - t_retry > 2.0:
            t_retry = now
            connect_sensor()
    else:
        try:
            ax, ay, az = sensor.acceleration
            ok = True
        except Exception:
            sensor = None

    if ok:
        if fx is None:
            fx, fy, fz = ax, ay, az
        fx += ALPHA * (ax - fx)
        fy += ALPHA * (ay - fy)
        fz += ALPHA * (az - fz)
        roll, pitch = angles(fx, fy, fz, cfg.ROLL_SIGN)
        sum_x += ax
        sum_y += ay
        sum_z += az
        n_sum += 1
        g = (fx * fx + fy * fy + fz * fz) ** 0.5
        if g < cfg.G_MIN or g > cfg.G_MAX:
            ok = False      # implausible gravity counts as a sensor fault

    # ---- stillness check, once per second
    if now - t_still >= 1.0:
        t_still = now
        if n_sum:
            still.add(sum_x / n_sum, sum_y / n_sum, sum_z / n_sum)
            still_value = still.metric()
        sum_x = sum_y = sum_z = 0.0
        n_sum = 0

    # ---- button (pressed = low). Ignore contact bounce for 0.3 s after a press
    pressed = not button.value
    press = pressed and not last_button and (now - last_press_t) > 0.3
    if press:
        last_press_t = now
    last_button = pressed

    # ---- logic
    is_still = still_value is not None and still_value < cfg.STILL_RANGE
    ev = monitor.update(dt, roll, pitch, sensor_ok=ok, still=is_still, ack=press)
    if ev:
        events_out += ev
        send_now = True
        for name, _ in ev:
            if name == "turn":
                confirm_until = now + 1.0

    state = monitor.display_state()
    if state != last_state:
        silenced = None         # a new alarm always sounds, even if the last one was silenced
        last_state = state
    if press:
        flash_until = now + 0.15
        send_now = True
        events_out.append(("press", state))      # every press is logged: sync mark for video and silence timing
        if state != "normal":
            silenced = state

    quiet = state == "normal" or silenced == state or (state == "critical" and monitor.acked)
    beeper.set(None if quiet else state, now)
    beeper.tick(now)

    frac_left = max(0.0, min(1.0, monitor.remaining() / monitor.interval))
    render(now, state, monitor.acked, frac_left, flash_until, confirm_until)

    # ---- one line of JSON per second, and straight away when something happens
    if send_now or now - t_report >= 1.0:
        t_report = now
        send_now = False
        print(json.dumps({
            "roll": round(roll, 1),
            "pitch": round(pitch, 1),
            "pos": monitor.pos,
            "state": state,
            "acked": monitor.acked,
            "sound": not quiet,
            "remaining_s": round(monitor.remaining(), 1),
            "interval_s": round(monitor.interval, 1),
            "anchor": round(monitor.anchor if monitor.anchor is not None else 0.0, 1),
            "hold_s": round(monitor.cand_t, 1),
            "hold_need_s": round(monitor.dwell, 1),
            "scale": cfg.TIME_SCALE,
            "still": None if still_value is None else round(still_value, 4),
            "ok": ok,
            "ev": events_out,
        }))
        events_out = []

    # ---- hold the sample rate
    spare = period - (time.monotonic() - now)
    if spare > 0:
        time.sleep(spare)
