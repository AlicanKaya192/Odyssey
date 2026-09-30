## Tek sınıf, bütün aile

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(
    train,
    trend=None,              # None, "add", "mul"
    damped_trend=False,      # yalnizca trend varsa
    seasonal=None,           # None, "add", "mul"
    seasonal_periods=None,   # mevsimin boyu (satir sayisi)
)
fit = model.fit()
```

| Trend | Mevsim | Yaygın adı | Ne zaman |
|---|---|---|---|
| Yok | Yok | Basit üstel düzleştirme | Trendsiz, mevsimsiz, gürültülü düzey |
| `"add"` | Yok | Holt | Doğrusal trend |
| `"add"` + sönüm | Yok | Sönümlü Holt | Trend var ama sonsuza kadar sürmez |
| `"mul"` | Yok | Üstel trend | Yüzdeyle büyüme |
| Yok | `"add"` | Mevsimsel düzleştirme | Düzey + sabit boylu mevsim |
| `"add"` | `"add"` | Toplamsal Holt–Winters | Trend + sabit boylu mevsim |
| `"add"` | `"mul"` | Çarpımsal Holt–Winters | Trend + düzeyle büyüyen mevsim |
| `"mul"` | `"mul"` | Tam çarpımsal | Yüzdeyle büyüme + orantılı mevsim |

`train` düzenli aralıklı bir indeks taşımalı (`asfreq`), `NaN` içermemeli ve
en az **iki tam mevsim** uzunluğunda olmalı.

## Sonuç nesnesi

| Özellik | İçerik |
|---|---|
| `fit.params` | Katsayılar ve başlangıç değerleri (sözlük) |
| `fit.params["smoothing_level"]` | `α` |
| `fit.params["smoothing_trend"]` | `β` |
| `fit.params["smoothing_seasonal"]` | `γ` |
| `fit.params["damping_trend"]` | `φ` |
| `fit.level`, `fit.trend`, `fit.season` | Bileşenlerin eğitim boyunca değerleri |
| `fit.fittedvalues` | Eğitimdeki bir adımlık tahminler |
| `fit.resid` | Eğitimdeki kalıntılar |
| `fit.forecast(h)` | Sonraki `h` adımın tahmini (tarih indeksli seri) |
| `fit.aic` | Bilgi ölçütü: küçük olan daha iyi |

Kullanılmayan bileşenin katsayısı `nan` gelir.

## Güncelleme denklemleri

Toplamsal trend ve toplamsal mevsim için (mevsim boyu $m$):

$$\ell_t = \alpha\,(y_t - s_{t-m}) + (1 - \alpha)(\ell_{t-1} + b_{t-1})$$

$$b_t = \beta\,(\ell_t - \ell_{t-1}) + (1 - \beta)\,b_{t-1}$$

$$s_t = \gamma\,(y_t - \ell_t) + (1 - \gamma)\,s_{t-m}$$

$$\hat{y}_{t+h} = \ell_t + h\,b_t + s_{t+h-m}$$

Üçü de aynı kalıp: **yeni bilgi × katsayı + eski tahmin × (1 − katsayı)**.

- Düzey, mevsim payı çıkarılmış gözleme doğru çekilir.
- Eğim, düzeydeki son değişime doğru çekilir.
- Mevsim payı, gözlemin düzeyden sapmasına doğru çekilir.

Çarpımsal mevsimde çıkarma yerine bölme, toplama yerine çarpma gelir.

Sönümlü trendde tahmin:

$$\hat{y}_{t+h} = \ell_t + (\phi + \phi^2 + \dots + \phi^h)\,b_t$$

`φ = 1` sönümsüz; `φ = 0.9` ile eğimin etkisi on adımda üçte birine iner.

## Katsayıyı kendin vermek

```python
fit = model.fit(smoothing_level=0.2, optimized=False)
fit = model.fit(smoothing_level=0.2)     # alfa sabit, gerisi bulunur
```

Ne zaman? Çok sayıda seriyi aynı ayarla tahmin ederken, ya da çok kısa bir
seride bulunan katsayıya güvenmediğinde. Tipik elle seçimler: `α` 0.1–0.3,
`β` 0.05–0.2, `γ` 0.1–0.3.

## Model seçimi

Üç yol, güvenilirlik sırasıyla:

1. **Kayan başlangıç** (Bölüm 15): adayların örnek dışı hatası. En güvenilir;
   en pahalı.
2. **Bilgi ölçütü:** `fit.aic`. Uyumu ödüllendirir, katsayı sayısını
   cezalandırır. Yalnızca **aynı veride, aynı dönüşümle** kurulan modeller
   karşılaştırılır.
3. **Yapıya bakarak:** trend var mı, dalgalar büyüyor mu (Bölüm 10)?

Eğitim hatasına (`fit.resid`) bakarak seçme: bileşen ekledikçe hep küçülür.

## pandas ile hızlı düzleştirme

```python
s.ewm(alpha=0.2, adjust=False).mean()       # basit ustel duzlestirme duzeyi
s.ewm(span=10, adjust=False).mean()         # alfa = 2 / (span + 1)
s.ewm(halflife=5, adjust=False).mean()      # agirlik 5 adimda yariya iner
```

`adjust=False` dersteki güncelleme kuralının aynısı. Tek adımlı tahmin için
`shift(1)`: `s.ewm(alpha=0.2, adjust=False).mean().shift(1)`.

Hareketli ortalamayla (Bölüm 07) karşılaştırma:

| | `rolling(n).mean()` | `ewm(alpha=a).mean()` |
|---|---|---|
| Ağırlıklar | Son `n` gözlem eşit, öncesi sıfır | Hepsi, üstel azalan |
| Pencereden çıkan değer | Ani etki | Etki yok: ağırlık zaten küçülmüş |
| Başta `NaN` | `n − 1` tane | Yok |
| Kabaca eşdeğerlik | `n` | `α = 2 / (n + 1)` |
