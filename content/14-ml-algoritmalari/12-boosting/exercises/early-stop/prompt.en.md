Write the function `early_stop(val_errors, patience)`: walk the validation
errors round by round (rounds count from 1); keep the best error and its round;
stop if there is no improvement for `patience` rounds in a row. Return the tuple
`(best round, stopping round)`; if the list ends, the stopping round is the last
round.

**Expected output:**

```
(5, 8)
(3, 3)
```
