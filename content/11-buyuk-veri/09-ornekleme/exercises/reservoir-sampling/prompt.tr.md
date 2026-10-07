Rezervuar örneklemesini kendin yaz ve her öğeye eşit şans verdiğini
dene.

**Yapman gerekenler:**

1. `reservoir(items, k, seed)` fonksiyonunu yaz:
   - `rng = random.Random(seed)`,
   - ilk `k` öğeyi listeye koy,
   - sonraki her `i`. öğe için `j = rng.randint(0, i)`; `j < k` ise
     `sample[j] = item`,
   - listeyi döndür.
2. `reservoir(range(1, 100_001), 5, seed=7)` sonucunu sıralı olarak yazdır.
3. Eşitlik denemesi: `seed` 0'dan 999'a, her seferinde
   `reservoir(range(100), 5, seed)`. Seçilen öğelerden kaçı alt yarıda
   (`< 50`), kaçı üst yarıda; iki sayıyı aynı satıra yazdır.

**Beklenen çıktı:**

```
[3302, 26216, 31671, 61488, 88915]
2467 2533
```

İki yarı neredeyse eşit: hiçbir öğe kayırılmıyor.
