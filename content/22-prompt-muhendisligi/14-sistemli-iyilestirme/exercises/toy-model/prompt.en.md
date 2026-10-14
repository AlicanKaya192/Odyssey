`toy_model(prompt, text)` should write the one from the lesson: put the
lower-case words of the text (`[a-z]+`) into a set. For every
`- label: w1, w2` line of the prompt, count how many of the listed words
appear in the text. Return the category with the most; on a tie the one
that comes first, and `"unknown"` if none appears.

**Expected output:**

```
shipping
returns
unknown
```
