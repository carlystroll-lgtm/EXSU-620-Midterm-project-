# Project 08: Has this patient been turned

Repositioning compliance and mobilisation patch. EXSU 620 Digital Prototyping, Fall 2026, Group 08.

A sensor on the chest of a bench phantom reports which way it is lying. The Pico decides when a turn
has offloaded tissue (a roll change of at least 30 degrees held for 15 minutes), prompts 15 minutes
before the 2 hour interval ends, alarms when it ends with no effective turn, and logs turns and time
upright for each shift. Bench only: nothing here goes near a patient or clinical equipment.

## What is in this folder

| Path | What it is |
|---|---|
| `code.py` | Pico firmware (CircuitPython 9). Reads the sensor at 20 Hz, drives the ring, speaker and button, prints one JSON line per second and at once on every event |
| `turnlogic.py` | Position classes, the turn rule and the alarm states. Runs on the Pico and on the laptop |
| `test_turnlogic.py` | Eight scripted tests of the turn logic. `python test_turnlogic.py` |
| `server.py` | Laptop service: reads the Pico over USB, stores every message in SQLite, serves the live page, the REST endpoints and the CSV export, and sends phone alerts to opted-in recipients |
| `monitor.html` | Live page: patient-in-bed view, bedside light mirror, countdown, roll trace, events. Served by `server.py`, or opened alone in Chrome to read the Pico directly |
| `dashboard.html` | Older dashboard with simulation buttons (`/classic`) |
| `enclosure/` | `make_enclosure.py` and the seven printed parts as STL |
| `analysis/` | `analyze.py` for the verification report, the scripted protocol and the data-sheet templates |
| `requirements.txt` | Laptop Python packages |

## Wiring (shield power switch on 3.3V)

| Part | Connection |
|---|---|
| LSM6DS3TR-C sensor | Grove to STEMMA QT cable into Grove port I2C0 (SDA GP8, SCL GP9) |
| NeoPixel Ring 16 | Power to VBUS (5 V), GND to GND, Data Input to GP16 |
| PAM8302 amplifier | Vin to 3V3 OUT through the breadboard red rail, GND to GND, A+ to GP18, A- to GND, SD open |
| 3 W 8 ohm speaker | Amplifier output + and - only |
| Acknowledge button | GP20 and GND (internal pull-up, active low) |

## Deploy

1. Pico: hold BOOTSEL, plug in USB, drag the CircuitPython 9 UF2 for the Pico 2 W onto the drive.
2. Copy `adafruit_lsm6ds`, `adafruit_register`, `adafruit_bus_device` and `neopixel.mpy` from the
   matching Adafruit bundle into `CIRCUITPY/lib`.
3. Copy `code.py` and `turnlogic.py` to `CIRCUITPY`. The ring shows green.
4. Laptop (Python 3.11 or later):
   ```
   python3 -m venv venv
   source venv/bin/activate          (Windows: venv\Scripts\activate)
   pip install -r requirements.txt
   ```
5. Find the port (`ls /dev/tty.usbmodem*` on a Mac, Device Manager on Windows) and start the service:
   ```
   python server.py --port /dev/tty.usbmodem1101
   ```
6. Open `http://localhost:8000`. On a phone on the same network: `http://<laptop IP>:8000`.
7. Phone alerts: each course participant who opts in installs the ntfy app, subscribes to a private
   topic, and is registered with the time they consented:
   ```
   python server.py --add-recipient "Name (course participant)" their-topic
   python server.py --list-recipients
   ```
8. Without hardware: `python server.py --simulate` (2 hours pass in 2 minutes).

Only one program can hold the Pico's USB port: close the VS Code Serial Monitor and Thonny before
starting the service.

## Demo speed

`cfg.TIME_SCALE = 60.0` in `code.py` makes the 2 hour interval last 2 minutes and the 15 minute hold
last 15 seconds. The live page shows a "Demo speed" label whenever it is on. Set it back to `1.0`
for real-time runs.

## Data

SQLite file `patch.db` next to `server.py`. Tables: `messages` (every line as received), `samples`,
`events`, `recipients` (label, ntfy topic, consent time), `notifications` (each phone alert sent).
No patient identifiers are stored or sent. Export: `http://localhost:8000/api/export.csv`.

## Verification

See `analysis/analyze.py`. Press the bedside button once on camera at the start of every filmed run:
that press is the time zero shared by the video and the log.
