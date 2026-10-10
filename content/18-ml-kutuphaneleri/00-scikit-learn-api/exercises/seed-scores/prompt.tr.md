Başlangıç kodundaki sabit veriyle `seed_scores(seeds)` her tohum için
`RandomForestClassifier(n_estimators=5, random_state=tohum)` eğitsin ve test
skorlarını 3 basamağa yuvarlı liste olarak döndürsün. Başlangıç kodu
`random_state` vermiyor: her çalıştırmada başka sonuç çıkıyor.

**Beklenen çıktı:**

```
[0.84, 0.853, 0.867]
```
