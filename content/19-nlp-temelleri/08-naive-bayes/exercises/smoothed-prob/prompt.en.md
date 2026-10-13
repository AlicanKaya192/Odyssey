`word_prob(count, class_total, vocab_size, alpha)` should return a word's
smoothed probability within a class, with 5 places:

`(count + alpha) / (class_total + alpha * vocab_size)`

In the first example the word was never seen in the class, yet its
probability is not zero.

**Expected output:**

```
0.00077
0.02
0.02437
```
