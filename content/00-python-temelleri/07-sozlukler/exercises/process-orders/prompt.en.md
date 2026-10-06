A shop's stock and the incoming orders:

```python
stock = {"apple": 10, "pear": 4, "plum": 0}
orders = [("apple", 3), ("pear", 5), ("plum", 1), ("kiwi", 2), ("apple", 6)]
```

Process the orders **in order**. For each order:

- If the product is not in the stock at all (no such key): add it to the
  list `unknown` and print `kiwi: unknown product`.
- If there is enough stock: take it off the stock and print
  `apple: sent 3`.
- If there is not enough stock: **send nothing**, write the missing amount
  to the dictionary `shortages` and print `pear: short by 1`.

At the end, print the remaining stock:

```
apple: sent 3
pear: short by 1
plum: short by 1
kiwi: unknown product
apple: sent 6
Stock: {'apple': 1, 'pear': 4, 'plum': 0}
```

Each order depends on the one before it: the first apple order brings the
stock down to 7, and the last apple order looks at that 7.

> Watch out: do not touch the stock when there is not enough; `pear` must
> stay at 4. Each order is a tuple; with `for product, amount in orders:`
> you get its two parts in separate variables.
