Write the function `finish_time(job, needs, minutes)`. It should return how many minutes after the pipeline starts `job` finishes:

- A job that waits for nothing starts at minute 0.
- A job starts when the **latest** of the jobs it waits for finishes.
- Finish = start + its own duration (`minutes[job]`).

You can compute the finishing time of the awaited jobs with the same function (recursion).

**Expected output:**

```
lint 2
test 5
build 8
deploy 9
```
