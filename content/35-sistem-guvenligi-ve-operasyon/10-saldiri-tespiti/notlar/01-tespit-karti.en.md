## Two methods

| | Signature-based | Anomaly-based |
|---|---|---|
| What does it look at? | Known attack patterns | Deviation from normal |
| A new attack | Misses it | Can catch it |
| False alarms | Few | Many |
| Maintenance | Updating signatures | Recalculating the baseline |

## The outcome table

| | Really an attack | Not an attack |
|---|---|---|
| **Alert** | True positive (TP) | False positive (FP), a false alarm |
| **No alert** | False negative (FN), a miss | True negative (TN) |

- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)

## Python patterns

- A signature: `re.compile(pattern, re.IGNORECASE).search(line)`.
- Mean and deviation: `statistics.mean`, `statistics.stdev`.
- The z-score: `(value - mean) / stdev`; `abs(z) > 3` is a common threshold.
- Set operations: `alerts & attacks` (TP), `alerts - attacks` (FP),
  `attacks - alerts` (FN).
- Counting by key: `Counter()` and an `(ip, user)` tuple.

## Keep in mind

- Signatures find the known, anomalies find the unusual; both are used
  together.
- Before dividing, check whether the denominator is zero: with no alerts at
  all, precision is undefined.
- Because attacks are rare, even a small false alarm rate means many empty
  alerts.
- Look at patterns rather than single events: a success that follows
  failures.
- Documentation uses ranges reserved for example IPs:
  `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.
