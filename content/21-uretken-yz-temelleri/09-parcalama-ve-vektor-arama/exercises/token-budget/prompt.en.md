`fit_chunks(chunks, budget)` should walk the ranked chunk list from the
start and take chunks while the total by `count_tokens` (read-only
`llm_client.py`) does not exceed `budget`; it stops at the first chunk that
would. Return `[number of chunks taken, total tokens]`.

**Expected output:**

```
[1, 11]
[3, 28]
```
