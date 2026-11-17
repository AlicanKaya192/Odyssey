`class_index(names)` should create a subfolder for each name in a temporary
folder with a blank (4 × 4, black) PNG inside, then read it with
`datasets.ImageFolder` and return the `class_to_idx` dictionary. Look at how
the order changes with number names.

**Expected output:**

```
{'bird': 0, 'cat': 1, 'dog': 2}
{'12': 0, '3': 1, '7': 2}
```
