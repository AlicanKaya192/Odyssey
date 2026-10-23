Suppose you are in a country where breakfast is eaten between 7:00 and 8:00, lunch between 12:00 and 13:00, and dinner between 18:00 and 19:00. Implement a program that prompts the user for a time and outputs `breakfast time`, `lunch time` or `dinner time` accordingly. If it is not time for a meal, **do not output anything**. The input is in 24-hour time as `#:##` or `##:##`, and each range is inclusive (7:00 and 8:00 are both breakfast).

Structure your program as in the starter code: `convert(time)` turns text like `"7:30"` into hours as a `float` (`7.5`). The `if __name__ == "__main__":` line at the end calls `main` only when the file is run directly; we will see why in week 5 with unit tests. (In CS50 the file is `meal.py`.)

Hint (from CS50): `hours, minutes = time.split(":")`; there are 60 minutes in an hour.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `7:00` → output `breakfast time`
- Input `7:30` → output `breakfast time`
- Input `12:42` → output `lunch time`
- Input `18:32` → output `dinner time`
- Input `11:11` → output (nothing)
- Input `8:00` → output `breakfast time`
- Input `19:00` → output `dinner time`
