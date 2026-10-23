Before there were emoji, there were emoticons: `:)` was a happy face and `:(` a sad one.

Implement a function called `convert` that accepts a `str` and **returns** that same input with any `:)` converted to `[happy]` and any `:(` converted to `[sad]`; all other text unchanged. Then, in the same file, implement a function called `main` that prompts the user for input, calls `convert` on it and prints the result. Be sure to call `main` at the bottom of your file.

*In CS50 the faces become emoji (🙂 🙁); in Odyssey we use `[happy]` / `[sad]` so that your code and output only use characters on the keyboard.* (In CS50 the file is `faces.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Hello :)` → output `Hello [happy]`
- Input `Goodbye :(` → output `Goodbye [sad]`
- Input `Hello :) Goodbye :(` → output `Hello [happy] Goodbye [sad]`
