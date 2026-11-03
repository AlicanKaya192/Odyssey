`redact(text)` should find every email address in the text with
`PATTERN` and turn it into the form `"a***@example.org"`; the domain (what
comes after `@`) is kept so the report still says which system is
affected. `re.sub` can be given a function instead of text: it takes the
match and returns the text to put in its place.

**Expected output:**

```
Owner: a***@example.org
Seen: b***@example.org, x***@y.org
No address here.
```
