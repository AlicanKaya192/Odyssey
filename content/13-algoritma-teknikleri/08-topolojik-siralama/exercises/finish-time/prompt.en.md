Write the function `finish_time(deps, hours)`: if jobs that do not wait for each
other can run at the same time, it returns after how many hours at the
earliest the whole pipeline finishes.

Get a topological order with the ready `course_order`; in order
`finish[job] = hours[job] + max(finish of the dependencies, or 0)`. The answer
is the largest finish.

**Expected output:**

```
18
5
```
