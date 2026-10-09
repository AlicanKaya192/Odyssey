`pair_with_sum(items, target)` fonksiyonunu **iki işaretçiyle** yaz: sıralı
listede toplamı `target` olan iki elemanı `(küçük, büyük)` demeti olarak
döndürsün; yoksa `None`.

İşaretçiler aynı elemanı iki kez kullanamaz (`left < right`).

**Hız şartı:** kodun sonunda 200 000 elemanlı bir listede **olmayan** bir
toplam aranıyor; süre 10 saniye. İç içe döngü 20 milyar ikili dener ve
yetişmez.

**Beklenen çıktı:**

```
(1, 6)
None
None
```
