Ask the user how many coins to flip. On each flip, pick a result with `random.choice(["heads", "tails"])` and print it on its own line. At the end, print how many times it was `heads`, in the form `3 heads`.

The check starts the random generator with the same seed for each case; if you call the random functions in the order the prompt gives, your program produces the same results.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Flips: 5
heads
heads
tails
heads
tails
3 heads
```
