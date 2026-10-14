`balanced_ids(per_label, seed)` havuzdan (`POOL`) dengeli örnek seçsin:
`rng = random.Random(seed)` kur; `LABELS` sırasıyla her kategorinin
havuzdaki mesajlarından `rng.sample(..., per_label)` ile seç ve bir
listeye ekle; sonunda listeyi `rng.shuffle` ile karıştır. Seçilenlerin
kimliklerini döndür.

**Beklenen çıktı:**

```
[27, 6, 33, 14, 15]
10
```
