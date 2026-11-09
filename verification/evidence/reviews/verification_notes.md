# Verification status

Live operation and delivery to both phones were confirmed during setup. These are functional observations, not measured formal acceptance results.

The guided calibration records 21 independently positioned roll measurements, three trials at each of −90, −60, −30, 0, +30, +60, +90 degrees. The project analysis script's criterion is every reading within ±5 degrees. An independent jig/protractor and operator positioning are required. Capture photos or video showing the reference and dashboard.

Configuration observed on the connected Pico:

- Demo scale 60: a nominal two-hour interval takes two minutes, and a fifteen-minute hold takes fifteen seconds. Demo results do not establish full-duration timing or drift.
- Audible alerts disabled. The original audible-silencing test cannot be scored as passed in this configuration.
- Stillness threshold is zero. Stillness-based detachment detection is disabled and cannot be scored as passed. Sensor disconnection is a separate fault.
- The deployed firmware does not log button `press` events. The existing analysis script requires these to synchronize filmed protocol/fault trials. Add and verify press logging before those trials.

Telegram API acceptance timestamps indicate server/API response time, not phone receipt time. Measure phone receipt independently on each phone for latency verification. Do not infer a latency pass from successful API responses alone.

No formal accuracy, drift, classification, sensitivity, alarm timing, button, fault, upright-duration or phone-latency pass has been issued yet. Preserve raw logs and record actual observations without filling template measurements from expected values.
