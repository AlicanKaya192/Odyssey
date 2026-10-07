Kategori başına ciroyu MapReduce ile hesapla ve pandas ile doğrula.

**Yapman gerekenler:**

1. `orders = make_orders(50_000)`; kayıtları
   `orders[["category", "quantity", "unit_price"]].to_dict("records")` ile
   sözlük listesine çevir.
2. `mapper(row)`: `(kategori, quantity * unit_price)` üretsin.
3. Shuffle ve `reducer(key, values)` (toplam) ile kategori başına ciroyu
   bul.
4. En yüksek cirolu üç kategoriyi, milyon TL olarak (iki ondalık), her
   satıra kategori ve ciro olarak yazdır.
5. pandas ile aynı hesabı yap ve her kategoride iki sonucun farkının
   0,01'den küçük olup olmadığını (`True` / `False`) yazdır.

**Beklenen çıktı:**

```
electronics 39.67
clothing 13.68
home 10.43
True
```
