`clean_html(text)` should do three things: decode HTML entities with
`html.unescape`, turn tags into spaces with `re.sub(r"<[^>]+>", " ", text)`
and finally collapse the spaces into one (`" ".join(text.split())`).

**Expected output:**

```
Great & cheap
Fast delivery, well packed
5 < 7
```
