Each task is a dict: `name`, `runs_as`, the script's owner `owner` and
its permission `mode`. `risky_tasks(tasks)` should return, in alphabetical
order, the names of tasks that run as `root` and whose script either does
not belong to `root` or can be written by the group or others
(`mode & 0o022`).

**Expected output:**

```
['audit', 'cleanup', 'report']
```
