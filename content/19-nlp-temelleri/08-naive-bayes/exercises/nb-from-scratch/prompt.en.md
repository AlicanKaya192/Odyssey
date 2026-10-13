`train` is ready: class counts, word counts per class and the vocabulary.
`predict(text)` should compute, for each class (in alphabetical order), the
sum of:

1. `log(prior)`: `priors[label] / total`
2. for each word of the text **that is in the vocabulary**,
   `log((counts[label][w] + 1) / (class_word_total + len(vocab)))`

and return the class with the largest score.

**Expected output:**

```
great sound -> pos
battery died -> neg
terrible -> neg
unknown words -> pos
```
