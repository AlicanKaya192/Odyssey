`unpinned(lines)` should return, in line order, the names of the packages
in the lines of a `requirements.txt` that are **not pinned to an exact
version** (do not contain `==`). Blank lines and comments (everything after
`#`) are skipped. The name is the part up to the first `<`, `>`, `=`, `!`,
`~`, space, `;` or `[` character: `re.split(r"[<>=!~ ;\[]", line)[0]`.

**Expected output:**

```
['pandas', 'flask', 'httpkit']
```
