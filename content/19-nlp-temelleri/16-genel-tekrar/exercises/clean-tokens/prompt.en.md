`clean_tokens(text)` should, in order:

1. unescape HTML entities (`html.unescape`),
2. replace tags (`<...>`) with a space,
3. lowercase and split with `re.findall(r"[a-z']+", ...)`,
4. drop the words in the `STOP` set.

"not" is not in the stop list: it is kept for sentiment.

**Expected output:**

```
['lid', 'not', 'tight', 'leaks']
```
