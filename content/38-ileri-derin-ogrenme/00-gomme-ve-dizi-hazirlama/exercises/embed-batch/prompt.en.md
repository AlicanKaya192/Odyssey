`embed_batch(batch_ids, vocab_size, dim)` should build an
`nn.Embedding(vocab_size, dim)` with `padding_idx=0` (the seed is set in the
starter) and pass the padded batch through it. Return a three-item list: the
output's shape (a list), the number of positions whose vector is all zeros,
and the layer's parameter count.

**Expected output:**

```
[[2, 4, 4], 3, 40]
```
