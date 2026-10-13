The counts are ready: `counts[class][word]` is how many reviews of that class
contain the word, `sizes[class]` the number of reviews in that class, `common`
the sum of the two classes.

- `log_odds(word)`: `log(((pos + 1) / (n_pos + 2)) / ((neg + 1) / (n_neg + 2)))`.
- `top_words(label, k)`: sort the words that appear in **at least 5** reviews
  in total by log-odds; return the `k` smallest for `"negative"` and the `k`
  largest for `"positive"` (the most extreme first).

**Expected output:**

```
['hate', 'honest', 'worse', 'stopped']
['love', 'expected', 'totally', 'packed']
```
