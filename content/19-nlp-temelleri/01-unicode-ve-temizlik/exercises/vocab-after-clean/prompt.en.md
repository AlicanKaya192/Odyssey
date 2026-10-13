In the starter code `vocabulary` and `vocab_sizes` are ready; `clean` returns
the text unchanged. `clean(text)` should apply the lesson's cleaning pipeline
in order:

1. `html.unescape`
2. turn tags into spaces: `re.sub(r"<[^>]+>", " ", text)`
3. `unicodedata.normalize("NFKC", text)`
4. straighten the quotes: `text.translate(QUOTES)`
5. remove the zero-width space: `chr(0x200B)`
6. collapse the spaces into one

The output is the number of words `[before cleaning, after cleaning]`.

**Expected output:**

```
[2225, 362]
```
