Run a function that imitates fetching pages from a website with a thread
pool.

**What to do:**

1. Write the function `fetch(page)`: it waits with `time.sleep(0.1)` and
   returns `page * 10` (think of it as the number of products on the page).
2. With `ThreadPoolExecutor(max_workers=8)` run `fetch` for pages 1 to 8
   (`ex.map`) and take the results into a list.
3. Print the list and its total on separate lines.

**Expected output:**

```
[10, 20, 30, 40, 50, 60, 70, 80]
360
```

Since the eight waits happen at the same time, the job takes about 0.1
seconds; sequentially it would take 0.8 seconds.
