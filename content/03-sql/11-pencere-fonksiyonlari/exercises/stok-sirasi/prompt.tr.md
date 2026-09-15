Ürünleri stoğa göre, en çoktan en aza sırala ve her birine bir sıra ver.
Aynı stoktaki ürünler **aynı sırayı** alsın, sonraki sıra **atlamasın**.

Sütunlar: `name`, `stock`, `stock_rank`. Satırları önce `stock`
(azalan), sonra `name` ile sırala.

```
name          stock  stock_rank
------------  -----  ----------
Antivirus     99     1
Office Suite  99     1
Cable         60     2
Keyboard      32     3
...
```

Üç sıralama işlevi eşitlikte farklı davranıyor. Burada istenen 1, 1, 2 —
1, 1, 3 değil.
