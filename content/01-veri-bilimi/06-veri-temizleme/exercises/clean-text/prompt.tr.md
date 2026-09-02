Aynı şehir üç farklı yazımla geliyor. Bunu düzeltmeden gruplarsan
**sayılar bölünüyor**.

Sütun adları başlangıç kodunda temizlendi; sıra değerlerde.

**Yapman gerekenler:**

1. Temizlemeden **önce** kaç farklı şehir olduğunu yazdır.
2. `name` ve `city` sütunlarındaki boşlukları at ve her kelimenin ilk
   harfini büyüt.
3. `name` ve `city` sütunlarını yazdır.
4. Temizledikten **sonra** kaç farklı şehir olduğunu yazdır.

**Beklenen çıktı:**

```
6
    name    city
0    Ada  Ankara
1  Kerem   Izmir
2   Mina  Ankara
3    Ada  Ankara
4  Deniz   Bursa
5    Efe   Izmir
6   Sila  Ankara
3
```

**İlk ve son satır bu alıştırmanın bütün mesele:** aynı veri, önce **altı**
şehir sonra **üç** şehir. `"Ankara"`, `"ANKARA"` ve `"Ankara "` pandas için
üç ayrı değerdi.

Bunu fark etmeden `groupby("city")` yazarsan Ankara üç ayrı gruba bölünüyor
ve hiçbirinin ortalaması doğru olmuyor.

**Kontrol yolu:** `nunique()` beklediğinden büyükse tutarsız yazım var
demektir.
