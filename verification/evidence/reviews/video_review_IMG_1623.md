# IMG_1623: button silencing timing review

Original: /Users/kyri/Desktop/IMG_1623.mov, 31.265 s, approximately 30 frames/s. Original unchanged.

The button cap and final inward thumb movement are more clearly visible than in the preceding clips. The final depression occurs approximately 29.80–29.90 s, with the first white acknowledgement frame at 29.898 s. A critical alarm burst is active: tones start near 29.155, 29.455 and 29.753 s, then the remaining burst is suppressed. The final tone and its decay end by approximately 29.915–30.035 s depending on the analysis threshold. Allowing for the visible depression bracket, quiet decay and frame quantization, the observed response is conservatively approximately 0.3 s or less.

Result: this single filmed trial supports the <=0.5 s button-silencing criterion. This is a conservative video-based estimate, not a precise electrical switch latency or a statistical repeatability demonstration. Initial thumb contact/resting pressure is not substituted for the later visible firm depression. Previous clips remain functional evidence without a numerical timing result.

Audio method: 20 ms Hann FFT, 2.5 ms hop, 1120–1280 Hz band, thresholds 0.001/0.002/0.004. The lower threshold includes room decay/background and therefore provides a conservative acoustic ending. No calibrated sound-level claim. Video/audio synchronization is assumed as recorded in the same original file; no external clock subtraction used.

Evidence: video_1623_latency_result.json, video_1623_tone_segments.json, video_1623_audio_metadata.json, video_1623_press_contact.jpg, extracted frames and original video. Technical alarm pattern and all-pattern repeatability are not established by this clip.
