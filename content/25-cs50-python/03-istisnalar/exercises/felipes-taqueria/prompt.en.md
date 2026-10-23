One of the most popular places to eat in Harvard Square is Felipe's Taqueria. Its menu is in the `menu` dict in the starter code: each entree maps to its price in dollars.

Implement a program that lets the user place an order, prompting for items, one per line, until the user ends the input (`Ctrl+D`, it reaches the program as an `EOFError`). After each item, display the total cost of all items so far, prefixed with a dollar sign and with two decimal places: `Total: $6.00`. Treat the input case-insensitively and ignore anything that is not an item. Every word of every item on the menu is capitalised. (In CS50 the file is `taqueria.py`.)

Hint: `"baja taco".title()` gives `"Baja Taco"`.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Taco`, `Taco` → output `Total: $3.00`, `Total: $6.00`
- Input `Baja Taco`, `Tortilla Salad` → output `Total: $4.25`, `Total: $12.25`
- Input `Burger`, `nachos` → output `Total: $11.00`
- Input `  super BURRITO `, `bowl` → output `Total: $8.50`, `Total: $17.00`
