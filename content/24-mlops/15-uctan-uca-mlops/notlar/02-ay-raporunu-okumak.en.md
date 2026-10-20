The line the pipeline writes every month is a decision; every decision has
a next step.

## The lesson's eight months

| Month | Drift | Accuracy | Decision |
|---|---|---|---|
| 1 | 0.070 | 0.813 | keep |
| 3 | 0.578 | 0.778 | v2 promoted (0.782) |
| 4 | 0.326 | 0.787 | candidate kept out (0.784) |
| 5 | 0.575 | 0.691 | data rejected (100% invalid) |
| 6 | 0.922 | 0.697 | v3 promoted (0.837) |
| 7 | 0.127 | 0.821 | keep |

## After each decision

| Decision | What is done |
|---|---|
| `keep` | Nothing; keep monitoring |
| `promoted` | The new version goes through shadow and canary; the old version stays in the registry for rolling back |
| `kept out` | The candidate's measurement goes into the registry; if the drift continues, the window size is reconsidered |
| `data rejected` | An alert; the data source is fixed, and the pipeline is run again by hand |

## Can broken data pass the gate?

| Where the candidate was measured | Accuracy |
|---|---|
| On a set from the same broken source | 0.784 |
| On clean data after the source was fixed | 0.673 |

If the gate's set is broken too, the candidate passes the gate; that's
why validation comes before the gate.

## Don't

- Don't leave a `data rejected` line silent; the model stays old for
  another month.
- Don't mistake a `kept out` line for an error; the gate did its job.
