"""
server.py  -  laptop service for the repositioning patch.

Reads one JSON line per second from the Pico over USB, stores it in SQLite,
and serves the dashboard and the REST endpoints.

    python server.py --port COM5              (Windows)
    python server.py --port /dev/tty.usbmodem1101   (Mac)
    python server.py --simulate               (no hardware, 2 hours pass in 2 minutes)

Dashboard:  http://localhost:8000          (live view, same page as monitor.html)
            http://localhost:8000/classic  (older dashboard with the simulation buttons)
Export:     http://localhost:8000/api/export.csv

Phone alerts go only to recipients who have opted in. Register one (stores the consent time):
    python server.py --add-recipient "Carly (course participant)" my-private-ntfy-topic
    python server.py --list-recipients
The recipient installs the ntfy app and subscribes to that topic. No patient information is stored
or sent: the database holds angles, states and events only.
"""
import argparse
import json
import os
import sqlite3
import threading
import time
import urllib.request
from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, PlainTextResponse

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "patch.db")
SHIFT_STARTS = [7, 15, 23]                  # hours of the day when a shift begins

app = FastAPI(title="Repositioning patch")
latest = {"t": 0.0, "data": None}
sim = {"on": False, "ack": False, "turn": False}   # the simulator has no bedside button


# ------------------------------------------------------------------ database
def db():
    con = sqlite3.connect(DB_PATH, timeout=5)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db() as con:
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("""CREATE TABLE IF NOT EXISTS samples(
            ts REAL, roll REAL, pitch REAL, pos TEXT, state TEXT,
            remaining_s REAL, still REAL)""")
        con.execute("CREATE TABLE IF NOT EXISTS events(ts REAL, type TEXT, detail TEXT)")
        con.execute("CREATE INDEX IF NOT EXISTS i_samples ON samples(ts)")
        con.execute("CREATE INDEX IF NOT EXISTS i_events ON events(ts)")
        # every line from the Pico exactly as received, for export and analysis
        con.execute("CREATE TABLE IF NOT EXISTS messages(seq INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL, raw TEXT)")
        # opted-in course participants who receive phone alerts, with the time they consented
        con.execute("""CREATE TABLE IF NOT EXISTS recipients(
            id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, topic TEXT, consented_at TEXT, active INTEGER DEFAULT 1)""")
        # each phone alert sent, for the notification latency check
        con.execute("CREATE TABLE IF NOT EXISTS notifications(ts REAL, recipient_id INTEGER, type TEXT, ok INTEGER, sent_ts REAL)")


def store(msg):
    """Save one message from the patch."""
    now = time.time()
    latest["t"] = now
    latest["data"] = msg
    with db() as con:
        con.execute("INSERT INTO messages(ts, raw) VALUES(?,?)", (now, json.dumps(msg)))
        con.execute("INSERT INTO samples VALUES(?,?,?,?,?,?,?)",
                    (now, msg.get("roll"), msg.get("pitch"), msg.get("pos"),
                     msg.get("state"), msg.get("remaining_s"), msg.get("still")))
        for name, detail in msg.get("ev", []):
            con.execute("INSERT INTO events VALUES(?,?,?)", (now, name, detail))
            if name in ("advisory", "critical", "technical"):
                push(name, now)


def push(name, event_ts):
    """Send an alert to every opted-in recipient. The text carries no patient information."""
    with db() as con:
        rows = con.execute("SELECT id, topic FROM recipients WHERE active=1 AND consented_at IS NOT NULL").fetchall()
    if not rows:
        return
    text = {"advisory": "Bed patch: turn due in 15 minutes",
            "critical": "Bed patch: turn overdue, no effective turn recorded",
            "technical": "Bed patch: check the patch"}[name]

    def send(rid, topic):
        ok = 0
        try:
            req = urllib.request.Request("https://ntfy.sh/" + topic, data=text.encode(), method="POST")
            urllib.request.urlopen(req, timeout=5)
            ok = 1
        except Exception as e:
            print("push failed:", e)
        with db() as con:
            con.execute("INSERT INTO notifications VALUES(?,?,?,?,?)", (event_ts, rid, name, ok, time.time()))
    for r in rows:
        threading.Thread(target=send, args=(r["id"], r["topic"]), daemon=True).start()


