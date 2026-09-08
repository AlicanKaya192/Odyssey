Find the suppliers that have no products at all.

One column: `name`. The result should be a single row.

```
name            
----------------
Rhine Components
```

**This exercise is testing a trap.** The form that comes to mind first is:

```sql
WHERE code NOT IN (SELECT supplier_code FROM products)
```

That query returns **zero rows** and raises no error. The reason: three
products have an empty `supplier_code`, so the subquery's list contains
`NULL`. `NOT IN` behaves like an `AND` chain and can never be true while
one part of it is unknown.

This section has a separate tool for exactly this, and it is unaffected by
empty values.
