`files` is a dictionary mapping file names to their contents. Write the function `find_secrets(files)`; it should find secrets written in the code and return a list of lines in this form:

- `"name:line: api-key"`: if the line has the `API_KEY` pattern.
- `"name:line: password"`: if the line has the `PASSWORD` pattern.

The files are visited **sorted** by name, lines are counted from 1. If a line has both, `api-key` comes first. The patterns are ready; `PATTERN.search(line)` counts as true when it finds a match.

**Expected output:**

```
old_config.py:1: api-key
settings.py:2: password
```
