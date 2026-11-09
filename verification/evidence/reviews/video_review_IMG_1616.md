# Targeted right-turn follow-up — IMG_1616.mov

Source: `/Users/kyri/Downloads/IMG_1616.mov`, 92.808 seconds, approximately 29.98 frames/second. Creation-time metadata: November 8, 2026, 15:47:41 America/Toronto. Original video unchanged. Review included a timed whole-clip storyboard and full-resolution reference views at 35, 50, 60, 75 and 90 seconds. No synchronized button marker or independently verified camera-to-server clock alignment was available, so wall-clock metadata is used only to associate the clip with the corresponding saved test.

## Visible observations

The sensor initially rests on the table. The operator lifts and adjusts it against a hand-held protractor/ruler assembly. Both the sensor and reference are repositioned repeatedly early in the clip; the later views show a steadier inclined hold. At the end the sensor is returned to the table.

The protractor body and baseline are held in the operator's hand rather than secured level to the tabletop. The reference markings are partly obscured, and the camera views the assembly obliquely. Consequently the clip does not independently establish an absolute 40-degree roll relative to gravity. A protractor reading between its arms is not an absolute tilt reference unless its zero arm is constrained to the independently known level surface.

## Corresponding saved sensor evidence

- Baseline: reported roll −0.1°, pitch −2.0°, supine; prior turn anchor +3.3°.
- The initial candidate hold did not complete. A `partial` event reported 3 seconds; reported roll fell to 28.2° and later 19.9°. Pitch was around −27 to −29° during that part of the motion.
- A later candidate hold accumulated from approximately 1.0 to 14.4 seconds in the saved telemetry, followed by a `turn: lateral` event at source uptime **3833.996 s**, Mac time **15:48:40.927**.
- At that turn: reported roll **40.1°**, pitch **−6.9°**, anchor updated to **40.1°**, remaining timer **119.9 seconds**.
- The critical state remained latched in those samples. This log supports a turn/reset event, not a claim that an unacknowledged critical indication cleared.

The repeated handling visible on video is consistent with the interrupted candidate and subsequent successful hold. It does not independently prove that every threshold crossing was physically correct, and the recorded device angle cannot serve as its own reference truth.

## Conclusion

**Functional right-turn recognition and timer reset are demonstrated.** The later continuous qualifying hold generated a lateral-turn event; the earlier interrupted hold did not.

**Independent exact-angle validation and the cause of the earlier protocol misses remain unresolved.** This later success does not retroactively replace or invalidate the four missing planned-turn events in IMG_1615. It should be retained as a separate diagnostic follow-up, not counted as extra true positives in the original protocol.

If an exact-angle retest is needed, secure the protractor's zero arm against a level tabletop or use an independently checked fixed wedge. Support the sensor plate flush against the 40-degree face, keep the sensor's roll axis identified and pitch near zero, and film the reference face, board and time reference together. Verify the physical reference before relying on the device display.

Evidence: `right40_targeted_baseline_20261108_154755.json`, `right40_targeted_result_20261108_154838.json`, and frames in `video_1616_frames/`.
