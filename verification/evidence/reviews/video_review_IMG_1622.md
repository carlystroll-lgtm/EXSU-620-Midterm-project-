# IMG_1622: active-alarm acknowledgement review

Source: /Users/kyri/Desktop/IMG_1622.mov. Duration 37.43 s, approximately 30 frames/s, audio analysed at 48 kHz. Original retained unchanged.

The clip confirms critical audible output and successful button acknowledgement while the critical burst is in progress. The first critical burst contains ten tones. The following burst starts near 34.025 s and stops after its fourth tone, with the remaining pulses suppressed. The fourth tone is shortened: approximately 34.878–34.985 s at the higher analysis threshold (0.108 s), compared with preceding tones of approximately 0.16–0.21 s. Including the quieter acoustic decay gives a final ending near 35.05 s. This is stronger evidence of interruption of an active burst than IMG_1621.

The matching server record contains acknowledgement and critical press events at source uptime 1477.589 s, with sound=false and acked=true (Mac 16:51:07.011). Earlier critical onset is at source uptime 1471.542 s. The video creation timestamp and Mac event are consistent with the acoustic ending near 35 s, but these clocks were not independently synchronized.

Result: functional critical-alarm silencing confirmed. No further recording is needed to demonstrate that function. The thumb obscures exact switch closure, so no precise physical-press-to-silence latency or independent numerical <=0.5 s pass is assigned. The short final tone and suppressed remainder support prompt operation, without establishing the exact timing origin. This limitation concerns measurement precision, not an observed slow response.

Method: 20 ms Hann FFT windows with 2.5 ms hop, 1120–1280 Hz tone band, threshold sweep 0.001/0.002/0.004; visual inspection of extracted frames around 33.8–35.5 s. Thresholds are analysis-specific, not calibrated sound levels. This clip does not independently establish all three alarm patterns or repeatability.

Supporting files: video_1622_audio_metadata.json, video_1622_tone_segments.json, video_1622_log_evidence.json, video_1622_press_contact.jpg, video_1622_audio_overview.png, and extracted frame directories.
