`perplexity(probs)` should compute perplexity from the probabilities the model
gave each word: `exp(−mean log p)`, 2 places. If any probability is 0,
return `math.inf`.

**Expected output:**

```
2.0
3.07
inf
```
