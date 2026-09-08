Her ürünün adını ve tedarikçisinin adını getir.

Sütunlar: `product` ve `supplier`. Ürün adına göre sırala.

**On iki ürünün hepsi sonuçta olmalı.** Üç üründe tedarikçi kayıtlı değil;
onlarda `supplier` boş görünecek.

```
product    supplier      
---------  --------------
Antivirus  Aegean Systems
Cable      Anatolia Tech 
...
```

Düz `JOIN` yazarsan sonuç **dokuz** satır olur: tedarikçisi olmayan üç
ürün sessizce kaybolur. Hata da almazsın — bu yüzden fark edilmesi zor.

Soldaki her satırı korumanın bir yolu var.