# -------------------------------------------------------------------- inputs
def read_serial(port):
    import serial
    while True:
        try:
            with serial.Serial(port, 115200, timeout=2) as ser:
                print("reading from", port)
                while True:
                    line = ser.readline().decode("utf-8", "ignore").strip()
                    if line.startswith("{"):
                        try:
                            store(json.loads(line))
                        except ValueError:
                            pass
        except Exception as e:
            print("serial problem:", e, "- retrying in 2 s")
            time.sleep(2)


def simulate():
    """Plays a scripted patient through the same logic the Pico runs."""
    from turnlogic import Config, Monitor
    cfg = Config()
    cfg.TIME_SCALE = 60.0
    m = Monitor(cfg)
    # (seconds, roll, pitch)
    script = [(40, 0, 2), (15, 8, 2), (30, 0, 2), (60, 42, 3), (20, 38, 3),
              (5, 5, 3), (150, 4, 3), (30, -40, 2), (40, 0, 78), (60, -35, 2)]
    print("simulating: 2 hours pass in 2 minutes")
    manual_roll = manual_left = shown_roll = 0
    while True:
        for seconds, script_roll, script_pitch in script:
            for _ in range(seconds):
                # the Turn patient button moves the patient for 20 s, then the script resumes
                if sim["turn"]:
                    sim["turn"] = False
                    manual_roll = 0 if abs(shown_roll) > 20 else 40
                    manual_left = 20
                if manual_left > 0:
                    manual_left -= 1
                    roll, pitch = manual_roll, 2
                else:
                    roll, pitch = script_roll, script_pitch
                shown_roll = roll
                events = []
                for _ in range(20):
                    events += m.update(0.05, roll, pitch, ack=sim["ack"])
                    sim["ack"] = False
                state = m.display_state()
                store({"roll": roll, "pitch": pitch, "pos": m.pos,
                       "state": state, "acked": m.acked,
                       "sound": state != "normal" and not (state == "critical" and m.acked),
                       "remaining_s": round(m.remaining(), 1),
                       "interval_s": m.interval, "anchor": round(m.anchor or 0.0, 1),
                       "hold_s": round(m.cand_t, 1), "hold_need_s": round(m.dwell, 1),
                       "scale": cfg.TIME_SCALE, "still": 0.2, "ok": True,
                       "ev": events})
                time.sleep(1)


# --------------------------------------------------------------------- shift
def shift_start(now=None):
    now = now or datetime.now()
    starts = [now.replace(hour=h, minute=0, second=0, microsecond=0) for h in SHIFT_STARTS]
    starts += [s - timedelta(days=1) for s in starts]
    return max(s for s in starts if s <= now)


def shift_summary():
    start = shift_start()
    t0 = start.timestamp()
    with db() as con:
        events = con.execute("SELECT type FROM events WHERE ts>=? ORDER BY ts", (t0,)).fetchall()
        rows = con.execute("SELECT ts, pos FROM samples WHERE ts>=? ORDER BY ts", (t0,)).fetchall()
    # time upright = sum of the gaps between consecutive samples while upright (gaps over 5 s are data loss)
    upright = 0.0
    for a, b in zip(rows, rows[1:]):
        if a["pos"] == "upright":
            upright += min(b["ts"] - a["ts"], 5.0)
    on_time = late = partial = turns = 0
    pending = False
    for (name,) in events:
        if name == "critical":
            late += 1
            pending = True
        elif name == "turn":
            turns += 1
            if pending:
                pending = False
            else:
                on_time += 1
        elif name == "partial":
            partial += 1
    intervals = on_time + late
    return {
        "shift_start": start.strftime("%H:%M"),
        "turns": turns,
        "late_intervals": late,
        "partial_turns": partial,
        "compliance_pct": None if intervals == 0 else round(100.0 * on_time / intervals),
        "out_of_bed_min": round(upright / 60.0, 1),
    }


# ----------------------------------------------------------------- endpoints
@app.get("/")
def live_view():
    return FileResponse(os.path.join(HERE, "monitor.html"))


@app.get("/classic")
def dashboard():
    return FileResponse(os.path.join(HERE, "dashboard.html"))


