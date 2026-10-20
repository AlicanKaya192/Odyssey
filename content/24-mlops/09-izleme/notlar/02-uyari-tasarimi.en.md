A good alert rarely goes off, but when it does it is worth looking at.

## Rules

- Every alert should have an **owner**: who will look?
- Every alert should state **what to do** (a short instruction).
- It should go off not on a single crossing but on **several crossings in
  a row** (`patience`).
- The threshold should be wider than the measure's normal wobble: first
  watch for a few weeks, then set the threshold.
- One alert for one problem: one problem shouldn't produce ten alerts.
- The quality alert (accuracy) arrives late; at least one of the early
  signals (input, predicted rate) should go with it.

## Alert or information?

| Situation | Alert (someone must look now) | Information on the dashboard |
|---|---|---|
| The error rate suddenly at 10% | Yes | |
| p95 latency went up a little | | Yes |
| The predicted rate has been drifting for two months | Yes | |
| The predicted rate a little different for one day | | Yes |
| Accuracy below the threshold | Yes | |

## Don't

- Don't put an alert on every measure; the more alerts there are, the less
  attention each one gets.
- Before tying alerts to automatic retraining, measure how often they go
  off wrongly.
- Don't read a rising predicted rate alone as "the model broke"; the
  customers may really have changed.
