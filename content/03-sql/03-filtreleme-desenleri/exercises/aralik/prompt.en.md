Sort the products priced **between 500 and 3200** from cheap to expensive,
showing `ad` and `fiyat`.

```
ad           fiyat
-----------  --------
Antivirus    780.00
Kulaklik     890.00
...
```

`BETWEEN` **includes both ends.** There is a product priced at exactly
3200 (`Monitor`) and it belongs in the result — six rows in total.

If you got five, you used a form that leaves the boundary out.
