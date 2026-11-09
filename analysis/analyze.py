"""
analyze.py  -  turns the verification runs into the numbers for the D7 verification report.

Every input is a CSV you record during a bench run. Templates sit next to this script.
Run any part on its own:

    python analyze.py --calibration calibration.csv
    python analyze.py --drift drift_log.csv
    python analyze.py --log protocol_log.csv --truth protocol_truth.csv
    python analyze.py --log alarm_log.csv --alarms
    python analyze.py --log fault_log.csv --faults faults.csv
    python analyze.py --log protocol_log.csv --truth protocol_truth.csv --upright

A "log" is the export from the laptop service (http://localhost:8000/api/export.csv) or the
"Download log (CSV)" button on the monitor page. Both have the same columns.

Time zero for the truth and fault files is the FIRST press of the bedside button in the log.
Press the button once on camera at the start of every filmed run: the video and the log then
share the same zero.

Results go to results/: summary.md plus the figures.

Needs: pip install pandas numpy matplotlib
"""
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = "results"

# acceptance criteria, as written in D1 and D6
ER1_MAX_ERR_DEG = 5.0
ER1_MAX_DRIFT_DEG = 2.0
ER2_MIN_AGREEMENT = 0.95
ER2_SETTLE_S = 3.0
ER4_MAX_FALSE_TURNS = 0
ER4_MIN_SENSITIVITY = 0.95
ER5_MAX_ONSET_ERR_S = 5.0
ER6_MAX_SILENCE_S = 0.5
ER7_MAX_DETECT_S = 60.0
ER8_MAX_UPRIGHT_ERR = 0.05


def write(lines):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "summary.md"), "a") as f:
        f.write("\n".join(lines) + "\n\n")
    print("\n".join(lines) + "\n")


def verdict(ok):
    return "PASS" if ok else "FAIL"


# ------------------------------------------------------------------ log reading
def read_log(path):
    df = pd.read_csv(path)
    t = pd.to_datetime(df["t"], utc=False, format="mixed")
    if getattr(t.dt, "tz", None) is not None:
        t = t.dt.tz_convert(None)
    df["time_s"] = (t - t.iloc[0]).dt.total_seconds()
    df["events"] = df["ev"].fillna("[]").apply(lambda s: json.loads(s) if isinstance(s, str) else [])
    return df


def events(df):
    rows = []
    for _, r in df.iterrows():
        for name, detail in r["events"]:
            rows.append({"time_s": r["time_s"], "name": name, "detail": detail,
                         "interval_s": r["interval_s"], "scale": r.get("scale", 1.0)})
    return pd.DataFrame(rows, columns=["time_s", "name", "detail", "interval_s", "scale"])


def sync_zero(ev):
    presses = ev[ev["name"] == "press"]
    if presses.empty:
        raise SystemExit("No button press in the log. Press the bedside button once on camera at the start of the run.")
    return presses["time_s"].iloc[0]


