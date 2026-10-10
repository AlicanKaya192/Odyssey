`download_all(count, limit)` starts `count` downloads together with `gather`
and returns `[number of downloads, most downloads running at once]`. Right
now they all run at the same time. Create an `asyncio.Semaphore(limit)` in
`download_all` and put the work in `download` inside an `async with gate:`
block; the peak must not exceed `limit`.

**Expected output:**

```
[10, 3]
```
