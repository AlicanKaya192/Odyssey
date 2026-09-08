Hiç sipariş vermemiş müşterileri bul.

Tek sütun: `customer`.

```
customer      
--------------
Quiet Partners
```

Altı müşteriden yalnızca biri hiç sipariş vermemiş.

Bu, `LEFT JOIN`'in en çok işe yarayan kalıbı ve iki adımdan oluşuyor:
önce bütün müşterileri getir, sonra **eşleşme bulunamayanları** süz.

Eşleşme bulunamadığında sağ tablonun sütunları boş kalıyor; süzmeyi ona
göre yapıyorsun.

Aynı kalıp "hiç satılmamış ürünler", "hiç kargolanmamış siparişler" için de
kullanılıyor.
