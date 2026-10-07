`/offset/books` pages with an offset and a limit. The response looks like
`{"items": [...], "offset": .., "limit": .., "total": ..}`.

**What to do:**

1. With `limit=8`, starting from `offset=0`, collect all books into an
   `items` list. After each request increase `offset` by `limit`; stop when
   `offset >= total`.
2. Print each requested offset and how many books came with that request;
   at the end print the total.

**Expected output:**

```
offset 0 -> 8 books
offset 8 -> 8 books
offset 16 -> 7 books
total: 23
```
