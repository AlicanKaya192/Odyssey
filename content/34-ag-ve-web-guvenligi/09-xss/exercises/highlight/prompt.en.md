A search page highlights the searched word in the result with
`<mark>...</mark>`. `highlight(text, word)` should first encode the text
**and** the word with `html.escape`, then replace the encoded word in the
encoded text with `<mark>WORD</mark>`. If the word is empty, return only
the encoded text. The starter code encodes nothing (reflected XSS).

**Expected output:**

```
x&lt;<mark>y</mark>
<mark>te</mark>a &amp; <mark>te</mark>e
a<mark>&lt;</mark>b
```
