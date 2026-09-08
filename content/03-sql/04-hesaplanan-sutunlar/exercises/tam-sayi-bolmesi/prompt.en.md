Work out **half** the stock of the products that are in stock (`stock`
above zero).

Columns: `name`, `stock`, `half_stock`. Sort by name.

```
name       stock  half_stock
---------  -----  ----------
Antivirus  99     49.5      
Cable      60     30.0      
...
```

**Careful:** `stock` is an integer. Write `stock / 2` and the result is an
integer too, so half of 99 comes out as **49** — not 49.5. The fraction is
not rounded, it is thrown away.

You get no error, just the wrong number. For a fractional result you have
to make one side of the division fractional.
