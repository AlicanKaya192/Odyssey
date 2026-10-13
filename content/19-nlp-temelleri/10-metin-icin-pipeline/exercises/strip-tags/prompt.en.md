- `strip_tags(text)`: replace HTML tags (`<...>`) with a space, collapse extra
  spaces into one and turn the text **lowercase**. Given as a `preprocessor`,
  the vectoriser does no lowercasing; that is your job.
- `vocab_has(word, preprocessor)`: build
  `TfidfVectorizer(preprocessor=preprocessor)` on the messy reviews and return
  whether `word` is in the vocabulary.

**Expected output:**

```
good value works
True
False
```
