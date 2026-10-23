Suppose you are in the habit of making a list of items you need from the grocery store.

Implement a program that prompts the user for items, one per line, until the user ends the input (`Ctrl+D`, `EOFError`). Then output the list in **all uppercase**, **sorted alphabetically** by item, prefixing each line with the number of times the user typed that item: `2 MILK`. No need to pluralise; treat the input case-insensitively. (In CS50 the file is `grocery.py`.)

Hint: keep the counts in a dict (item → how many times). `sorted(counts)` gives the dict's keys in alphabetical order.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `mango`, `strawberry` → output `1 MANGO`, `1 STRAWBERRY`
- Input `milk`, `milk` → output `2 MILK`
- Input `tortilla`, `sweet potato` → output `1 SWEET POTATO`, `1 TORTILLA`
- Input `Apple`, `banana`, `apple`, `APPLE` → output `3 APPLE`, `1 BANANA`
