A task took `200000` seconds. Split it into days, hours, minutes and
seconds:

```
2 days 7 hours 33 minutes 20 seconds
```

Use four variables: `days`, `hours`, `minutes`, `seconds`.

It is done with `//` (whole division) and `%` (remainder) only. A day is
`24 * 60 * 60 = 86400` seconds, an hour `3600` seconds, a minute `60`
seconds.

The way to go: first find how many **whole days** fit. Once the days are
taken out, find how many whole hours fit in the seconds left over (the
remainder!). Do the same for minutes; whatever is left at the end is the
seconds.

> Watch out: `hours` is not all the hours in the total (that would be
> 55), but the hours **left over** after the days. At every step, work
> with the remainder of the previous one.
