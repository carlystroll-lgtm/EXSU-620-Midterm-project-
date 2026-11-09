# Normal-speed two-hour alarm test

The saved run contains 7,266 normal-speed samples across approximately 2 hours 2 minutes 44 seconds. No missing source sequence numbers, restarts, sensor faults, upright samples, or host gaps over two seconds were observed. Maximum host sample gap was 1.056 seconds. Sound remained disabled.

| Alarm | Target after timer start | Recorded elapsed | Result against ±5 s |
|---|---|---|---|
| advisory | 6300 s | 6300.0 s | PASS |
| critical | 7200 s | 7200.0 s | PASS |

Timer origin was inferred from the first normal-speed uptime and remaining-time sample, with approximately 0.1-second remaining-time precision. An earlier demo advisory in the raw window is excluded by its scale=60 configuration; it is retained in raw evidence.

An acknowledgement event followed the normal-speed critical alert. This run supports the two-hour timing and sustained logging checks. The user confirmed that the phone received both alerts. This is functional receipt evidence; exact arrival latency was not independently recorded. Stillness-based detachment detection is disabled in the deployed configuration; this test does not establish that behavior.

Raw evidence: [normal_run_result_20261108_004933.json](normal_run_result_20261108_004933.json).
