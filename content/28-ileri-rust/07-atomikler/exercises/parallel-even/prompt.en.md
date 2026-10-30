`count_even(list)`: count the evens. Split the list with `chunks(2)`, and each part does `fetch_add(1, Ordering::Relaxed)` in a branch. Do not use `Mutex`.
