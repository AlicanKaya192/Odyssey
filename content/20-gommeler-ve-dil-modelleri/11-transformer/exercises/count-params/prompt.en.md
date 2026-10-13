`count_params(d, layers, vocab, ffn=4)` should compute a model's parameter
count: in each block attention `4d²`, the feed-forward network `2 · ffn ·
d²`, two layer norms `4d`; add the embedding table `vocab · d`.

**Expected output:**

```
3232
123371520
95059968
```
