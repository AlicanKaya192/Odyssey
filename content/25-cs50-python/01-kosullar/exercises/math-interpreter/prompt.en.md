Python already does maths, but let us write a program that lets users do maths without knowing Python. Implement a program that prompts the user for an arithmetic expression and then calculates and outputs the result as a floating-point value **formatted to one decimal place**. Assume the input is formatted as `x y z`, with one space between each: `x` is an integer, `y` is `+`, `-`, `*` or `/`, and `z` is an integer. For `1 + 1`, output `2.0`. If `y` is `/`, `z` will not be 0. (In CS50 the file is `interpreter.py`.)

Hint (from CS50): the `split` method of a string separates it into values, which can all be assigned to variables at once: `x, y, z = expression.split(" ")` assigns `"1"` to `x`, `"+"` to `y` and `"1"` to `z` for `"1 + 1"`.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `1 + 1` → output `2.0`
- Input `2 - 3` → output `-1.0`
- Input `2 * 2` → output `4.0`
- Input `50 / 5` → output `10.0`
- Input `7 / 2` → output `3.5`
