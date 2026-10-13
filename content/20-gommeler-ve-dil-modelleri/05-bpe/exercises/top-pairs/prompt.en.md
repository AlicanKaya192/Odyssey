`top_pairs(words, k)` should count the adjacent symbol pairs in a list of
`[symbol list, frequency]` items, weighted by the word's frequency, and
return the `k` most frequent pairs as `[a, b, count]`. Order: count from
largest, ties by the pair's alphabetical order.

**Expected output:**

```
['w', '</w>', 11]
['l', 'o', 7]
['o', 'w', 7]
```
