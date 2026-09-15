Rank the products by stock, from most to least. Products with the same
stock get **the same rank**, and the next rank does **not skip**.

Columns: `name`, `stock`, `stock_rank`. Sort the rows by `stock`
(descending) first, then by `name`.

```
name          stock  stock_rank
------------  -----  ----------
Antivirus     99     1
Office Suite  99     1
Cable         60     2
Keyboard      32     3
...
```

The three ranking functions behave differently on ties. What is wanted
here is 1, 1, 2 — not 1, 1, 3.
