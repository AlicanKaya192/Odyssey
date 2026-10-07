Measure how much the combiner cuts the number of pairs that cross the
network on five "machines".

**What to do:**

1. `orders = make_orders(200_000)`; split the table into five pieces of
   40 000 (each piece is a machine).
2. In each piece build the `(payment, quantity)` pairs.
3. Without a combiner: add up the number of all pairs.
4. With a combiner: in each piece add up the pairs per payment method with
   `defaultdict(int)`; the number of pairs to send is the length of this
   dictionary. Also combine all pieces' local totals into a single
   dictionary.
5. Print the two numbers on one line.
6. Print whether the combined totals match pandas'
   `orders.groupby("payment")["quantity"].sum()`.

**Expected output:**

```
200000 15
True
```
