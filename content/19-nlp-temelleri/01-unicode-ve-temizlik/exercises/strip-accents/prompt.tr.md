`words.txt` dosyasında aksanlı kelimeler var. `strip_accents(text)`
metni NFD ile harf + işaret olarak ayırsın, birleşen işaretleri
(`unicodedata.combining(c)` sıfırdan farklı olanlar) atsın ve kalanları
birleştirip döndürsün.

**Beklenen çıktı:**

```
cafe
naive
Angstrom
seker
Izmir
uber
facade
resume
jalapeno
creme brulee
```
