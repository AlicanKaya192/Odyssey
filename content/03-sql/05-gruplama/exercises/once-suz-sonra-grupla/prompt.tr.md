Bu alıştırma bölümün tamamını bir araya getiriyor: iki ayrı süzme, bir
gruplama ve iki ölçütlü sıralama.

Yalnızca **stokta bulunan** ürünleri say (`stock` sıfırdan büyük),
kategoriye göre grupla ve **en az iki** ürünü kalan kategorileri getir.

Sütunlar: `category` ve `item_count`. Önce sayıya göre büyükten küçüğe,
eşitlik olursa kategoriye göre sırala.

```
category   item_count
---------  ----------
Accessory  5         
Computer   2         
Software   2         
```

Accessory'de altı ürün var ama biri stokta değil; süzme gruplamadan önce
olduğu için sayı beş çıkıyor. Display kategorisi listede yok: iki ürünü de
stokta değil.

Sıra sabit: `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY`.

`ORDER BY` en son çalıştığı için orada takma adı kullanabilirsin —
`HAVING`'de kullanamadığın hâlde.
