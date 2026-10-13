`evaluate(preprocessor)` should build a Pipeline from
`TfidfVectorizer(preprocessor=preprocessor)` and `LinearSVC()`, train it on the
training data and return `[vocabulary size, test macro F1]` (F1 with 3
places).

**Expected output:**

```
[1210, 0.931]
[347, 0.935]
```
