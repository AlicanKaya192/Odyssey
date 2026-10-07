Örnekleme ve yaklaşık hesap için formüller ve kod.

## Örneklem almak

```python
df.sample(n=10_000, random_state=42)          # tam 10 000 satır
df.sample(frac=0.01, random_state=42)         # yüzde bir
df.groupby("city", group_keys=False).sample(n=200, random_state=0)  # katmanlı
```

## Standart hata ve güven aralığı

```text
standart hata (SE) = s / √n            (s: örneklemin standart sapması)
%95 güven aralığı  = tahmin ± 1,96 × SE
```

```python
se = s["unit_price"].std() / np.sqrt(len(s))
low, high = s["unit_price"].mean() - 1.96 * se, s["unit_price"].mean() + 1.96 * se
```

## Kaç satır gerekir?

Ortalamayı ± E hata payıyla (%95 güvenle) tahmin etmek için:

```text
n ≈ (1,96 × σ / E)²
```

σ verinin standart sapması (bilmiyorsan küçük bir ön örneklemden tahmin et).
Sipariş fiyatlarında σ = 841,6:

| İstenen hata payı (E) | Gereken örneklem |
|---|---|
| ± 50 TL | 1 089 |
| ± 20 TL | 6 803 |
| ± 10 TL | 27 209 |
| ± 5 TL | 108 834 |

Hatayı yarıya indirmek dört kat veri istiyor.

## Bu patikanın ölçümleri

| Örneklem | Tahminlerin dağılımı (TL) |
|---|---|
| 100 | 87,6 |
| 1 000 | 25,8 |
| 10 000 | 8,2 |
| 100 000 | 2,4 |

200 güven aralığının 191'i (%95,5) gerçek ortalamayı içerdi.

## Okurken örneklemek

```python
rng = random.Random(42)
pd.read_csv("orders.csv", skiprows=lambda i: i > 0 and rng.random() > 0.01)
```

## Rezervuar örneklemesi

```python
def reservoir(items, k, seed):
    rng = random.Random(seed)
    sample = []
    for i, item in enumerate(items):
        if i < k:
            sample.append(item)
        else:
            j = rng.randint(0, i)
            if j < k:
                sample[j] = item
    return sample
```

## DuckDB

```sql
... USING SAMPLE 1% (bernoulli, 42)     -- yüzde bir, tohum 42
... USING SAMPLE 10000 ROWS             -- tam 10 000 satır
approx_count_distinct(x)                -- yaklaşık farklı değer sayısı
approx_quantile(x, 0.5)                 -- yaklaşık ortanca
```
