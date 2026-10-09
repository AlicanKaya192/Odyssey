Write the function `error_counts(log)`: `log` is a multi-line text whose
every line is `date time LEVEL message`. Count the messages of the lines
whose level is `ERROR` and return a `{message: count}` dictionary. The
pattern, with `re.MULTILINE`: `^\S+ \S+ ERROR (.+)$`.

**Expected output:**

```
{'disk full': 2, 'timeout': 1}
```
