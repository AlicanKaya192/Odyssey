Write the function `mask_emails(text)`: replace the part before `@` of
every e-mail address in the text with `***` and keep the domain:
`ada.l@example.com` → `***@example.com`. Use `re.sub` and `\1` in the new
text; the address pattern is `[\w.]+@([\w.]+)`.

**Expected output:**

```
Mail ***@example.com or ***@test.org now
```
