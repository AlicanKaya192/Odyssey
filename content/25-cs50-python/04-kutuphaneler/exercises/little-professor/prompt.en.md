One of David's first toys as a child was Little Professor, a "calculator" that would generate ten maths problems for him to solve. If it displayed `4 + 0 =`, David would answer `4`. For a wrong answer it displayed `EEE`; after three wrong answers to the same problem it showed the correct answer (`4 + 0 = 4`).

Implement a program that:

- Prompts the user for a level, `n`. If the user does not input 1, 2 or 3, it prompts again.
- Generates **ten** addition problems formatted as `X + Y = `, where `X` and `Y` are non-negative integers with `n` digits. Use the problem as the prompt of `input`.
- Asks each problem. If an answer is wrong (or not even a number), it outputs `EEE` and asks again, allowing three tries in total for that problem. If all three are wrong, it outputs the correct answer as `6 + 6 = 12` and moves on.
- Finally outputs the score: the number of problems answered correctly on the first try, as `Score: 9`.

Structure your program as in the starter code: `get_level` gets and returns the level, `generate_integer(level)` returns a random integer with `level` digits (0–9 for 1, 10–99 for 2, 100–999 for 3; it raises a `ValueError` for any other level). Generate the numbers **`X` first, then `Y`** for each problem: the check starts the random generator with the same seed for each case, so in the same order your program asks the same problems. (In CS50 the file is `professor.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `1`, `7`, `6`, `9`, `6`, `9`, `11`, `1`, `12`, `4`, `9` → output `Score: 10`
- Input `1`, `cat`, `7`, `6`, `9`, `6`, `9`, `11`, `1`, `12`, `4`, `9` → output `EEE`, `Score: 9`
- Input `1`, `cat`, `8`, `9`, `6`, `9`, `6`, `9`, `11`, `1`, `12`, `4`, `9` → output `EEE`, `EEE`, `EEE`, `5 + 2 = 7`, `Score: 9`
- Input `-1`, `4`, `2`, `94`, `161`, `137`, `108`, `145`, `107`, `117`, `21`, `141`, `82` → output `Score: 10`
- Input `3`, `751`, `1043`, `1095`, `450`, `288`, `1173`, `1315`, `1043`, `959`, `1117` → output `Score: 10`
