Raise the price of the products in the `ACC` category by **10%**.

The other categories must not change — the check looks at both.

**Do not work the prices out by hand.** You could find the new price of
all six with a calculator and type them in one by one, but that is a
solution that stops working the moment another `ACC` product is added.

Inside `SET` you can use the column itself:

```sql
SET price = price * 1.10
```

The server does this separately for every row: it reads that row's own
old price and writes the new one.

Do not forget the `WHERE`. Forget it and all twelve products get the
rise, and the server will not call that an error.
