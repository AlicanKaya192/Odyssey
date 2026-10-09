Write the function `max_meetings(meetings)`: it returns the largest number of
meetings that fit into one room. Each meeting is `[start, end]`; a meeting may
start at the moment another ends.

**Earliest end first:** sort by end, keep the end of the last one chosen, take
the ones that do not start before it.

The 200,000 requests on the last line make a solution that compares each new
meeting with every chosen one hit the time limit.

**Expected output:**

```
3
2
8201
```
