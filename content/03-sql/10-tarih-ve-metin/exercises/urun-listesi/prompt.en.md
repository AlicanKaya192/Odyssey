For each category, show the product names **in a single cell**, in
alphabetical order.

Columns: `category_code`, `products`. The names separated by a comma and
a space (`', '`). Sort by category code.

```
category_code  products
-------------  ---------------------------------------------------
ACC            Cable, Headset, Keyboard, Microphone, Mouse, Webcam
COM            Desktop, Laptop
...
```

The function that gathers rows into one piece of text is `STRING_AGG`;
like the other aggregate functions it works with `GROUP BY`.

**The order does not come by itself.** You have to state the order inside
the list separately; the `ORDER BY` at the end of the query only sorts
the rows, not the names inside the cell. The check looks for that
clause.
