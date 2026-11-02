Every finding is a dictionary: `name`, `score` (CVSS), `exposed` (is it
open to the internet) and `patched` (has the patch been applied).

Write the function `needs_action(findings, threshold)`: return the names
of the findings that are **not** patched and whose score is equal to or
greater than `threshold`. Order:

1. the ones open to the internet first,
2. within the same group, the higher score first,
3. if the scores are equal too, alphabetical by name.

**Expected output:**

```
threshold 7.0
  api server
  web login
  old library
threshold 4.0
  api server
  web login
  old library
  test box
```
