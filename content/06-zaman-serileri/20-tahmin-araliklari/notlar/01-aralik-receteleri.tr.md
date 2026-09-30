## Dört yol

| Yol | Nasıl | Artısı | Eksisi |
|---|---|---|---|
| Deneysel | Örnek dışı hataların yüzdelikleri | Varsayımsız; her yöntemle çalışır | Yeterli sayıda geçmiş hata ister |
| Formül | tahmin ± `z` × hata standart sapması | Basit | Normal dağılım ve sıfır yanlılık varsayar |
| Model | `get_forecast(h).conf_int(alpha)` | Hazır; ufka göre genişler | Model yanlışsa fazla dar |
| Yüzdelik modeli | Doğrudan yüzdeliği öğrenen model | Aralığın boyu koşula göre değişir | Her yüzdelik için ayrı model |

## Deneysel aralık, ufka göre

Kayan başlangıçtaki hataları ufuk ufuk sakla; her ufkun kendi yüzdeliğini al.

```python
errors = []                                   # her deney icin h uzunlugunda hata dizisi
for cut in cuts:
    train = s.loc[:cut]
    test = s.loc[cut + pd.Timedelta(days=1):].iloc[:h]
    errors.append(test.to_numpy() - forecast(train, h))
errors = np.array(errors)                     # (deney sayisi, h)

low = np.quantile(errors, 0.10, axis=0)       # her ufuk icin ayri
high = np.quantile(errors, 0.90, axis=0)

point = forecast(s, h)
interval_low, interval_high = point + low, point + high
```

Az deney varsa ufukları öbekle (hafta hafta) ya da bütün ufukları birleştir;
on üç hatadan yüzdelik çıkarmak güvenilmez.

## Formülle genişleme

| Yöntem | `h` adım sonraki hatanın standart sapması |
|---|---|
| Ortalama | `σ` (sabit) |
| Naif | `σ √h` |
| Mevsimsel naif | `σ √(k + 1)`; `k`, tamamlanmış mevsim sayısı |
| Kayma | `σ √(h (1 + h / T))` |

`σ`, bir adımlık hatanın standart sapması; `T`, eğitim uzunluğu. Bunlar
hataların birbirinden bağımsız olduğunu varsayar; gerçek serilerde genişleme
çoğu zaman daha yavaştır (günlük satışta mevsimsel naif: 17.0, 18.2, 19.5,
21.3; formül 17.0, 24.0, 29.4, 33.9 derdi). **Formüle güvenme, ölç.**

## statsmodels

```python
result = fit.get_forecast(h, exog=future)     # exog yalnizca dis degiskenli modelde
result.predicted_mean
result.conf_int(alpha=0.2)                    # iki sutun: alt, ust
result.se_mean                                # her ufkun standart hatasi
```

Logaritmalı modelde uçları da geri çevir:

```python
interval = np.exp(result.conf_int(alpha=0.05))
```

`ExponentialSmoothing` (Bölüm 16) aralık vermez; onun için deneysel yol ya da
`statsmodels.tsa.exponential_smoothing.ets.ETSModel`.

## Kapsamayı ölçmek

```python
inside = (actual >= low) & (actual <= high)
coverage = inside.mean()
width = (high - low).mean()
```

İkisi birlikte okunur:

| Kapsama | Genişlik | Yorum |
|---|---|---|
| Söylenene yakın | Dar | İyi aralık |
| Söylenene yakın | Çok geniş | Dürüst ama işe yaramaz |
| Söylenenden düşük | Dar | Aşırı güvenli; model bir şeyi bilmiyor |
| Söylenenden yüksek | Geniş | Fazla temkinli; daraltılabilir |

Sonsuz genişlikte bir aralık her zaman %100 kapsar. Amaç, **söylenen kapsamayı
tutan en dar aralık**.

Kapsamaya dönem dönem de bak: ortalaması doğru ama hep aynı dönemde çöken bir
aralık (derste yıl dönümü) bir eksik değişkene işaret eder.

## Yüzdelik ve pinball

```python
def pinball(actual, forecast, q):
    diff = actual - forecast
    return np.mean(np.maximum(q * diff, (q - 1) * diff))
```

| `q` | Eksik tahminin cezası | Fazla tahminin cezası |
|---|---|---|
| 0.5 | 0.5 | 0.5 |
| 0.8 | 0.8 | 0.2 |
| 0.9 | 0.9 | 0.1 |

Doğrudan yüzdelik öğrenen modeller:

```python
from sklearn.ensemble import HistGradientBoostingRegressor

model = HistGradientBoostingRegressor(loss="quantile", quantile=0.9)
```

Bölüm 19'daki özellik tablosuyla kullanılır; ağacın düzeyi uzatamama sorunu
burada da geçerli (hedefi farka çevir).

## Hangi yüzdelik?

$$q = \frac{c_{\text{eksik}}}{c_{\text{eksik}} + c_{\text{fazla}}}$$

| Durum | Eksik : fazla maliyeti | `q` |
|---|---|---|
| Taze ürün, ucuz; raf boş kalmasın | 4 : 1 | 0.80 |
| Pahalı, çabuk bozulan ürün | 1 : 3 | 0.25 |
| Hastane malzemesi | 50 : 1 | 0.98 |
| Maliyetler eşit | 1 : 1 | 0.50 |

Yüksek bir **hizmet düzeyi** ("stok %95 yetsin") doğrudan `q = 0.95` demek;
bedeli, eklenen güvenlik payı kadar fazla stok.

## Sunarken

- İki aralık ver: %80 (olağan oynama) ve %95 (kötü gün).
- Grafikte bant olarak çiz: `ax.fill_between(index, low, high, alpha=0.2)`.
- "Aralık" de, "garanti" deme: %95'lik aralık yirmi günde bir aşılır, bu
  beklenen bir şeydir.
- Kapsamanın geçmişte ne tuttuğunu yanına yaz: "%95 dedik, son bir yılda %87
  tuttu."