# ------------------------------------------------------------------ ER-1 calibration
def calibration(path):
    d = pd.read_csv(path)                                   # true_deg, trial, measured_deg
    slope, icpt = np.polyfit(d["true_deg"], d["measured_deg"], 1)
    pred = slope * d["true_deg"] + icpt
    ss_res = ((d["measured_deg"] - pred) ** 2).sum()
    ss_tot = ((d["measured_deg"] - d["measured_deg"].mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot
    d["error_deg"] = d["measured_deg"] - d["true_deg"]
    d["residual_deg"] = d["measured_deg"] - pred
    by = d.groupby("true_deg")["error_deg"].agg(["mean", "std", "min", "max", "count"]).reset_index()
    worst = d["error_deg"].abs().max()

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot([-95, 95], [-95, 95], color="0.6", lw=1, label="ideal")
    ax[0].scatter(d["true_deg"], d["measured_deg"], s=18, label="readings")
    xs = np.array([-95, 95])
    ax[0].plot(xs, slope * xs + icpt, lw=1.2, label="fit %.3fx %+.2f" % (slope, icpt))
    ax[0].set_xlabel("Jig angle (deg)"); ax[0].set_ylabel("Reported roll (deg)")
    ax[0].set_title("Calibration curve"); ax[0].legend(frameon=False)
    ax[1].axhspan(-ER1_MAX_ERR_DEG, ER1_MAX_ERR_DEG, color="0.92")
    ax[1].scatter(d["true_deg"], d["error_deg"], s=18)
    ax[1].axhline(0, color="0.6", lw=1)
    ax[1].set_xlabel("Jig angle (deg)"); ax[1].set_ylabel("Error (deg)")
    ax[1].set_title("Error per reading (band = +/- %g deg)" % ER1_MAX_ERR_DEG)
    fig.tight_layout(); os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "calibration.png"), dpi=150)

    lines = ["## ER-1 calibration", "",
             "Fit: reported = %.4f x jig %+.2f deg, R squared %.4f, n = %d readings." % (slope, icpt, r2, len(d)),
             "Largest error %.2f deg. Residual standard deviation %.2f deg." % (worst, d["residual_deg"].std()),
             "", "| Jig angle (deg) | Mean error (deg) | SD (deg) | Min (deg) | Max (deg) | n |",
             "|---|---|---|---|---|---|"]
    for _, r in by.iterrows():
        lines.append("| %g | %.2f | %.2f | %.2f | %.2f | %d |" % (r["true_deg"], r["mean"], r["std"] if r["count"] > 1 else 0,
                                                               r["min"], r["max"], r["count"]))
    lines += ["", "ER-1 accuracy (every reading within +/- %g deg): **%s**" % (ER1_MAX_ERR_DEG, verdict(worst <= ER1_MAX_ERR_DEG))]
    write(lines)


# ------------------------------------------------------------------ ER-1 drift
def drift(path):
    df = read_log(path)
    df = df[df["ok"].astype(str).str.lower() == "true"]
    hours = df["time_s"] / 3600
    slope, icpt = np.polyfit(hours, df["roll"], 1)
    start = df[df["time_s"] < 60]["roll"].mean()
    dev = (df["roll"] - start).abs().max()
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(df["time_s"] / 60, df["roll"] - start, lw=0.8)
    ax.axhspan(-ER1_MAX_DRIFT_DEG, ER1_MAX_DRIFT_DEG, color="0.92", zorder=0)
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Roll change from first minute (deg)")
    ax.set_title("Drift, sensor still on the jig")
    fig.tight_layout(); os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, "drift.png"), dpi=150)
    write(["## ER-1 drift", "",
           "Run length %.1f min. Trend %.2f deg per hour. Largest departure from the first minute %.2f deg." % (
               df["time_s"].iloc[-1] / 60, slope, dev),
           "", "ER-1 drift (within +/- %g deg over the run): **%s**" % (ER1_MAX_DRIFT_DEG, verdict(dev <= ER1_MAX_DRIFT_DEG))])


