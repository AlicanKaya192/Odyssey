Hiç ürünü olmayan tedarikçileri bul.

Tek sütun: `name`. Sonuç tek satır olmalı.

```
name            
----------------
Rhine Components
```

**Bu alıştırma bir tuzağı deniyor.** Akla ilk gelen yazım şu:

```sql
WHERE code NOT IN (SELECT supplier_code FROM products)
```

Bu sorgu **sıfır satır** döndürüyor ve hata da vermiyor. Sebebi: üç üründe
`supplier_code` boş, yani alt sorgunun listesinde `NULL` var. `NOT IN` bir
`AND` zinciri gibi çalışıyor ve içinde bilinmeyen bir parça varken asla
doğru olamıyor.

Bu bölümde bunun için ayrı bir araç var; boş değerlerden etkilenmiyor.
