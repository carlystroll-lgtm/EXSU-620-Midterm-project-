# EXSU 620 — verification summary

Bench prototype tests conducted November 7–8, 2026. This summary describes the evidence collected; it does not claim an unconditional pass of every course requirement. Acceptance thresholds below come from the project's analysis script and prior project context, rather than a separately supplied current course rubric.

## Configuration tested

Raspberry Pi Pico 2 W with CircuitPython, angle sensor, light ring, acknowledgement button, USB logging server and Telegram alerts. Audible output is intentionally disabled. Roll/pitch zero offsets were set from an operator-confirmed level reference. Stillness threshold remains zero, disabling stillness-based detachment detection. Demo runs used scale 60; the final two-hour run used scale 1. Telemetry sequence numbers and device uptime were added after logging gaps were found.

## Results

| Check | Evidence/result | Interpretation |
|---|---|---|
| Zero correction | Post-correction mean roll +0.07°, pitch +0.08° over ten seconds | Zero reference check completed; not a full accuracy test |
| Roll accuracy, ±5° | The later −60° trial 1 repeat has +1.66° error; its original −6.94° error is retained. The later +60° trial 2 repeat has +1.24° error; its original +6.16° error is retained. All latest selected captures are within tolerance, but earlier discrepancies remain unresolved. Independent 0° trial 1 subsequently captured at +1.50° on November 8 | Overall accuracy pass not established; all attempts retained |
| Stationary drift, ±2° | 31.08-minute recorded span, 1,830 samples; maximum roll departure 0.346°; no missing sequences or faults | Pass for the tested stationary duration only |
| Effective turns | Left turn near −41.9°, return flat, and right turn near +40.2° recorded after demo hold; timer reset to ~120 s | Functional turn/reset behavior demonstrated; not a full sensitivity study |
| Small movement rejection | Approximately 12–14° roll did not generate a turn or reset timer | Functional rejection demonstrated |
| Brief movement rejection | Partial event of about 14 s; no turn/reset | Observed partial trial documented; not an exact eight-second trial |
| Button acknowledgement | `ack` recorded; `acked=true`; critical state and overdue timer retained | Acknowledgement behavior demonstrated; audible-silencing latency not tested |
| Upright duration, ±5% | Independent operator stopwatch 61.49 s; logged interval 62.437 s; +0.947 s / +1.54%; no missing sequences | Meets numerical criterion in this stopwatch-based trial; no saved video |
| Demo alarm onset, ±5 s | Advisory 104.958 s (target 105); critical 119.974 s (target 120) after effective turn | Pass for recorded demo trial; user confirmed both phone alerts |
| Normal-speed alarm onset, ±5 s | Advisory ~6,300.0 s; critical ~7,200.0 s. 7,266 samples across ~2 h 2 min 44 s; no missing sequences, restarts or faults | Pass for recorded normal-speed interval; user confirmed both phone alerts |
| Sensor unplug/reconnect | Multiple technical faults and recoveries; filmed IMG_1603 supports approximately five-second visible fault response | Sensor disconnection behavior demonstrated; not all fault types |
| One-phone technical receipt within 30 s | IMG_1611 shows new message, with conservative ≤17.02 s bound from last clearly connected frame to readable alert | Supports target for this filmed trial, with Telegram chat open |
| Two-phone receipt | Earlier user confirmation and API acceptance records for two recipients | Functional reports retained; two-phone arrival latency not filmed |

## Findings that remain open

1. **Accuracy:** retain out-of-tolerance measurements. Repeat runs may be presented as repeats, with earlier attempts in the appendix. A documented setup error is needed to justify excluding an attempt; a better later reading alone is not an exclusion reason. The independent zero trial was later completed on November 8 at +1.50°; its collection date and chronology are retained.
2. **Full scripted scoring:** the 46-step filmed protocol and corresponding independent truth dataset were not completed. Position agreement ≥95%, turn sensitivity ≥95%, and zero false turns across that dataset have not been established by the smaller functional checks.
3. **Fault coverage:** stillness-based detachment detection is disabled. Stationary/detachment trials cannot be reported as passed in that configuration. Sensor cable disconnection is a different fault.
4. **Recovery logging:** a third early reconnection visibly recovered without a saved `technical_clear` event. Later runs recorded it successfully. USB/logging fixes were subsequently installed and passed continuity checks, but the earlier missing event's specific cause was not established.
5. **Sound requirement:** audible alerts were disabled at the user's request. The original ≤0.5-second button-to-silence requirement was not tested and must not be marked passed on the basis of permanently silent telemetry.
6. **Reference evidence:** stopwatch duration and normal-speed phone receipts are operator reported. Video IMG_1611 supports one filmed technical-alert arrival bound; it does not establish all notification conditions or multiple repeated latency trials.
7. **Rubric scope:** confirm required trial counts and drift duration against the final course requirements before declaring verification complete.

## Evidence index

- [Roll accuracy main table and all-attempt appendix](roll_accuracy_results.md)
- [Normal-speed two-hour timing review](normal_speed_two_hour_review.md)
- [One-phone filmed notification review](video_review_IMG_1611.md)
- [Earlier fault video review](video_review_IMG_1603.md)
- [Earlier notification video review](video_review_IMG_1608.md)
- Raw JSON files in this folder retain captured telemetry, event timing, original/repeat measurements and operator reports.

Original code and firmware backups are retained separately. Synced `sources/` reference files were not modified. Historical evidence has not been overwritten with improved repeats.

## Protocol video follow-up

See [IMG_1615 review](protocol_1615_review.md) for the complete step table, retained discrepancies, and proposed short targeted 40-degree right-turn check. Do not treat plan-based event ratios as independently validated sensitivity or specificity.

## Targeted right-turn follow-up

[IMG_1616 review](video_review_IMG_1616.md) documents interrupted handling followed by a recorded right/lateral turn at reported roll 40.1° and a timer reset to 119.9 seconds. The protractor baseline was hand-held, so an independently fixed 40-degree reference was not established. The follow-up supports functional turn recognition, not closure of the original protocol sensitivity finding.

## Operator clarification: interrupted protocol holds

Steps 3 and 11 are classified as invalid test executions based on the operator's later report of interrupted holds. Steps 4 and 12 are excluded as dependent return steps after qualifying lateral turns were not established. The four original no-event observations remain saved. Remaining positive planned-step coverage is 16/16, not validated sensitivity. Formal position agreement and sensitivity/specificity remain unissued; angle-reference and synchronization limitations remain.

## Conditional sensitivity estimate

Conditional observed sensitivity is 16/16 = 100% after the documented exclusions. The estimate assumes all 16 retained trials were true qualifying turns. This assumption remains unverified for every retained trial; the estimate is not an independently verified performance result and does not close the sensitivity requirement.
