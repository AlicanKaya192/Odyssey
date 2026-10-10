Write the function `top_words(texts, n)`: count the words of each text
separately into a `Counter` with `ThreadPoolExecutor` (`pool.map`), add the
counters up and return the `n` most common words as `[word, count]` lists
(`most_common`).

**Expected output:**

```
[['a', 4], ['c', 3]]
```
