`aspect_labels(text, aspects)` should split the text into sentences with
`re.findall(r"[^.!?]+", text.lower())`. For every sentence that mentions a
feature, add its `negated(sentence, 3)` score to that feature. Finally return
a dictionary for the features that **appeared**: total > 0 `"positive"`, < 0
`"negative"`, 0 `"neutral"`. `negated` is ready.

**Expected output:**

```
{'strap': 'positive', 'screen': 'negative'}
```
