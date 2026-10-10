`fetch_all(names)` fetches each name one after another with
`await fetch(name)`; five names take 1 second. Make them wait together with
`asyncio.gather`; the results must still be a list **in name order**. Do not
change the `run_fetch_all` wrapper below. The expected output:

```
[1, 2, 3, 4, 1]
True
```

**Expected output:**

```
[1, 2, 3, 4, 1]
True
```
