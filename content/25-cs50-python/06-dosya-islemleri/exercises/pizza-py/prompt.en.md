Pinocchio's Pizza & Subs's menu is ready as CSV: `regular.csv` and `sicilian.csv` are in the exercise's folder.

Implement a program that expects **exactly one** command-line argument, the name of a CSV file in this format, and outputs the table formatted as ASCII art with the `tabulate` package: `tabulate(..., headers="keys", tablefmt="grid")`. If there is not exactly one argument (`Too few command-line arguments` / `Too many command-line arguments`), the name does not end in `.csv` (`Not a CSV file`), or the file does not exist (`File does not exist`), exit via `sys.exit`. (In CS50 the file is `pizza.py`; `tabulate` is installed in Odyssey.)

Hint: `csv.DictReader` gives rows as dicts; `tabulate` takes a list of dicts with `headers="keys"`.

## How to test

The cases CS50 gives; Odyssey runs each one in a separate folder and compares your output and the file you write.

- No input → output (nothing) (exit code 1)
- Command `python cozum.py regular.csv sicilian.csv` → output (nothing) (exit code 1)
- Command `python cozum.py non_existent.csv` → output (nothing) (exit code 1)
- Command `python cozum.py sicilian.txt` → output (nothing) (exit code 1)
- Command `python cozum.py regular.csv` → output:

```text
+-----------------+---------+---------+
| Regular Pizza   | Small   | Large   |
+=================+=========+=========+
| Cheese          | $13.50  | $18.95  |
+-----------------+---------+---------+
| 1 topping       | $14.75  | $20.95  |
+-----------------+---------+---------+
| 2 toppings      | $15.95  | $22.95  |
+-----------------+---------+---------+
| 3 toppings      | $16.95  | $24.95  |
+-----------------+---------+---------+
| Special         | $18.50  | $26.95  |
+-----------------+---------+---------+
```

- Command `python cozum.py sicilian.csv` → output:

```text
+------------------+---------+---------+
| Sicilian Pizza   | Small   | Large   |
+==================+=========+=========+
| Cheese           | $25.50  | $39.95  |
+------------------+---------+---------+
| 1 item           | $27.50  | $41.95  |
+------------------+---------+---------+
| 2 items          | $29.50  | $43.95  |
+------------------+---------+---------+
| 3 items          | $31.50  | $45.95  |
+------------------+---------+---------+
| Special          | $33.50  | $47.95  |
+------------------+---------+---------+
```

