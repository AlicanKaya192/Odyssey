## Hangi soruya hangi yapı?

| Soru | Yapı | Kesin karşılığı |
|---|---|---|
| Bu öğe daha önce geldi mi? | Bloom filtresi | `set` |
| Bu öğe kaç kez geldi? | Count-Min sketch | `Counter` / `dict` |
| Kaç farklı öğe geldi? | HyperLogLog | `len(set(...))` |
| İki küme ne kadar benzer? | MinHash (+ LSH) | Jaccard, bütün kümelerle |

## Hata yönleri

- **Bloom:** yanlış pozitif olabilir, yanlış negatif olmaz. Silme desteklemez
  (bir biti sıfırlamak başka öğeleri de siler).
- **Count-Min:** hep fazla tahmin eder; az geçen öğelerde göreli hata büyük.
- **HyperLogLog:** iki yöne de yanılabilir; hata yaklaşık `1.04/√m`.
- **MinHash:** iki yöne de yanılabilir; imza boyu `k` arttıkça hata
  `1/√k` gibi küçülür.

## Birleştirilebilirlik

Hepsi **birleştirilebilir**: iki sunucunun Bloom filtreleri bit bit `or`,
Count-Min tabloları hücre hücre toplam, HyperLogLog kovaları kova kova `max`,
MinHash imzaları sıra sıra `min` ile birleşir. Dağıtık sistemlerde her makine
kendi özetini tutup sonunda birleştirmek bu yüzden mümkün.

## Sık hatalar

- Python'un `hash()`'ini kullanmak: metin için her çalıştırmada değişebilir,
  kaydedilen filtre ertesi gün işe yaramaz. `hashlib` kullan.
- Tek hash fonksiyonunu `k` kez kullanmak: `k` farklı tohum gerekir.
- Bloom filtresini öngörülenden çok fazla öğeyle doldurmak: yanlış pozitif
  oranı hızla tırmanır; boyutu baştan beklenen öğe sayısına göre seç.
