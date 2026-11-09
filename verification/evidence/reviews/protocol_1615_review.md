# Scripted protocol video review — IMG_1615

Video: `/Users/kyri/Downloads/IMG_1615.mov`, 26 minutes 4.46 seconds, about 29.98 frames/second. Original file unchanged. Recording metadata: November 8, 2026, 15:10:12 America/Toronto. This review inspected a broad timeline storyboard and early/middle/late timed views for all 46 planned steps; it is not frame-by-frame certification of every angle and dwell.

## Data continuity

The separately saved armed log window spans 26.8 minutes, including time outside the video. It contains 1,608 samples, no missing source sequence numbers or source restarts, and a maximum receipt gap of 1.054 seconds. Four samples report a sensor fault and are retained. The log contains 19 turn events: 16 lateral and three upright, plus five partial events and 34 position events.

## Diagnostic comparison with the plan

| Comparison | Count |
|---|---|
| Planned lateral/return turn steps with a turn event | 16 / 20 |
| Planned lateral/return turn steps without an event | 4: steps 3, 4, 11, 12 |
| Planned partial/no-turn steps with a turn event | 0 / 23 |
| Planned upright steps with an upright turn event | 3 / 3 |

**These are schedule-comparison counts, not independently validated sensitivity or specificity.** A provisional four-second guide-start offset was used, with a five-second event-window tolerance matching the existing analysis approach. Varying the offset from zero to eight seconds gives the same counts. The start button/independent stopwatch is not in the camera framing, and there is no saved physical press marker. Camera metadata and recognizable movements support a provisional association but do not establish exact synchronization.

If the planned labels were incorrectly treated as truth, the event ratios would be 80% for planned positives and 100% for planned negatives. Do not present those as validated sensitivity/specificity: actual angle, axis, dwell, and prerequisites for a return turn must first be established independently.

## Operator clarification and scoring disposition

After reviewing the results, the operator reported that the holds were interrupted. Steps **3 and 11** are classified as **invalid test executions based on the operator report**, rather than confirmed device misses. Steps **4 and 12** are excluded as dependent return steps because the preceding qualifying lateral turns were not established. This explanation was supplied after testing and is not independently confirmed as the cause from the video.

The original observation remains: no turn event occurred in those four scheduled windows. They are retained in the records with explicit exclusion reasons, not replaced with passing results. The remaining planned positive-step coverage is **16/16**. This remains a schedule comparison, not validated sensitivity, because reference-angle/dwell and synchronization limitations still apply. No change is made to the separate angle-accuracy discrepancies.

## Original observed discrepancy

The first two planned right-turn holds (steps 3 and 11) show hand-held tilting against a protractor, but the markings and level reference are not consistently readable. No turn event was recorded during either hold or its following flat-return step. The device reported roll roughly 17–25 degrees during those two held windows, below its 30-degree criterion. That device result cannot itself prove the true physical angle. The video does not presently distinguish reference/positioning error from sensor/calibration error. Once the preceding lateral turn is not established, failure to count its flat return is not an independent sensitivity failure.

Later lateral turns and upright holds appear in the video and event log. Flat positions and gross upright posture are clear in many views; hands, sleeves, and the frame edge obscure several lateral references. Do not assume the nominal 40-degree target was actually achieved in every frame.

## Step-by-step review

| Step | Planned label / position | Event comparison | Video evidence limits |
|---|---|---|---|
| 1 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 2 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 3 | turn / right | no event | Tilted sensor and protractor visible, but angle scale/zero not reliably readable; no turn event. |
| 4 | turn / supine | no event | Sensor visibly rests flat in inspected views; no turn event. Prior effective-turn premise not established. |
| 5 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 6 | partial / not specified | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 7 | turn / left | event present | Lateral hold visible against protractor; some views obscured by sleeve; logged lateral turn. |
| 8 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 9 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 10 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 11 | turn / right | no event | Tilted sensor and protractor visible, but angle scale/zero not reliably readable; no turn event. |
| 12 | turn / supine | no event | Sensor visibly rests flat; no turn event. Prior effective-turn premise not established. |
| 13 | upright / upright | upright turn event present | Sensor visibly held upright in inspected views. |
| 14 | none / supine | no turn event | Sensor visibly rests on table in inspected stable views. |
| 15 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 16 | partial / not specified | no turn event | Tilt held across inspected views; exact short-hold duration/return requires finer video annotation. |
| 17 | turn / left | event present | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 18 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 19 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 20 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 21 | turn / right | event present | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 22 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 23 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 24 | partial / not specified | no turn event | Tilt visible; exact angle and brief-hold duration not independently resolved. |
| 25 | turn / left | event present | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 26 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 27 | upright / upright | upright turn event present | Sensor visibly held upright in inspected views. |
| 28 | none / supine | no turn event | Sensor visibly rests on table in inspected stable views. |
| 29 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 30 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 31 | turn / right | event present | Tilt visible; hands/sleeve obscure part of the sensor/reference. |
| 32 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 33 | partial / supine | no turn event | Wrist/sleeve obscures sensor in several inspected views. |
| 34 | partial / not specified | no turn event | Tilt and reference visible; exact angle/dwell not independently resolved. |
| 35 | turn / left | event present | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 36 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 37 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 38 | partial / supine | no turn event | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 39 | turn / right | event present | Hand-held tilt and reference instrument visible; angle markings or baseline not continuously readable. |
| 40 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |
| 41 | upright / upright | upright turn event present | Sensor visibly held upright in inspected views. |
| 42 | none / supine | no turn event | Sensor visibly rests on table in inspected stable views. |
| 43 | partial / supine | no turn event | Wrist/sleeve obscures sensor/reference in inspected views. |
| 44 | partial / not specified | no turn event | Tilt/reference partly at edge of frame; exact angle/dwell not independently resolved. |
| 45 | turn / left | event present | Much of sensor/reference lies near or beyond right frame edge in inspected views. |
| 46 | turn / supine | event present | Sensor visibly rests on table in inspected stable views. |

## Disposition

**Retain the full run; no unconditional protocol pass is issued.** The existing automatic scorer requires a first `press` event and independent ground-truth timing. Creating a synthetic press or relabeling the planned template as observed truth would hide those limitations, so neither was done.

Before repeating an entire 26-minute run, perform a short targeted right-turn check with a fixed, independently established 40-degree wedge and the sensor axes clearly identified. Film the reference face and the board together, include a visible time reference, and inspect the reported angle and turn event. This can identify whether the early misses were setup or device errors. It does not retroactively replace the current observations.

For full sensitivity, specificity and position agreement, obtain independently reviewable movement labels/times and resolve ambiguous steps. If that cannot be done from the existing footage, report the limitations and target the necessary retests rather than invent scores.

Evidence: [step comparison](protocol_1615_schedule_comparison.csv), [structured review](protocol_1615_review.json), original timed frames in `video_1615_frames/`, per-step frames in `video_1615_step_frames/`, and the preserved completed-run JSON.

## Conditional sensitivity calculation

After excluding steps 3, 4, 11 and 12 on the documented operator-reported execution/dependency grounds, all 16 retained planned turn trials contained a turn event. **Conditional observed sensitivity = 16/16 = 100%.** This is a formal arithmetic estimate conditional on those 16 trials being independently confirmed as qualifying turns. The current reference-angle/dwell and synchronization limitations prevent treating it as independently verified sensitivity or closing the >=95% requirement. No new observations were collected.