# ------------------------------------------------------------------ ER-2, ER-4 protocol scoring
def protocol(log_path, truth_path):
    df = read_log(log_path)
    ev = events(df)
    zero = sync_zero(ev)
    truth = pd.read_csv(truth_path)                         # step, label, position, start_s, end_s
    turns = ev[ev["name"] == "turn"].copy()
    turns["t"] = turns["time_s"] - zero
    used = set()
    rows = []
    for _, s in truth.iterrows():
        hit = turns[(turns["t"] >= s["start_s"]) & (turns["t"] <= s["end_s"] + 5)]
        counted = len(hit) > 0
        used.update(hit.index)
        if s["label"] == "turn":
            outcome = "TP" if counted else "FN"
        elif s["label"] in ("partial", "none", "upright"):
            outcome = "FP" if (counted and s["label"] != "upright") else "TN"
        else:
            outcome = ""
        rows.append({"step": s["step"], "label": s["label"], "device_counted_turn": counted, "outcome": outcome})
    res = pd.DataFrame(rows)
    stray = turns[~turns.index.isin(used) & (turns["t"] >= 0)]
    tp = (res["outcome"] == "TP").sum(); fn = (res["outcome"] == "FN").sum()
    fp = (res["outcome"] == "FP").sum() + len(stray); tn = (res["outcome"] == "TN").sum()
    n_partial = (truth["label"] == "partial").sum()
    sens = tp / (tp + fn) if tp + fn else float("nan")
    spec = tn / (tn + fp) if tn + fp else float("nan")
    ftr = fp / n_partial if n_partial else float("nan")
    os.makedirs(OUT, exist_ok=True)
    res.to_csv(os.path.join(OUT, "protocol_scored.csv"), index=False)

    # ER-2: agreement of the reported position with the video, settling time excluded at each step start
    agree = total = 0
    for _, s in truth.iterrows():
        if not isinstance(s.get("position"), str):
            continue
        seg = df[(df["time_s"] - zero >= s["start_s"] + ER2_SETTLE_S) & (df["time_s"] - zero <= s["end_s"])]
        total += len(seg)
        agree += (seg["pos"] == s["position"]).sum()
    agreement = agree / total if total else float("nan")

    write(["## ER-4 turn detection against video", "",
           "| | Device counted a turn | Device did not |", "|---|---|---|",
           "| True turn (video) | %d (TP) | %d (FN) |" % (tp, fn),
           "| Partial turn or no turn (video) | %d (FP) | %d (TN) |" % (fp, tn), "",
           "Sensitivity %.3f. Specificity %.3f. False turn rate %d of %d partial manoeuvres (%.3f). Turns counted outside any scripted step: %d." % (
               sens, spec, fp, n_partial, ftr, len(stray)),
           "", "ER-4 (false turns <= %d and sensitivity >= %.2f): **%s**" % (
               ER4_MAX_FALSE_TURNS, ER4_MIN_SENSITIVITY, verdict(fp <= ER4_MAX_FALSE_TURNS and sens >= ER4_MIN_SENSITIVITY)),
           "", "## ER-2 position agreement with video", "",
           "%d of %d scored samples agree (%.1f%%), first %g s of each step excluded." % (agree, total, 100 * agreement, ER2_SETTLE_S),
           "", "ER-2 (agreement >= %.0f%%): **%s**" % (100 * ER2_MIN_AGREEMENT, verdict(agreement >= ER2_MIN_AGREEMENT))])
    return df, ev, zero, truth


# ------------------------------------------------------------------ ER-5, ER-6 alarm timing
def alarms(log_path):
    df = read_log(log_path)
    ev = events(df)
    starts = [0.0] + list(ev[ev["name"] == "turn"]["time_s"])
    lines = ["## ER-5 alarm onset", "",
             "Measured on the laptop clock from the last effective turn (or power-up). Expected onsets: advisory at 87.5% of the interval, critical at 100%.",
             "", "| Alarm | Expected (s) | Logged (s) | Error (s) |", "|---|---|---|---|"]
    errs = []
    for kind, frac in (("advisory", 0.875), ("critical", 1.0)):
        for _, a in ev[ev["name"] == kind].iterrows():
            t0 = max(s for s in starts if s <= a["time_s"])
            expected = t0 + frac * a["interval_s"]
            err = a["time_s"] - expected
            errs.append(abs(err))
            lines.append("| %s | %.1f | %.1f | %+.2f |" % (kind, expected, a["time_s"], err))
    worst = max(errs) if errs else float("nan")
    lines += ["", "Largest onset error %.2f s over %d alarms." % (worst, len(errs)),
              "", "ER-5 onset (every alarm within +/- %g s): **%s**" % (ER5_MAX_ONSET_ERR_S, verdict(bool(errs) and worst <= ER5_MAX_ONSET_ERR_S))]

    # ER-6: a press during an alarm must report the sound off in the same or the next message
    lines += ["", "## ER-6 silence on button press", "",
              "| Press at (s) | State | Sound off after (s) |", "|---|---|---|"]
    delays = []
    for i, r in df.iterrows():
        for name, detail in r["events"]:
            if name == "press" and detail in ("advisory", "critical", "technical"):
                later = df[(df["time_s"] >= r["time_s"]) & (df["sound"].astype(str).str.lower() == "false")]
                d = later["time_s"].iloc[0] - r["time_s"] if not later.empty else float("nan")
                delays.append(d)
                lines.append("| %.2f | %s | %.2f |" % (r["time_s"], detail, d))
    w = max(delays) if delays else float("nan")
    lines += ["", "Device-reported silencing: largest delay %.2f s over %d presses (confirm on video at 30 frames per second)." % (w, len(delays)),
              "", "ER-6 silence (every press <= %g s): **%s**" % (ER6_MAX_SILENCE_S, verdict(bool(delays) and w <= ER6_MAX_SILENCE_S))]
    write(lines)


