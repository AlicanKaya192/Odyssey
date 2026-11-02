Risk kaydı bir sözlük listesi: `name`, `likelihood`, `impact`.

`top_risks(register, n)` fonksiyonunu yaz: puanı (olasılık × etki) en
yüksek `n` riski `[ad, puan]` listeleri olarak döndürsün. Puanı eşit
olanlar ada göre abece sırasında. `n` kayıttaki risk sayısından büyükse
hepsini döndür.

**Beklenen çıktı:**

```
['ransomware', 15]
['laptop lost', 12]
['db leak', 10]
```
