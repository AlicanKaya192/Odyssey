There is an `app.log` next to your file; the lines look like
`2026-03-15 10:02:11 ERROR [db] message`, with a broken line among them.
Write the function `log_levels(path)`: read the file with `pathlib`, parse
each line with `re.fullmatch` (pattern: `\S+ \S+ (\w+) \[\w+\] .+`), count
the levels of the matching lines with `Counter` and return a dictionary. Skip
lines that do not match.

**Expected output:**

```
ERROR 2
INFO 2
WARNING 1
```
