A machine sells bottles of Coke for 50 cents and only accepts coins of 25, 10 and 5 cents.

Implement a program that prompts the user to insert a coin, **one at a time**. Before each coin, print the amount still due in the form `Amount Due: 50`. Once the user has put in at least 50 cents, print how many cents in change they are owed in the form `Change Owed: 10` and stop. Assume the user will only input integers; ignore any value that is not an accepted coin (like `30`), so the amount does not change. (In CS50 the file is `coke.py`.)

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `25`, `25` → output `Amount Due: 50`, `Amount Due: 25`, `Change Owed: 0`
- Input `25`, `10`, `25` → output `Amount Due: 50`, `Amount Due: 25`, `Amount Due: 15`, `Change Owed: 10`
- Input `10`, `5`, `30`, `25`, `10` → output:

```text
Amount Due: 50
Amount Due: 40
Amount Due: 35
Amount Due: 35
Amount Due: 10
Change Owed: 0
```

- Input `5`, `5`, `5`, `5`, `5`, `5`, `5`, `5`, `5`, `5` → output:

```text
Amount Due: 50
Amount Due: 45
Amount Due: 40
Amount Due: 35
Amount Due: 30
Amount Due: 25
Amount Due: 20
Amount Due: 15
Amount Due: 10
Amount Due: 5
Change Owed: 0
```

