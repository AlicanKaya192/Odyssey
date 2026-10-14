`count(text)` should write the section's simplified counter: split the text
into pieces with `re.findall(r"\w+|[^\w\s]", text)`; every punctuation mark
is 1 token, every word is 1 token for every started group of four characters
(`"cat"` 1, `"capital"` 2). Return the total as an `int`.

**Expected output:**

```
1 2 6
```
