`best_window(values, k)` fonksiyonunu **kayan pencereyle** yaz: art arda `k`
değerin en büyük toplamını döndürsün. `k` liste boyundan büyükse `None`.

İlk pencereyi topla; sonra her adımda gireni ekle, çıkanı çıkar.

**Hız şartı:** kodun sonunda 200 000 günlük veride 5 000 günlük pencere
aranıyor; süre 10 saniye. Her pencereyi baştan toplamak yaklaşık bir milyar
toplama demek.

**Beklenen çıktı:**

```
16
None
256558
```
