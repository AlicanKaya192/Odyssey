`budget_stop(trace, budget)` should add up the rounds' input tokens in
order. At the first round where the total exceeds `budget`, return
`[the total at that point, round number]` (rounds count from 1); if it
never exceeds it, `[total, 0]`.

**Expected output:**

```
[365, 4]
[246, 0]
```
