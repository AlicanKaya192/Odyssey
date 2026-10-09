`finish_time(deps, hours)` fonksiyonunu yaz: birbirini beklemeyen işler aynı
anda yapılabiliyorsa bütün hattın en erken kaç saatte biteceğini döndürsün.

Hazır `course_order` ile topolojik sıra al; sırayla
`finish[iş] = hours[iş] + max(bağımlılıkların bitişi, yoksa 0)`. Cevap en büyük
bitiş.

**Beklenen çıktı:**

```
18
5
```
