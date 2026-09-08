**İkiden fazla** ürünü olan kategorileri getir.

Sütunlar: `category` ve `item_count`. Kategoriye göre sırala.

```
category   item_count
---------  ----------
Accessory  6         
```

Sonuç tek satır: dört kategoriden yalnızca birinde ikiden fazla ürün var.

**`WHERE COUNT(*) > 2` yazma** — hata alırsın:

```
An aggregate may not appear in the WHERE clause
```

Sebebi işleme sırası: `WHERE` gruplar oluşmadan **önce** çalışıyor, o
sırada sayılacak bir grup yok. Grupları süzen ayrı bir parça var.
