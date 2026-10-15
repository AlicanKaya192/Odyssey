Write the function `critical_path(jobs)`. `jobs` is a dictionary: job name → `[minutes, jobs it depends on]`. A job waits for the latest of the jobs it depends on.

Return `[total time, path]`:

- Total time: the finish minute of the job that finishes last.
- Path: from that job backwards, at each step choosing the **latest finishing** of the jobs it depends on, the job names in order from start to end.
- On a tie, the one that comes first in the dictionary (or the `needs` list) is chosen; `max(..., key=...)` already does that.

**Expected output:**

```
[6, ['lint', 'test', 'build']]
[8, ['docs', 'build']]
```
