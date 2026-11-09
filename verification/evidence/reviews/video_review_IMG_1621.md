# Audible acknowledgement follow-up — IMG_1621.mov

Original: `/Users/kyri/Desktop/IMG_1621.mov`. Duration 34.995 seconds, approximately 29.98 fps; usable 48 kHz audio. Normal-speed-looking pulse frequency and spacing, unlike the preceding slowed clip. Original unchanged.

The operator clarified that the second button press was firm. The second action is therefore the intended test action; the earlier touch is retained rather than treated as an equivalent successful trial.

## Confirmed functional evidence

- An advisory-style three-pulse sequence is present near 11 seconds, with energy around 880 Hz.
- A first critical burst contains ten pulses near 25.88–28.57 seconds.
- The next critical burst starts near 30.94 seconds and contains eight audible pulses, ending near 33.15–33.17 seconds depending on the analysis threshold. The remaining pulses are suppressed.
- The second, firmer button action is visible near the end. A white acknowledgement flash begins at approximately 33.193–33.227 seconds, followed by steady red indication. Exact electrical switch closure is obscured by the thumb; the flash is firmware acknowledgement, not independent physical contact timing.
- The server records `ack` and `press: critical` together, with `sound=false`, at Mac time 16:47:16.388 (source uptime 1246.966 s). The critical onset was 16:47:09.086. The clock relationship to the video is not independently calibrated.

**Finding: the second press successfully acknowledges and silences the critical alarm sequence.** The operator does not need to repeat the test to establish this functional behavior.

## Numerical latency limitation

The last tone ends approximately 0.02–0.08 seconds before the first acknowledgement-flash frame, depending on audio threshold and selected flash frame. Its duration is similar to preceding full tones. The video therefore does not unambiguously show an active tone being cut off after a separately resolved electrical switch closure. It may show acknowledgement during the short gap between tones, with subsequent pulses suppressed.

No exact positive button-to-acoustic-cessation latency is assigned, and the <=0.5-second timing criterion is not marked numerically verified from this clip alone. This is a measurement-boundary limitation, not evidence of slow silencing or a failed button. A near-coincident flash and acoustic ending must not be reported as a precise zero-latency measurement.

For strict timed verification, press during the first or second audible tone in the burst and frame the button travel clearly. If a repeat is not pursued, retain the functional pass and explicitly state that the numerical <=0.5-second limit was not independently measured.

## Method and scope

Acoustic segments were identified using 20 ms Hann FFT windows, 2.5 ms hop, a 1120–1280 Hz band, and an analysis-specific amplitude threshold. The final tone ends at 33.1725, 33.1625 and 33.1475 seconds for thresholds 0.001, 0.002 and 0.004. This threshold sweep is not a calibrated sound-level measurement. Frame quantization is about 33 ms; audio/video synchronization and physical switch closure add uncertainty.

The clip independently supports advisory/critical output and critical acknowledgement. Separate operator-reported tests support all three patterns, including technical. The technical pattern is not independently tested in this clip.

Supporting records: `video_1621_audio_metadata.json`, `video_1621_tone_segments.json`, `video_1621_log_evidence.json`, audio plots, and the timed full/press frame directories.
