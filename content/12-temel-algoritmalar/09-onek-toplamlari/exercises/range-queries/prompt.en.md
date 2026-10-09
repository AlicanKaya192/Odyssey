Write the function `answer_queries(values, queries)`: `queries` is a list of
`[lo, hi]` pairs; for each, it returns the sum of `values[lo:hi]` (hi not
included), in order, in a list.

Build the prefix sum **once** first, then answer every question with
`prefix[hi] - prefix[lo]`.

**Speed requirement:** at the end of the code 50 000 questions are answered on
a list of 100 000 elements; the time limit is 10 seconds. Adding each question
from scratch means billions of additions.

**Expected output:**

```
[8, 19, 0]
-605946111
```
