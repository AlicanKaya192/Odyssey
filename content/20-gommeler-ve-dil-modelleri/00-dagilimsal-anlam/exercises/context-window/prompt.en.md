`context_words(tokens, i, window)` should return, in order, up to `window`
words on the left and on the right of token `i`; the token itself is not
included. At the start or end of the sentence the window is cut short.

**Expected output:**

```
['the', 'small', 'chased', 'the']
['small']
['cat', 'chased', 'the']
```
