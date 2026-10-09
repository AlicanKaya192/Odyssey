## Sayı üretmek

| Fonksiyon | Ne verir |
|---|---|
| `random()` | `[0, 1)` aralığında ondalık |
| `uniform(a, b)` | `a` ile `b` arasında ondalık |
| `randint(a, b)` | `a` ile `b` arasında tam sayı, **ikisi de dahil** |
| `randrange(a, b, adım)` | `range(a, b, adım)` içinden biri; `b` dahil değil |
| `gauss(mu, sigma)` | normal dağılım |
| `expovariate(lambd)` | üstel dağılım (bekleme süreleri) |

## Seçmek ve karıştırmak

| Fonksiyon | Ne yapar | Tekrar olur mu? |
|---|---|---|
| `choice(xs)` | tek eleman | — |
| `choices(xs, weights=..., k=n)` | `n` seçim | evet (yerine koyarak) |
| `sample(xs, n)` | `n` farklı eleman | hayır |
| `shuffle(xs)` | listeyi yerinde karıştırır, `None` döndürür | — |

## Tekrarlanabilirlik

- `random.seed(n)`: paylaşılan üreteci ayarlar (bütün program etkilenir).
- `r = random.Random(n)`: yalnızca senin kullandığın ayrı üreteç; testte ve
  deneylerde tercih edilir.
- Aynı tohum + aynı çağrı sırası = aynı sonuç. Araya bir çağrı eklemek
  sonraki bütün sayıları değiştirir.

## Sık hatalar

- `shuffle`'ın sonucunu bir değişkene atamak: `x = random.shuffle(xs)` →
  `x` `None`. Karışık bir **kopya** gerekiyorsa `r.sample(xs, len(xs))`.
- `randint(1, 6)`'da 6'nın dahil olduğunu unutmak; `randrange(1, 6)`'da 6
  dahil değildir.
- Güvenlik gerektiren kodda `random` kullanmak: `secrets`.
