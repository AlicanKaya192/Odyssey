The lesson's rule thought "Not bad" was negative. `predict_neg(text)` should
work with the same `GOOD` and `BAD` lists, but if `not` comes **right
before** a word from a list, it should reverse that word's effect: a
positive word counts -1, a negative word +1. Return `"positive"` if the
score is positive, `"negative"` if negative and `"neutral"` if zero.

The last line of the output is the number of correct predictions on 2000
reviews; the lesson's rule got 898. Look at the third example too: when
another word comes between "not" and the word, the rule is wrong again.

**Expected output:**

```
positive
negative
positive
1005
```
