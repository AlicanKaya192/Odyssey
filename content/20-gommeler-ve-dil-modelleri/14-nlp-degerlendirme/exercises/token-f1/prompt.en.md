A measure common in question answering: `token_f1(candidate, reference)`
should find the number of shared words (the intersection of two `Counter`s);
precision = shared / candidate words, recall = shared / reference words; F1 is
their harmonic mean (3 places). `0.0` if no words are shared.

**Expected output:**

```
0.667
1.0
0.0
```
