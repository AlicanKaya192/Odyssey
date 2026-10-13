`greedy(sentences, max_len)` should start from `<s>` with bigram counts and pick
the **most frequent** next word at each step (ties alphabetically). Stop when
`</s>` comes or after `max_len` words; return the generated words (without
`<s>` and `</s>`).

**Expected output:**

```
['my', 'order', 'is', 'late']
['my', 'order']
```
