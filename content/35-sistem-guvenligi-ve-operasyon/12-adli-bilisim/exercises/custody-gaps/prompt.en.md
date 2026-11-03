Each handover is `[time, giver, taker]`. If a handover's giver is not
the **taker** of the previous handover, there is a gap in the chain.
`custody_gaps(entries)` should return the times of the handovers with a
gap, in order. No gap is looked for before the first handover.

**Expected output:**

```
['17:00', '19:00']
```
