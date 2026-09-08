Return the id and order count of customers with **at least two orders**.

Columns: `customer_id` and `order_count`. Sort by the count descending,
breaking ties by id.

```
customer_id  order_count
-----------  -----------
1            3          
2            2          
...
```

The result should be four rows.

You could solve this with `HAVING` and it would be shorter. But here we
are learning the **derived table**: do the grouping in a subquery inside
`FROM` and filter its result from outside.

That pattern becomes the only way when the grouped result has to be joined
to another table.

**The alias is required:** if you do not give the temporary table a name
after closing the parenthesis, you get a syntax error.