# ------------------------------------------------------------------ ER-7 faults
def faults(log_path, faults_path):
    df = read_log(log_path)
    ev = events(df)
    zero = sync_zero(ev)
    tech = ev[ev["name"] == "technical"].copy()
    tech["t"] = tech["time_s"] - zero
    f = pd.read_csv(faults_path)                           # trial, fault, t_fault_s
    lines = ["## ER-7 fault detection (labelled fault dataset)", "",
             "| Trial | Fault | Fault at (s) | Technical alarm at (s) | Detection time (s) |", "|---|---|---|---|---|"]
    det = []
    for _, r in f.iterrows():
        after = tech[tech["t"] >= r["t_fault_s"]]
        if after.empty:
            lines.append("| %s | %s | %.1f | none | missed |" % (r["trial"], r["fault"], r["t_fault_s"]))
            det.append(float("inf"))
        else:
            d = after["t"].iloc[0] - r["t_fault_s"]
            det.append(d)
            lines.append("| %s | %s | %.1f | %.1f | %.1f |" % (r["trial"], r["fault"], r["t_fault_s"], after["t"].iloc[0], d))
    w = max(det) if det else float("nan")
    lines += ["", "Detected %d of %d faults, slowest %.1f s." % (sum(np.isfinite(det)), len(det), w),
              "", "ER-7 (every fault detected within %g s): **%s**" % (ER7_MAX_DETECT_S, verdict(bool(det) and w <= ER7_MAX_DETECT_S))]
    write(lines)


# ------------------------------------------------------------------ ER-8 time upright
def upright(log_path, truth_path):
    df = read_log(log_path)
    ev = events(df)
    zero = sync_zero(ev)
    truth = pd.read_csv(truth_path)
    video = sum(r["end_s"] - r["start_s"] for _, r in truth.iterrows() if r["label"] == "upright")
    t = df["time_s"].to_numpy()
    gaps = np.minimum(np.diff(t), 5.0)
    up = (df["pos"].to_numpy()[:-1] == "upright")
    scale = float(df["scale"].iloc[0]) if "scale" in df else 1.0
    device = gaps[up].sum()
    err = (device - video) / video if video else float("nan")
    write(["## ER-8 time upright", "",
           "Video %.1f s, device %.1f s (log time; multiply both by %g for patient time in a demo-speed run). Difference %+.1f%%." % (
               video, device, scale, 100 * err),
           "", "ER-8 time upright (within +/- %.0f%%): **%s**" % (100 * ER8_MAX_UPRIGHT_ERR, verdict(abs(err) <= ER8_MAX_UPRIGHT_ERR))])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--calibration"); p.add_argument("--drift"); p.add_argument("--log")
    p.add_argument("--truth"); p.add_argument("--faults")
    p.add_argument("--alarms", action="store_true"); p.add_argument("--upright", action="store_true")
    p.add_argument("--out", default="results")
    a = p.parse_args()
    OUT = a.out
    if a.calibration:
        calibration(a.calibration)
    if a.drift:
        drift(a.drift)
    if a.log and a.truth and not a.upright:
        protocol(a.log, a.truth)
    if a.log and a.alarms:
        alarms(a.log)
    if a.log and a.faults:
        faults(a.log, a.faults)
    if a.log and a.truth and a.upright:
        upright(a.log, a.truth)
