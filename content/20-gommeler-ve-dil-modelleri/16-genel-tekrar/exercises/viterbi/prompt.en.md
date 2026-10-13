`viterbi(words, start, trans, emit)` should find the most likely tag sequence
in an HMM. At the first word the score is `log start[t] + log emit[t][word]`;
at each next word, for each tag pick the best previous tag (`score + log
trans[previous][t]`), add the emission and keep a back pointer. At the end,
walk back from the best tag.

**Expected output:**

```
['DET', 'NOUN']
['NOUN', 'DET', 'NOUN']
```
