`parallel_sum(list, parts)`: split the list into `parts` parts, add each part in its own branch, and add to a shared total. Use `thread::scope` and `Mutex`. An empty list gives `0`.
