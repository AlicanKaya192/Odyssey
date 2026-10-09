Write the function `word_counts(words)`: it takes a list of words and
returns how many times each word occurs, in a **dictionary**.

- `["to", "be", "or", "not", "to", "be"]` →
  `{"to": 2, "be": 2, "or": 1, "not": 1}`

Do not use `.count()`: scanning the list from the start for every word would
be `O(n²)`. Count in a dictionary in one pass.

**Expected output:**

```
{'to': 2, 'be': 2, 'or': 1, 'not': 1}
{}
```
