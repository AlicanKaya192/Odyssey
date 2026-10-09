`next_greater(values)` fonksiyonunu **monoton yığınla** yaz: her eleman
için kendinden sonra gelen **ilk daha büyük** değeri döndürsün; yoksa `-1`.

- `[2, 7, 3, 5, 4, 6, 8]` → `[7, 8, 5, 6, 6, 8, -1]`

Yığında cevabını bekleyen elemanların **indekslerini** tut. Yeni bir değer
gelince, yığının üstündeki kendinden küçük değerlerin hepsinin cevabı odur.

**Hız şartı:** kodun sonunda 200 000 azalan sıcaklık var; iç içe döngü
20 milyar adım atar ve süre (10 saniye) yetmez.

**Beklenen çıktı:**

```
[7, 8, 5, 6, 6, 8, -1]
200000
```
