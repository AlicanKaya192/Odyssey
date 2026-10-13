The lexicon sometimes decides on a very weak score.
`coverage_accuracy(margin)` should decide only for reviews with
`abs(score) > margin` (`scores` is ready): `"positive"` if the score > 0,
otherwise `"negative"`. Return `[coverage, accuracy]`, both with 3 places:
coverage is the share of reviews decided, accuracy the share of correct
predictions among them.

**Expected output:**

```
0 [0.777, 0.881]
1 [0.436, 0.979]
2 [0.182, 0.997]
```
