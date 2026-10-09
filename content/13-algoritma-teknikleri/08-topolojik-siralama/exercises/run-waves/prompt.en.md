Write the function `waves(deps)`: it returns the jobs in **waves**: the first
wave is those waiting for nothing, the next wave those that wait only for
earlier waves. Each wave is an alphabetically sorted list.

Run Kahn round by round: all jobs whose waiting count is zero right now form
a wave; then decrease the counters of the jobs behind them. No `graphlib`.

**Expected output:**

```
['extract']
['clean', 'validate']
['features']
['train']
['evaluate']
['report']
```
