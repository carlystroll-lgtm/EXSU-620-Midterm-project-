# Audible alarm / button test — IMG_1619.mov

Original: `/Users/kyri/Desktop/IMG_1619.mov`. Encoded playback duration 64.733 seconds, 30 fps, with a usable mono audio track decoded locally at 48 kHz. Original unchanged. The clip appears slow-motion processed: critical tones have an approximately 300 Hz fundamental and pulse durations around 0.62-0.83 playback seconds, versus the firmware's nominal 1,200 Hz critical signal. Exact original-speed timing cannot be reconstructed from nominal 30 fps alone. Container track edit mappings are 1:1, so the original capture/slow-motion factor is not directly established from those mappings.

## Supported observations

- Audible alarm output is present.
- The audio contains ten clearly separated tonal pulses from approximately 49.00 to 59.26 playback seconds, consistent with a ten-pulse critical pattern slowed in playback.
- The button and approaching hand are visible near the end. Finger contact/approach begins earlier, but clear depression/actuation is not independently timestamped. The stronger visible depression occurs near 62 playback seconds, after the ten-pulse burst has ended.
- The ring subsequently appears steady red. An archived server record contains `ack` and `press: critical`, with `sound=false` and `acked=true` in the same emitted message at Mac time 16:32:57.003. The critical event was at 16:32:52.747. Camera and Mac clocks were not independently synchronized, and slow-motion processing prevents a simple direct wall-clock/video-time subtraction.

## Acoustic analysis

The extracted waveform was analyzed with 40 ms Hann FFT windows, 5 ms hops and a 270-330 Hz band-amplitude threshold of 0.001. Ten pulse segments were found; the last above-threshold segment ended near 59.255 playback seconds. This is a signal-analysis boundary, not a calibrated sound-pressure measurement. Room reverberation, microphone behavior, threshold choice and audio/video synchronization contribute uncertainty.

## Disposition

**Sound output and a ten-pulse alarm sequence are demonstrated.** The logged acknowledgement and sound-state change support functional button response.

**The <=0.5-second physical-button-to-acoustic-silence latency is not established by this clip.** Ten complete pulses occur before the clearest button depression, so acoustic cessation may be the natural end of the burst. Finger contact alone does not establish electrical switch closure. This is an inconclusive latency trial, not evidence of a failed button or speaker.

For a short repeat, use normal video with audio at 60 fps if available. Frame the red button from a side angle so its travel is visible. Press firmly during the first or second audible pulse, rather than after the burst. Retain the whole clip. If using slow motion, preserve the known recording/playback rate and avoid ambiguous edited speed ramps. Repeat trials should retain all observations.

Separate operator statement: sound output, all three alarm patterns and button silencing were tested and confirmed outside the earlier silent logging runs. This is operator-reported functional evidence; this clip independently demonstrates only the audible sequence visible/heard here, not every alarm type or numerical silence latency.

Supporting files: `video_1619_audio_metadata.json`, `video_1619_tone_segments.json`, `video_1619_log_evidence.json`, waveform plots and timed frame directories. No token or chat identifier was extracted for this review.
