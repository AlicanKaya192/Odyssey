Availability promises are named by their "nines": 99.9% is "three nines",
99.99% is "four nines". The table below was computed with Python; a year is
365 days and a month is 30 days.

| Promise | Per year (minutes) | Per month (minutes) | Per week (minutes) |
|---|---|---|---|
| 99% | 5256.0 | 432.0 | 100.8 |
| 99.5% | 2628.0 | 216.0 | 50.4 |
| 99.9% | 525.6 | 43.2 | 10.1 |
| 99.95% | 262.8 | 21.6 | 5.0 |
| 99.99% | 52.6 | 4.3 | 1.0 |
| 99.999% | 5.3 | 0.4 | 0.1 |

## How is it computed?

The allowed downtime is the "not up" share of the total time:

```python
def allowed_minutes(percent, days):
    return days * 24 * 60 * (1 - percent / 100)


print(round(allowed_minutes(99.9, 30), 1))
```

```text
43.2
```

The other way round, the availability actually reached is the time up
divided by the total time:

```python
total = 30 * 24 * 60
down = 12 + 30
print(round((total - down) / total * 100, 3))
```

```text
99.903
```

A service that was down for 42 minutes in a month only just kept its 99.9%
promise: the allowance for that month was 43.2 minutes, and the result was
99.903%, just above the target. One more outage and the promise would have
been broken.

## Watch out

- The percentages look close; do not compare them without turning them
  into minutes.
- Whether "planned maintenance" counts is written into the agreement from
  the start.
- More nines means more machines, more people and more money. Not every
  service needs five nines.
