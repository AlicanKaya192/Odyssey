Work out **half** the stock of the products that are in stock (`stok`
above zero).

Columns: `ad`, `stok`, `yari_stok`. Sort by name.

```
ad         stok  yari_stok
---------  ----  ---------
Antivirus  99    49.500000
Kablo      60    30.000000
...
```

**Careful:** `stok` is an integer. Write `stok / 2` and the result is an
integer too, so half of 99 comes out as **49** — not 49.5. The fraction is
not rounded, it is thrown away.

You get no error, just the wrong number. For a fractional result you have
to make one side of the division fractional.
