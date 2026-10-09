Write the function `course_order(deps)` with **Kahn's** algorithm: `deps` is
`{job: [jobs it waits for]}`. It returns a topological order; on a tie take the
one first **alphabetically** (a heap). `None` if there is a cycle.

`all_nodes` is ready: the jobs in both the keys and the values.

**Expected output:**

```
extract
clean
validate
features
train
evaluate
report
None
```
