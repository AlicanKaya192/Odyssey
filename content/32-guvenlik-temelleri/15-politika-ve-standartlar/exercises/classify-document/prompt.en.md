`LEVELS` keeps the levels ordered from low to high. `keywords` maps a
level to a list of keywords.

`classify_document(text, keywords)` should return the **highest** level
whose keyword appears in the text (case does not matter); `"public"` if
none appears.

**Expected output:**

```
public
internal
restricted
confidential
```
