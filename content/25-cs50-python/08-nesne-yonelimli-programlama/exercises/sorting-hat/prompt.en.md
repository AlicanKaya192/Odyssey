Write the lesson's sorting hat, but have `sort` **return** a string instead of printing. In the `Hat` class, the list of the four Hogwarts houses is a **class variable** named `houses`; `sort(cls, name)` is a **class method** (`@classmethod`) that returns a string like `Harry is in Ravenclaw`, choosing the house with `random.choice(cls.houses)`. The program asks for the name without creating any `Hat` object and prints `print(Hat.sort(name))`. Odyssey starts the random number generator with the same seed on every try, so call `random.choice` exactly once.

Example run (the prompt can say anything you like; only your output is checked):

```text
$ python cozum.py
Name: Harry
Harry is in Ravenclaw
```
