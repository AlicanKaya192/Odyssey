A server log wrote event times as Unix time. Because they come from
two services, some are in seconds and some in milliseconds:

```python
stamps = [1710000000, 1710003600123, 1710009000, 1710012345000]
```

**What to do:**

1. Look at each number: if it is larger than `1e12` it is in milliseconds,
   so divide it by `1000`.
2. Convert it to UTC time with `datetime.fromtimestamp(seconds, tz=timezone.utc)`.
3. Print each event as `"%Y-%m-%d %H:%M:%S"`, one per line.
4. Print the time between the first and the last event in **minutes** (one
   decimal).

**Expected output:**

```
2024-03-09 16:00:00
2024-03-09 17:00:00
2024-03-09 18:30:00
2024-03-09 19:25:45
205.8
```

Had you forgotten to divide, the millisecond rows would have gone tens of
thousands of years ahead and failed. Without `tz=timezone.utc` the same code
would print different times on another computer.
