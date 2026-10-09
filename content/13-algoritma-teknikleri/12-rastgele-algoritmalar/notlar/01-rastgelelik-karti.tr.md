## Python'un `random` modülü

| İş | Nasıl | Not |
|---|---|---|
| Tohum | `random.seed(42)` | aynı tohum, aynı dizi |
| Tek seçim | `random.choice(xs)` | |
| Yerine koymadan `k` öğe | `random.sample(xs, k)` | aynı öğe iki kez gelmez |
| Yerine koyarak `k` öğe | `random.choices(xs, k=k)` | ağırlık da verilebilir: `weights=` |
| Yerinde karıştır | `random.shuffle(xs)` | Fisher-Yates, `None` döndürür |
| Tam sayı | `random.randint(a, b)` | `b` **dahil** |
| Kesir | `random.random()` | `0 <= x < 1` |

NumPy'de: `rng = np.random.default_rng(42)`, sonra `rng.integers`,
`rng.choice`, `rng.permutation`. scikit-learn'de `random_state=42`.

## Algoritmalar

| Algoritma | Tür | Maliyet |
|---|---|---|
| Quickselect (rastgele pivot) | Las Vegas | ortalama `O(n)` |
| Fisher-Yates | | `O(n)` |
| Rezervuar örnekleme | | `O(n)` zaman, `O(k)` bellek |
| Monte Carlo tahmini | Monte Carlo | hata `1/√n` gibi |

## Sık hatalar

- `xs = random.shuffle(xs)`: `shuffle` listeyi yerinde değiştirir ve `None`
  döndürür; `xs` artık `None`.
- `randint(0, len(xs))`: üst sınır dahil olduğu için bir fazla, indeks hatası.
- Karıştırırken her konumu bütün listeden seçmek: yanlı karıştırma.
- Tohumu döngünün içinde vermek: her turda aynı "rastgele" sayı.
- Rastgele bir sonucu tek denemeyle yorumlamak: Monte Carlo'da tek deneme şans
  payı taşır; birkaç tekrarın ortalamasına bak.
