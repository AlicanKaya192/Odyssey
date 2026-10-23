The U.S. Food and Drug Administration (FDA) publishes posters showing nutrition information for the 20 most frequently consumed raw fruits in the United States. The `calories` dict in the starter code maps each fruit on the poster to the calories in one portion; the keys are in lowercase.

Implement a program that prompts the user for a fruit (case-insensitively) and outputs the calories in one portion of it in the form `Calories: 130`. Assume the user types the fruit as written on the poster (`strawberries`, not `strawberry`). If it is not a fruit, **output nothing**. (In CS50 the file is `nutrition.py`; CS50 asks students to type the dict themselves, here it is given.)

Hint: `in` asks whether a key is in a dict: `"apple" in calories` → `True`.

## How to test

The cases CS50 gives; Odyssey runs each one separately and compares your output. Your prompt can say anything you like; only your output is checked.

- Input `Apple` → output `Calories: 130`
- Input `Avocado` → output `Calories: 50`
- Input `Sweet Cherries` → output `Calories: 100`
- Input `Tomato` → output (nothing)
- Input `  KIWIFRUIT ` → output `Calories: 90`
- Input `honeydew melon` → output `Calories: 50`
