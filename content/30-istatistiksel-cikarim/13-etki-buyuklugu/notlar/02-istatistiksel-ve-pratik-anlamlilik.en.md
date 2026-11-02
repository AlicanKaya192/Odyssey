In statistics the word "significant" only means "hard to explain by
chance". It does not mean "important", "large" or "useful". The easiest way
to make the decision clear is to write a practical threshold **before** the
test: "unless the difference is at least this big, the change is not worth
it."

## Five situations

Compare the difference's confidence interval with the threshold and with
zero:

| Where is the interval? | Statistical | Practical | Decision |
|---|---|---|---|
| Entirely above the threshold | significant | important | apply |
| Above zero but containing the threshold | significant | unclear | more data, or decide by cost |
| Above zero, entirely below the threshold | significant | unimportant | not worth applying |
| Containing zero, wide | not significant | unknown | the test is too weak, no result |
| Containing zero, narrow and below the threshold | not significant | unimportant | any effect is small |

The difference between the last two rows matters: a "not significant"
result **says nothing** when the interval is wide; when the interval is
narrow it says "there is no large effect".

## Common mistakes

- **"p is tiny, so the effect is big."** p depends on the sample size; with
  a large sample a tiny difference gives a tiny p as well.
- **"Not significant, so there is no effect."** With a small sample a real
  and large effect can come out not significant too. Look at the interval.
- **Choosing the threshold after the result.** Setting a threshold after
  seeing the result bends the test toward the answer you wanted.
- **Reporting only the relative change.** "Up 50%" cannot be read without
  the base rate.

## A one-sentence report

"The new button raised buying by X points over A's base rate (95%
confidence interval: low–high points); it is not certain that it reached the
increase of at least 1 point we aimed for." This sentence carries far more
information than a p-value.
