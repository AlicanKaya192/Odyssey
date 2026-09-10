Set the stock to `20` for every product whose stock is **below 5**.

Four products will be affected. The others must not change.

The real subject of this exercise is not the command but the **habit**.
Rehearse before you write:

```sql
SELECT * FROM products WHERE stock < 5;
```

See on screen which rows are about to change. If four rows come back the
`WHERE` is right, and now you can write the `UPDATE` with that same
`WHERE`.

It takes two seconds and it prevents almost every mistake people make
writing `UPDATE`. A real database has no undo button.
