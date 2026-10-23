In *The Hitchhiker's Guide to the Galaxy* the giant computer Deep Thought, after thinking for a very long time, reveals the Answer to the Great Question of Life, the Universe and Everything: forty-two.

Implement a program that prompts the user for the answer to that question, outputting `Yes` if the user inputs `42` or (case-insensitively) `forty-two` or `forty two`, and `No` otherwise. Spaces on either side should not matter either. (In CS50 the file is `deep.py`.)

Hint (from CS50): no need to convert the input to an `int` if you compare with `"42"`, a `str`, rather than `42`.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `42` → output `Yes`
- Input `Forty Two` → output `Yes`
- Input `forty-two` → output `Yes`
- Input `50` → output `No`
- Input `  FORTY-two  ` → output `Yes`
