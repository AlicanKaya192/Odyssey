`ask_checked(script, max_tries)` should ask `MESSAGES` with
`ChatClient(script)` at most `max_tries` times (`max_tokens=120`,
`temperature=0.7`). Parse each answer's last line with the given
`final_answer` and compare it with the given `order_total(ITEMS, 0.10)`.
If they are equal return `[amount, which attempt]`; if none matches,
`[None, max_tries]`.

**Expected output:**

```
[193.41, 3]
[None, 2]
```