@app.get("/api/since")
def since(seq: int = -1):
    """Messages after seq, oldest first. seq=-1 returns only the newest seq, so a page starts live."""
    with db() as con:
        last = con.execute("SELECT COALESCE(MAX(seq), 0) FROM messages").fetchone()[0]
        if seq < 0:
            return {"last": last, "messages": []}
        rows = con.execute("SELECT seq, ts, raw FROM messages WHERE seq>? ORDER BY seq LIMIT 500", (seq,)).fetchall()
    return {"last": rows[-1]["seq"] if rows else seq,
            "messages": [dict(json.loads(r["raw"]), _seq=r["seq"], _ts=r["ts"]) for r in rows]}


@app.get("/api/export.csv")
def export_csv():
    """Every message as one CSV row, in the same columns as the monitor page's download."""
    cols = ["t", "roll", "pitch", "pos", "state", "acked", "sound", "remaining_s", "interval_s",
            "anchor", "hold_s", "hold_need_s", "scale", "still", "ok", "ev"]
    out = [",".join(cols)]
    with db() as con:
        for r in con.execute("SELECT ts, raw FROM messages ORDER BY seq"):
            m = json.loads(r["raw"])
            m["t"] = datetime.fromtimestamp(r["ts"]).isoformat(timespec="milliseconds")
            m["ev"] = json.dumps(m.get("ev", []))
            cells = []
            for c in cols:
                v = m.get(c)
                v = "" if v is None else str(v)
                cells.append('"' + v.replace('"', '""') + '"' if any(ch in v for ch in ',"\n') else v)
            out.append(",".join(cells))
    return PlainTextResponse("\n".join(out) + "\n", media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=patch-export.csv"})


@app.get("/api/status")
def status():
    with db() as con:
        ev = con.execute("SELECT ts,type,detail FROM events ORDER BY ts DESC LIMIT 15").fetchall()
    return {
        "simulated": sim["on"],
        "age_s": None if latest["data"] is None else round(time.time() - latest["t"], 1),
        "latest": latest["data"],
        "shift": shift_summary(),
        "events": [dict(e) for e in ev],
    }


@app.post("/api/ack")
def ack():
    """Stands in for the bedside button. Only works in simulation."""
    if sim["on"]:
        sim["ack"] = True
    return {"accepted": sim["on"]}


@app.post("/api/turn")
def turn():
    """Turns the simulated patient. Only works in simulation."""
    if sim["on"]:
        sim["turn"] = True
    return {"accepted": sim["on"]}


@app.get("/api/history")
def history(minutes: float = 10):
    t0 = time.time() - minutes * 60
    with db() as con:
        rows = con.execute("SELECT ts,roll,pitch,pos,state FROM samples WHERE ts>=? ORDER BY ts",
                           (t0,)).fetchall()
    return [dict(r) for r in rows]


@app.get("/api/shift")
def shift():
    return shift_summary()


@app.get("/api/events")
def events(limit: int = 200):
    with db() as con:
        rows = con.execute("SELECT ts,type,detail FROM events ORDER BY ts DESC LIMIT ?",
                           (limit,)).fetchall()
    return [dict(r) for r in rows]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", help="serial port of the Pico, for example COM5")
    p.add_argument("--simulate", action="store_true", help="run without hardware")
    p.add_argument("--http", type=int, default=8000)
    p.add_argument("--add-recipient", nargs=2, metavar=("LABEL", "NTFY_TOPIC"),
                   help="register an opted-in course participant for phone alerts")
    p.add_argument("--list-recipients", action="store_true")
    args = p.parse_args()
    init_db()
    if args.add_recipient:
        label, topic = args.add_recipient
        ok = input("Has %s agreed to receive bed patch alerts on their phone? Type yes: " % label)
        if ok.strip().lower() != "yes":
            raise SystemExit("Not registered: consent not given.")
        with db() as con:
            con.execute("INSERT INTO recipients(label, topic, consented_at) VALUES(?,?,?)",
                        (label, topic, datetime.now().astimezone().isoformat(timespec="seconds")))
        raise SystemExit("Registered %s." % label)
    if args.list_recipients:
        with db() as con:
            for r in con.execute("SELECT id, label, topic, consented_at, active FROM recipients"):
                print(dict(r))
        raise SystemExit
    if not args.port and not args.simulate:
        p.error("give --port or --simulate")
    sim["on"] = args.simulate
    target = simulate if args.simulate else lambda: read_serial(args.port)
    threading.Thread(target=target, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=args.http, log_level="warning")
