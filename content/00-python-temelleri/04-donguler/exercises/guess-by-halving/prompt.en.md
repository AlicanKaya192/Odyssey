Someone picked a number between 1 and 1000: `secret = 371`. After each
guess, all you are told is "too high" or "too low". The smartest way is to
say the **exact middle** of the remaining range every time: each guess
rules out half of the possibilities. This is called **binary search**.

Start the range with `low = 1`, `high = 1000` and repeat:

1. `guess = (low + high) // 2`
2. Print the guess.
3. If the guess is larger than `secret`, move the upper limit to one below
   the guess; if smaller, move the lower limit to one above the guess; if
   equal, stop.

Count the guesses in the variable `guesses`. The output should be:

```
Guess 1: 500 -> too high
Guess 2: 250 -> too low
Guess 3: 375 -> too high
Guess 4: 312 -> too low
Guess 5: 343 -> too low
Guess 6: 359 -> too low
Guess 7: 367 -> too low
Guess 8: 371 -> correct
Found 371 in 8 guesses
```

You found one number among 1000 in 8 guesses; whichever number is picked,
10 guesses are always enough. That is the power of this method: every
guess halves the remaining range.

> Watch out: when updating a limit, write `high = guess - 1`, not
> `high = guess`: `guess` has already been tried. Otherwise the loop never
> ends for some numbers.
