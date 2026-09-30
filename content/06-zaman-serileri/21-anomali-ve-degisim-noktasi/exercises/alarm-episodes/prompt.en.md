Turn the twelve alarms into events: join alarms that are close to each other
and name each event by its direction and length.

In the starter code `deviation` (the relative deviation) and `alarm`
(true/false) are ready.

**What to do:**

1. Take the alarm days: `days = alarm[alarm].index`.
2. Split the days into events: an alarm belongs to the same event if it is
   **at most 3 days** after the previous one; otherwise a new event starts.
   Each event is a list of days.
3. Print one line per event:
   - the first and the last day (`"%m-%d"`)
   - the number of alarms
   - the direction: `up` if all the deviations are positive, `down` if all are
     negative, otherwise `mixed`
   - the kind: `shift` if there are 3 or more alarms, otherwise `spike`

**Expected output:**

```
03-14 03-14 1 up spike
06-20 06-20 1 up spike
09-02 09-14 9 up shift
10-08 10-08 1 down spike
```

Twelve alarms came down to four events. Three are one-day jumps; one is a run
of nine alarms all in the same direction: a level shift. On a monitoring
screen these four lines are shown instead of twelve separate notifications.
