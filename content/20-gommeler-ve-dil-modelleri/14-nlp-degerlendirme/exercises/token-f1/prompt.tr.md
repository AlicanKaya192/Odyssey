Soru cevaplamada sık kullanılan ölçü: `token_f1(candidate, reference)`
ortak kelime sayısını (iki `Counter`'ın kesişimi) bulsun; kesinlik = ortak /
aday kelime sayısı, geri çağırma = ortak / referans kelime sayısı; F1 ikisinin
harmonik ortalaması (3 basamak). Ortak kelime yoksa `0.0`.

**Beklenen çıktı:**

```
0.667
1.0
0.0
```
