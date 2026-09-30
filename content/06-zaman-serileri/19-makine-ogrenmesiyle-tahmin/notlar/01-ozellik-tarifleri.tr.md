## Gecikmeler

```python
for k in (1, 7, 14, 28):
    X[f"lag{k}"] = y.shift(k)
```

Hangi gecikmeler? ACF ve PACF'de bandı aşanlar (Bölüm 12), artı mevsimin
katları (7, 14, 28; 12, 24).

`h` adım ilerisini tahmin ediyorsan en küçük gecikme `h` olmalı.

## Pencereler

```python
past = y.shift(1)                         # once kaydir

X["mean7"] = past.rolling(7).mean()       # yakin duzey
X["mean28"] = past.rolling(28).mean()     # uzun duzey
X["std7"] = past.rolling(7).std()         # yakin oynaklik
X["max7"] = past.rolling(7).max()
X["trend"] = X["mean7"] - X["mean28"]     # duzey yukseliyor mu?
X["ewm"] = past.ewm(alpha=0.3, adjust=False).mean()
```

Mevsimsel pencere: aynı konumun geçmiş değerleri.

```python
X["same_dow_4w"] = sum(y.shift(7 * i) for i in range(1, 5)) / 4
```

## Takvim

```python
X["dow"] = index.dayofweek
X["month"] = index.month
X["day"] = index.day
X["weekend"] = (index.dayofweek >= 5).astype(int)
X["holiday"] = index.isin(holiday_dates).astype(int)
```

| Model | Haftanın günü nasıl verilir |
|---|---|
| Ağaç tabanlı | Sayı olarak (0–6) yeter; ağaç eşikleri kendisi bulur |
| Doğrusal | **Kukla sütunlar**: `pd.get_dummies(X["dow"], drop_first=True)` |

Doğrusal modele haftanın gününü 0–6 sayısı olarak vermek "pazar, pazartesinin
altı katı" demektir. Kukla sütunlara çevir.

Döngüsel değişkenler (ay, saat) için sinüs ve kosinüs: Aralık ile Ocak komşu
kalır.

## Hedefi dönüştürmek

| Dönüşüm | Hedef | Geri dönüş | Ne zaman |
|---|---|---|---|
| Fark | `y - y.shift(m)` | `+ lag_m` | Trendli seri, ağaç tabanlı model |
| Oran | `y / y.shift(m)` | `× lag_m` | Çarpımsal büyüme |
| Logaritma | `np.log(y)` | `np.exp` | Büyüyen varyans |
| Düzeye oran | `y / mean28` | `× mean28` | Farklı ölçekli çok seri |

Özellikleri de aynı tabana göre yazmak iyi olur: `lag1 - lag7`, `mean7 -
lag7`. Böylece model hiçbir yerde ham düzeyi görmez.

## Çok adımlı tahmin

**Özyinelemeli:**

```python
history = train.copy().astype(float)
for day in future_index:
    history.loc[day] = float("nan")
    row = features(history).loc[[day]]
    history.loc[day] = model.predict(row[columns])[0]
forecast = history.loc[future_index]
```

Her adımda tablo yeniden kuruluyor; tahminler bir sonraki adımın gecikmesi
oluyor. Hata birikir; dış değişkenlerin geleceği her adım için gerekir.

**Doğrudan, güvenli özellikler:** bütün gecikme ve pencereleri en az `h` kadar
kaydır. Tek model, tek `predict`. Yakın ufuk için elde olan taze bilgiyi
kullanmaz.

**Ufuk başına model:**

```python
models = {}
for h in (1, 7, 14, 28):
    target = y.shift(-h)                  # h gun sonraki deger (yalnizca egitimde)
    rows = X.join(target.rename("target")).dropna()
    models[h] = Model().fit(rows[columns], rows["target"])
```

`shift(-h)` burada sızıntı değil: hedefi tanımlıyor, özellik değil. Her ufuk
elindeki en taze bilgiyi kullanır; bedeli `h` tane model.

## Çok seri, tek model

Yüzlerce ürün varsa uzun biçimdeki tabloya (Bölüm 08) özellikleri **seri
başına** ekle:

```python
long["lag7"] = long.groupby("store")["sales"].shift(7)
long["mean28"] = (long.groupby("store")["sales"]
                      .transform(lambda v: v.shift(1).rolling(28).mean()))
```

`groupby` olmadan `shift`, bir mağazanın son satırını ötekinin ilk satırına
taşır. Mağaza kimliği de bir özellik olur; ölçekler farklıysa hedefi düzeye
oranla.

## Denetim listesi

1. Her özellik `shift` ile en az ufuk kadar geriden mi geliyor?
2. `rolling`, `ewm`, `expanding`'den önce `shift` var mı?
3. Ölçekleme, kodlama, doldurma yalnızca eğitimde mi `fit` edildi?
4. Doğrulama zamana göre mi?
5. Test, eğitimden **sonra** mı ve arada ufuk kadar boşluk gerekiyor mu
   (`gap`)?
6. Eğitim ve test hatası arasındaki fark makul mü?
7. Temel yöntem aynı düzenekte kaç veriyor?
