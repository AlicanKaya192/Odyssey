`fake_fetch(url)` waits 0.3 seconds on every call. Because `fetch_all(urls)`
fetches the addresses one after another, 10 addresses take 3 seconds. Rewrite
the function with `ThreadPoolExecutor(max_workers=10)` and `pool.map`; the
results must still be a list **in address order**. The expected output:

```
[22, 22, 22, 22, 22, 22, 22, 22, 22, 22]
True
```

**Expected output:**

```
[22, 22, 22, 22, 22, 22, 22, 22, 22, 22]
True
```
