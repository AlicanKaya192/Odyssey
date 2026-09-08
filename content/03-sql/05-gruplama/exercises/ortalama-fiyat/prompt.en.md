Return three things per category at once: how many products there are,
and the price of the cheapest and the priciest.

Columns: `category`, `item_count`, `cheapest`, `priciest`. Sort by
category.

```
category   item_count  cheapest  priciest
---------  ----------  --------  --------
Accessory  6           95.0      1320.0  
Computer   2           18900.0   24500.0 
...
```

You can use as many aggregate functions as you like inside the same
`GROUP BY`; they all apply to the same groups.
