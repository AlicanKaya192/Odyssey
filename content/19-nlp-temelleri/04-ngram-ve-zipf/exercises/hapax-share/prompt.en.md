`hapax_share(n)` should return the share of words that appear **only once**
in the vocabulary of the first `n` support tickets, with 3 places. The word
count (`counts`) is ready. In the output, watch how the share changes as the
data grows: every new ticket brings new order numbers and emails (that is
what the placeholders of section 03 are for).

**Expected output:**

```
100 0.371
1000 0.596
3000 0.65
```
