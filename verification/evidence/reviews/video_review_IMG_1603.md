# Sensor-disconnection video review — IMG_1603.mov

Source: `/Users/kyri/Desktop/IMG_1603.mov`, 46.63 seconds, approximately 30 frames/second. Reviewed using locally extracted frames with requested timestamps and returned actual presentation times. Original video was not modified.

## Visible observations

| Observation | Video time | Basis |
|---|---:|---|
| Sensor power light still on during connector handling | 4.50 s | Green light visible in sensor enclosure |
| Sensor power light off; connector withdrawn | 5.00 s | Sensor enclosure dark |
| Main ring still green | 9.50 s | Green ring visible |
| Main ring shows cyan/blue technical indication | 10.00 s | Technical pattern visible |
| Sensor light off during reconnection handling | approximately 28 s | Hand partially obscures connector |
| Sensor power light restored | approximately 29 s | Green sensor light visible |
| Main ring still cyan/blue | approximately 30 s | Fault pattern visible |
| Main ring green again | approximately 31 s | Normal pattern visible |

Estimated power-loss-to-visible-fault response: **4.5–5.5 seconds**, using the transition brackets above. Connector contacts are partially obscured; sensor power-light loss is the visible disconnection proxy. This is a frame-bracketed estimate, not a frame-exact electrical measurement.

The visible fault response in this clip is within the existing analysis script's **60-second sensor-fault detection criterion** for this filmed trial. This does not establish detection of stillness, detachment, or every other fault type.

Recovery is visible approximately two seconds after the sensor power light returns (roughly 1–3 seconds using the sampled transition brackets). Reconnection contacts are obscured; do not report an exact physical contact-to-recovery delay.

## Corresponding recorded trial

The file's creation-time metadata is 2026-11-07 18:09:03, America/Toronto. Its sequence and timing are consistent with the third recorded sensor-disconnection trial, but the phone and laptop clocks were not independently synchronized. Do not subtract video wall-clock metadata from laptop timestamps to claim exact latency.

Saved third-trial records show:

- First captured `ok=false` sample: 18:09:08.762.
- `technical: sensor` event: 18:09:12.737.
- Telegram API acceptance record: 18:09:13.085, approximately 0.349 seconds after the server event timestamp, for one active recipient.
- First captured recovered `ok=true`, `state=normal` sample: 18:09:36.967.
- No `technical_clear` event in the saved third-trial recovery log.

The ~3.97 seconds between the first captured faulted sample and the event is a log-observed interval; it is not the physical unplug latency. Incoming messages have gaps, and the first faulted sample can follow the actual fault onset.

The video confirms visible fault detection and recovery even though the third recovery event is missing from the laptop log. The cause of the missing event is unresolved; firmware emission or USB/log capture loss remain possible. It must not be counted as successful recovery-event logging.

## Limits

- The phone screen is too small/obscured to establish notification arrival time or content. Telegram API acceptance is not proof of phone receipt latency.
- Only one active recipient was found in the database during this fault test. Earlier user-reported two-phone receipt is separate evidence.
- Audio was not analyzed. Firmware and saved telemetry have sound disabled; this is not a button-to-silence latency test.
- This clip covers one filmed unplug/reconnect cycle, not three independently timed cycles.
- Accuracy checks elsewhere contain out-of-tolerance attempts; this fault video does not establish an overall verification pass.

Evidence images: `video_transition_sheet.jpg` and individual frames under `video_frames/`. Raw third-trial logs: `sensor_unplug_trial3_20261107_180921.json` and `sensor_reconnect_trial3_20261107_180958.json`.
