`answer_queries(values, queries)` fonksiyonunu yaz: `queries` `[lo, hi]`
çiftlerinin listesi; her biri için `values[lo:hi]` toplamını (hi dahil değil)
sırayla bir listede döndürsün.

Önce önek toplamını **bir kez** kur, sonra her soruyu `prefix[hi] -
prefix[lo]` ile cevapla.

**Hız şartı:** kodun sonunda 100 000 elemanlı listede 50 000 soru
cevaplanıyor; süre 10 saniye. Her soruyu baştan toplamak milyarlarca
toplama demek.

**Beklenen çıktı:**

```
[8, 19, 0]
-605946111
```
