`bigram_prob(sentences, a, b, k)` should add `<s>` and `</s>` to the sentences,
build the counts and return the add-k probability with 3 places:

`(count(a, b) + k) / (count(a followed by anything) + k · V)`

`V` is the vocabulary size (`<s>` and `</s>` included).

**Expected output:**

```
0.667
0.2
0.024
```
