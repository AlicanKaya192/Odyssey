Work out the revenue per category with MapReduce and check it with pandas.

**What to do:**

1. `orders = make_orders(50_000)`; turn the records into a list of
   dictionaries with `orders[["category", "quantity", "unit_price"]].to_dict("records")`.
2. `mapper(row)`: it produces `(category, quantity * unit_price)`.
3. Find the revenue per category with the shuffle and `reducer(key, values)`
   (a total).
4. Print the three categories with the highest revenue, in millions of lira
   (two decimals), with the category and revenue on each line.
5. Do the same calculation with pandas and print whether the difference
   between the two results is smaller than 0.01 in every category (`True` /
   `False`).

**Expected output:**

```
electronics 39.67
clothing 13.68
home 10.43
True
```
