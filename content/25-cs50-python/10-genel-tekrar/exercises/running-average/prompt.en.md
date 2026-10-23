Write a program that asks for numbers with `Number: ` until the user ends the input (`Ctrl+D`, it reaches the program as an `EOFError`). For an input that is not a number, it prints `Not a number` and keeps asking. When the input ends, it prints only the average with two digits after the point: `Average: 12.50`. If no numbers were entered, `No numbers`. Decimal numbers are valid too (`2.5`).

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Number: 10
Number: 15
Number: Average: 12.50
```
