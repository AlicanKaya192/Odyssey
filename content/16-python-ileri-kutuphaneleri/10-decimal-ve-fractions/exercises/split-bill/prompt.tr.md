`split_bill(total, n)` tutarı `n` kişiye bölüp her payı metin olarak
listede döndürüyor; ama paylar kuruşa yuvarlanınca toplam tutmuyor
(`100.00` üçe → üç kez `33.33`). Payları **aşağı** yuvarla
(`ROUND_DOWN`), kalan kuruşları **ilk** paylara birer birer ekle.
Payların toplamı her zaman `total`'a eşit olmalı.

**Beklenen çıktı:**

```
['33.34', '33.33', '33.33']
['0.02', '0.02', '0.01']
```
