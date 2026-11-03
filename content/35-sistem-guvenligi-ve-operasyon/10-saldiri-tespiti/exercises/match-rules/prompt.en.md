`rules` is rule name → regular expression text. `match_rules(lines, rules)`
should try every line against every rule with `re.search` and return
`"<line no>: <rule>"` for the matches; lines are counted from 1, and within
a line the rules are in alphabetical order by name. The starter code
searches for the pattern as plain text; it must be tried as a regular
expression.

**Expected output:**

```
2: path traversal
3: path traversal
3: script tag
```
