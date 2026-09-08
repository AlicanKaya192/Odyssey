Return each product's name and its supplier's name.

Columns: `product` and `supplier`. Sort by product name.

**All twelve products must be in the result.** Three of them have no
supplier recorded; for those, `supplier` will be empty.

```
product    supplier      
---------  --------------
Antivirus  Aegean Systems
Cable      Anatolia Tech 
...
```

Write a plain `JOIN` and the result is **nine** rows: the three products
with no supplier quietly disappear. You get no error either — which is why
it is hard to notice.

There is a way to keep every row on the left.
