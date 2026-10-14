`abstain_scores(results)` should compute the precision and recall of
abstaining from every `[has_answer, said_not_found]` pair. Precision: among
the questions where it said "not found", the share that have no answer.
Recall: among the questions with no answer, the share where it said "not
found". `[precision, recall]`, rounded to 2 places; `0.0` if the denominator
is 0.

**Expected output:**

```
[0.67, 0.67]
```
