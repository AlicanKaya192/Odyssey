Write the function `has_cycle(deps)`: it returns `True` if the dependencies
contain a **directed cycle**.

Kahn's counter method is an easy way: if the number of jobs that can be taken
in order is below the number of all jobs, there is a cycle. On the
50,000-job chain on the last line, recursive DFS hits the depth limit.

**Expected output:**

```
False
True
False True
```
