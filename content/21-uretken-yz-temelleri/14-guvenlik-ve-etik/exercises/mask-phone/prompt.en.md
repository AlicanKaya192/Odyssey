The lesson's masker left the first bracket outside for the form
`(555) 123-4567`. `mask(text)` should replace emails, phone numbers and order
numbers with `[EMAIL]`, `[PHONE]`, `[ORDER]` as in the lesson; but the phone
pattern should also cover an optional leading `(`:
`r"\+?\(?\d[\d\s()-]{8,}\d"`.

**Expected output:**

```
My number is [PHONE].
Mail [EMAIL]
Order [ORDER]
```
