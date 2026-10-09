Write the function `run_order(tasks)`: `tasks` is a list of `[priority, name]`
pairs. A smaller number means **higher priority**. It returns the tasks'
**names** in the order they will run; those with **equal** priority run **in
order of arrival** in the list.

Put `(priority, number, name)` tuples in the heap; `enumerate` is enough for
`number`. No `sorted` and no `sort`.

**Expected output:**

```
bugfix
deploy
tests
review
docs
```
