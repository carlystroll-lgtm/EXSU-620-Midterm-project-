# One-phone fault-notification verification — IMG_1611.mov

Original: `/Users/kyri/Desktop/IMG_1611.mov`. Duration 53.01 seconds; approximately 29.98 fps. Original unchanged. Local frame review uses returned presentation timestamps. Creation metadata: 2026-11-07 21:06:38, America/Toronto; video and laptop clocks were not independently synchronized.

## Video evidence

- At actual **11.977 s**, the sensor is visibly powered and connected, the main ring is green, and the phone displays the prior chat history. No current 9:07 PM sensor alert is present yet.
- The sensor connector is handled during approximately 14–22 s, partially obscured by hands. The sensor is clearly disconnected and unpowered by **22.985 s**.
- At **24.987 s**, the phone still shows the earlier chat sequence. At **25.988 s**, the chat gains another incoming line. The message is clearly readable in the close-up at **28.990 s**: **“Bed patch: check the patch”**, timestamped **9:07 PM**, following the earlier 9:04 PM technical message.
- The receiving phone remains in view through the transition to the new message. This is stronger arrival evidence than the previous clip, in which the phone entered view after delivery.
- Reconnection handling and restored sensor power are visible late in the clip; the main ring subsequently returns to green. The log records `technical_clear`.

## Conservative timing assessment

The last unambiguously connected-and-powered reference frame is at **11.977 s**. The new alert is clearly readable by **28.990 s**. Because the physical unplug happens after that connected frame, **17.02 seconds is a conservative upper bound on physical-disconnection-to-visible-message time**, assuming the clip's continuous timebase. This bound deliberately includes pre-disconnection time and the later close-up, rather than claiming an exact electrical unplug or arrival instant.

The alert line appears between approximately 24.987–25.988 s, but small screen text and partially obscured connector contacts do not justify a frame-exact latency measurement. Do not describe the 17.02-second bound as an exact measured delay.

**One-phone receipt within the 30-second target: supported for this filmed sensor-fault trial by the conservative video bound.** It does not establish repeatability, all alert types, lock-screen/OS banner behavior, or receipt by a second phone. The filmed chat is open; the observed endpoint is message display inside Telegram.

## Matching server records

| Record | Mac local time |
|---|---|
| `technical: sensor` | 21:07:03.896 |
| Telegram API accepted, recipient 2 | 21:07:04.254 |
| Telegram API accepted, recipient 1 | 21:07:04.268 |
| `technical_clear` | 21:07:22.513 |

Server-event-to-API-response intervals are approximately 0.359 and 0.372 seconds. These are not phone receipt latencies. Two API acceptances are recorded, but only the filmed phone's arrival is visually verified. Video-relative timing above does not depend on subtracting phone and Mac wall clocks.

## Evidence retained

- Raw selected server telemetry, events and Telegram records: `video_1611_log_evidence.json`.
- Still frames: `video_1611_frames/`.
- Relevant views: `frame_000_12.00.jpg`, `frame_006_23.00.jpg`, `frame_008_25.00.jpg`, `frame_009_26.00.jpg`, `frame_012_29.00.jpg`.
- Original and previous video reviews remain preserved. This successful trial does not remove prior failed accuracy measurements or resolve the earlier missing recovery event's cause.
