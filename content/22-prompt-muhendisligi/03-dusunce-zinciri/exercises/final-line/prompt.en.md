`final_answer(text)` should find the line `Answer: <number>` standing on
its own and return the number as a `float`; `None` if the line is missing
or has anything besides the number. There may be spaces around it:
`re.search(r"^Answer:\s*(\d+(?:\.\d+)?)\s*$", text, flags=re.M)`.

**Expected output:**

```
5.0
12.5
None
```
