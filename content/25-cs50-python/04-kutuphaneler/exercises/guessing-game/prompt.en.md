"I'm thinking of a number between 1 and 100... What is it?"

Implement a program that:

- Prompts the user for a level, `n`. If the user does not input a positive integer, it prompts again.
- Randomly generates an integer between 1 and `n`, inclusive, with the `random` module: `random.randint(1, n)`.
- Prompts the user to guess it; if the guess is not a positive integer, it prompts again.
- If the guess is smaller, it outputs `Too small!`, if larger `Too large!`, and prompts again; if equal, it outputs `Just right!` and exits.

(In CS50 the file is `game.py`.)

The check resets the random number generator to the same starting point (a seed) for each case; if you call `randint` once, after the level, your program picks the same number.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `cat`, `-1`, `1`, `1` → output `Just right!`
- Input `10`, `cat`, `-1`, `100`, `1`, `4` → output `Too large!`, `Too small!`, `Just right!`
- Input `10000`, `cat`, `-1`, `100000`, `1`, `4186` → output `Too large!`, `Too small!`, `Just right!`
- Input `0`, `100`, `cat`, `-1`, `1000`, `1`, `58` → output `Too large!`, `Too small!`, `Just right!`
