`beam_step(beams, table, width)` should take one step of beam search. `beams`
is a list of `[score, words]`; `table` maps last word → {next word:
probability}. Extend each path with every possible word, add
`log(probability)` to the score (3 places), sort by score from largest to
smallest, and return the best `width` paths.

**Expected output:**

```
-1.021 ['<s>', 'the', 'app']
-1.204 ['<s>', 'my', 'order']
```
