`parse_json(text)` should try three ways in order, as in the lesson: the
text itself, the text with the code block marks removed
(`` re.sub(r"^`{3}(?:json)?\s*|\s*`{3}$", "", text.strip()) ``) and the part
between the first `{` and the last `}`. Return the first one that works
as `[data, name of the way]` (names `"as is"`, `"fence"`, `"braces"`); if
none works, `[None, "failed"]`.

**Expected output:**

```
[{'a': 1}, 'as is']
[{'a': 2}, 'fence']
[{'a': 3}, 'braces']
[None, 'failed']
```
