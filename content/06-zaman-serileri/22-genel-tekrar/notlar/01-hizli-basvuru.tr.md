Patikanın bütün araçları, iş sırasıyla. Ayrıntı için ilgili bölümün notlarına
dön.

## Tarihi okumak

| İş | Kod |
|---|---|
| Metni tarihe çevir | `pd.to_datetime(s, format="%d.%m.%Y")` |
| Bozuk değerleri gör | `pd.to_datetime(s, errors="coerce")` → `NaT` |
| Okurken çevir | `pd.read_csv(f, index_col="date", parse_dates=True)` |
| Saat dilimi ver / çevir | `.dt.tz_localize("Europe/Istanbul")`, `.dt.tz_convert("UTC")` |
| Parçalar | `.dt.year`, `.dt.month`, `.dt.dayofweek`, `.dt.hour` |
| Biçimli metin | `.dt.strftime("%Y-%m-%d")` |

## Düzenli indeks

| İş | Kod |
|---|---|
| İndeks yap, sırala | `df.set_index("date").sort_index()` |
| Çiftleri at | `df.drop_duplicates()`, `s[~s.index.duplicated()]` |
| Düzenli sıklık | `s.asfreq("D")` |
| Tarih aralığı | `pd.date_range("2024-01-01", periods=28, freq="D")` |
| Dilimle | `s.loc["2024-03"]`, `s.loc["2024-03-01":"2024-03-15"]` |
| Dönem | `s.index.to_period("M")` |

Sıklık kısaltmaları: `h` saat, `D` gün, `B` iş günü, `W-SUN` hafta, `MS` / `ME`
ay başı / sonu, `QS` çeyrek, `YS` yıl.

## Özetlemek ve kaydırmak

| İş | Kod |
|---|---|
| Aşağı örnekle | `s.resample("MS").sum()` (akış), `.mean()` / `.last()` (durum) |
| Yukarı örnekle | `s.resample("h").ffill()`, `.interpolate()` |
| Haftanın günü profili | `s.groupby(s.index.dayofweek).mean()` |
| Geçmişi taşı | `s.shift(1)`, `s.shift(7)` |
| Değişim | `s.diff()`, `s.diff(7)`, `s.pct_change()` |
| Hareketli pencere | `s.rolling(7).mean()`; özellikte `s.shift(1).rolling(7).mean()` |
| Genişleyen / üstel | `s.expanding().mean()`, `s.ewm(alpha=0.3).mean()` |
| Uzun → geniş | `df.pivot(index="date", columns="store", values="sales")` |

## Tanı

| Soru | Kod |
|---|---|
| Bileşenler | `STL(s, period=7, robust=True).fit()` → `.trend`, `.seasonal`, `.resid` |
| Durağan mı | `adfuller(s)[1]` (küçük p: durağan), `kpss(s)[1]` (küçük p: değil) |
| Otokorelasyon | `acf(s, nlags=30)`, `pacf(s, nlags=30)`, `plot_acf(s)` |
| Kalıntı beyaz gürültü mü | `acorr_ljungbox(resid, lags=[14])` (büyük p: evet) |
| Varyansı dizginle | `np.log(s)`; geri dönüş `np.exp` |

## Eksik ve aykırı

| İş | Kod |
|---|---|
| Eksikleri say | `s.isna().sum()` |
| Kısa boşluk | `s.interpolate(limit=3)` |
| Mevsimli seri | `pd.concat([s.shift(7), s.shift(-7)], axis=1).mean(axis=1)` ile doldur |
| Dayanıklı puan | `0.6745 * (r - r.median()) / (r - r.median()).abs().median()` |

## Taban çizgi ve doğrulama

| İş | Kod |
|---|---|
| Naif | `train.iloc[-1]` |
| Mevsimsel naif | son `m` değeri tekrar et |
| MAE / RMSE | `np.abs(e).mean()`, `np.sqrt((e ** 2).mean())` |
| MASE | MAE / eğitimdeki mevsimsel naif MAE'si |
| Kayan başlangıç | kesim listesi; her kesimde `train = s.loc[:cut]`, sonraki `h` gün test |
| scikit-learn | `TimeSeriesSplit(n_splits=5)`; karıştırılmış `KFold` kullanma |

## Modeller

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA

fit = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=7).fit()
forecast = fit.forecast(28)

fit = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7), exog=x_train).fit()
result = fit.get_forecast(28, exog=x_future)
result.predicted_mean
result.conf_int(alpha=0.2)
```

Takvim özellikleri (gelecekte her zaman bilinir):

```python
angle = 2 * np.pi * index.dayofyear / 365.25
x["sin1"], x["cos1"] = np.sin(angle), np.cos(angle)      # yillik Fourier
x["dow"] = index.dayofweek                               # ya da gun kuklalari
x["t"] = (index - start).days                            # trend
```

Gecikme özellikleri her zaman `shift` ile; ufuk `h` ise en yeni gecikme `h`.

## Aralık

| İş | Kod |
|---|---|
| Deneysel | kayan başlangıç hatalarının `np.quantile(errors, [0.1, 0.9])` değeri |
| Kapsama | `((actual >= low) & (actual <= high)).mean()` |
| Pinball | `np.mean(np.maximum(q * d, (q - 1) * d))`, `d = actual - forecast` |
| Hangi yüzdelik | eksik maliyeti / (eksik + fazla maliyeti) |

## Anomali ve değişim

| İş | Kod |
|---|---|
| Canlı beklenti | `pd.concat([s.shift(7 * k) for k in (1, 2, 3, 4)], axis=1).median(axis=1)` |
| Tekrar uzunluğu | `same = s.diff() == 0`; `same.groupby((~same).cumsum()).sum() + 1` |
| CUSUM | `total = max(0, total + z - k)`; `total > h` ise alarm |
| Değişim günü | her kesim için iki parçanın kare toplamı; en küçüğü ve kazancı |

## Karar ağacı: hangi yöntem?

| Durum | İlk denenecek |
|---|---|
| Kısa seri, belirgin mevsim | Mevsimsel naif, Holt–Winters |
| Trend + tek mevsim, dış bilgi yok | Holt–Winters ya da mevsimsel ARIMA |
| İki mevsim (haftalık + yıllık) | Fourier terimli regresyon ya da ARIMA + Fourier |
| Bilinen dış etkenler (tatil, kampanya, fiyat) | Dış değişkenli regresyon / ARIMA |
| Çok özellik, doğrusal olmayan etkiler | Ağaç modelleri (hedef farkta) |
| Rastgele yürüyüş (fiyat) | Naif; asıl iş aralık |
