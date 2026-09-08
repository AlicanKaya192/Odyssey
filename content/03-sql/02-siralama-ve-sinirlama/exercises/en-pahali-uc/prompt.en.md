Bring back the `name` and `price` of the **three** most expensive products.

```
name       price  
---------  -------
Laptop     24500.0
Desktop    18900.0
Projector  7400.0 
```

Two pieces are needed: how many rows you want (`TOP`) and the ordering
that decides **which** rows those are (`ORDER BY`).

Writing `TOP 3` without `ORDER BY` means "three products at random" — the
query runs but does not answer the question you asked.
