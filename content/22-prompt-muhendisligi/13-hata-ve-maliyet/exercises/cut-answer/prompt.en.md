`ask(reply, max_tokens, tries)` should send `MESSAGES` with
`ChatClient([reply] * tries)`. If the answer is cut with `"length"`, it
should double `max_tokens` and ask again, at most `tries` calls. It should
add up the paid tokens and return `[text, input, output]`; if it never
fits, the text is `None`.

**Expected output:**

```
4 True 39 26
20 True 13 15
2 False 26 5
```
