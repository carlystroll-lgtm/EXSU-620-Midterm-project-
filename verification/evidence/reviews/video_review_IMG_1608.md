# One-phone notification video review — IMG_1608.mov

Original source: `/Users/kyri/Desktop/IMG_1608.mov`. Duration 97.98 seconds; approximately 29.98 frames/second. Creation-time metadata: 2026-11-07 20:43:20, America/Toronto. Original file unchanged. Timed still frames were extracted locally with actual frame presentation times.

## Supported observations

- At approximately 29–31 seconds, the receiving phone is clearly shown in the EXSU 620 Bed Patch bot conversation. The latest visible incoming message is **“Bed patch: check the patch”**, timestamped **8:43 PM**. This provides visible evidence of delivery to the filmed phone.
- The message is already present when the phone is brought into view. The instant of receipt is not visible, so this clip alone does not establish exact phone notification latency or an operating-system notification banner.
- A cyan/blue device fault indication is visible in the mid-clip frames, followed by green indication in later frames. Physical sensor connection handling is outside the main camera framing; exact unplug and reconnect times cannot be read from the video.
- The dashboard visible behind the phone displays a stale-data/USB warning (approximately 59 seconds without data in the 30-second frame). Its displayed position is not reliable live evidence for this recording. This does not imply the separate server log stopped: the local database contains telemetry and events during the interval.

## Matching local records

Phone and laptop clocks were not independently synchronized. The following wall-clock timestamps are from the Mac database; association with the clip is supported by recording metadata, message minute and event sequence, not a frame-exact synchronization marker.

| Recorded event | Mac local time |
|---|---|
| Technical sensor fault | 20:43:45.053 |
| Telegram API acceptance, recipient 2 | 20:43:45.409 |
| Telegram API acceptance, recipient 1 | 20:43:45.431 |
| `technical_clear` | 20:44:05.828 |
| Advisory | 20:44:29.730 |
| Critical | 20:44:44.730 |

The technical alert was accepted by Telegram approximately **0.356 and 0.378 seconds after the server event timestamp**. These are server-event-to-API-response intervals, not phone arrival times. Logs also record successful API acceptance for advisory and critical alerts to both recipient IDs.

Unlike the previous third-trial clip, this test has a saved `technical_clear` event. The prior missing event remains a separate finding; a later success does not establish its cause or erase it.

## Result and limits

**One-phone delivery demonstration: supported.** The technical-alert content is readable on the filmed phone, and the server records the corresponding technical event and successful API responses.

**Phone receipt latency criterion: not yet established.** The phone is off camera during the actual arrival, physical fault onset is not visibly timed, and there is no independently verified video-to-Mac clock synchronization. Do not label the API-response durations as phone notification latency.

**Two-phone arrival verification: not performed in this clip.** Two API responses are recorded, but only one receiving phone is shown.

For a timed retest, continuously frame the sensor connector, device ring, and receiving phone. Begin with the bot chat visible before unplugging, keep it visible through the appearance of the new message, and visibly unplug/reconnect only the sensor cable. This permits a conservative arrival-time bound using the same video clock. Use the dashboard served at `http://localhost:8000/` and confirm its data age is fresh before relying on it.

Evidence: `video_1608_log_evidence.json`; still frames in `video_1608_frames/`. The readable phone view is `video_1608_frames/frame_002_30.00.jpg` (actual frame time 29.992 seconds).
