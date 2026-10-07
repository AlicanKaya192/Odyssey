Kategori başına ciroyu dört "makinede" birleştiricili MapReduce ile
hesapla.

**Yapman gerekenler:**

1. `orders` (100 000 satır) dört makineye bölünmüş hâlde hazır:
   `machines` dört tablonun listesi.
2. **Map + birleştirici:** her makinede `(kategori, ciro)` çiftlerini
   makinenin içinde topla; her makinenin sonucu bir sözlük.
3. **Shuffle:** her anahtarı `zlib.crc32(key.encode()) % 2` numaralı
   indirgeyiciye gönder (indirgeyici başına anahtar → değer listesi).
4. **Reduce:** her anahtarın değerlerini topla.
5. Yazdır: ağdan geçen çift sayısı (birleştiricili), her indirgeyicinin
   anahtarları (abece sırasıyla, indirgeyici numarasıyla), ve sonuçların
   pandas `groupby` ile 0,01'den az farkla aynı olup olmadığı.

**Beklenen çıktı:**

```
24
0 books electronics home sports
1 clothing toys
True
```
