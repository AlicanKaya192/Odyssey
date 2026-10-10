Write the function `square_all(numbers, n_workers)`:

- Create a `tasks` and a `results` queue (`queue.Queue`).
- Start `n_workers` threads; each worker takes from `tasks`, leaves when it
  sees `STOP`, otherwise puts the square of the number into `results`.
- Put the numbers in the queue, then one `STOP` per worker, and `join` the
  workers.
- Return the squares as a **sorted** list.

**Expected output:**

```
[1, 4, 9]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
