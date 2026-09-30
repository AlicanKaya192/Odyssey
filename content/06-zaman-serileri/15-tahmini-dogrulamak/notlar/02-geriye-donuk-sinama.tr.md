## Düzeneğin dört ayarı

| Ayar | Soru | Tipik seçim |
|---|---|---|
| Ufuk (`h`) | Gerçekte kaç adım ileriyi tahmin edeceğim? | Kararın ufku: 7, 28, 12 |
| Adım (`step`) | Başlangıçlar arasında kaç adım olsun? | `h` (çakışmayan testler) ya da 1 mevsim |
| Deney sayısı | Kaç başlangıç? | En az 5–10; mümkünse bir tam yılı kapsasın |
| Pencere | Eğitim ne kadar geriye gitsin? | Genişleyen; seri değişiyorsa kayan |

İlk başlangıçtan önce modelin öğrenebileceği kadar veri kalmalı: en az iki tam
mevsim.

## Genel işlev

```python
import numpy as np
import pandas as pd


def backtest(y, forecast, first, step, h, count, window=None):
    rows = []
    for i in range(count):
        cut = pd.Timestamp(first) + step * i * y.index.freq
        train = y.loc[:cut]
        if window is not None:
            train = train.iloc[-window:]
        test = y.loc[cut:].iloc[1:h + 1]
        if len(test) < h:
            break
        predicted = np.asarray(forecast(train, h), dtype=float)
        rows.append({
            "cut": cut,
            "mae": np.mean(np.abs(test.to_numpy() - predicted)),
            "bias": np.mean(test.to_numpy() - predicted),
        })
    return pd.DataFrame(rows).set_index("cut")
```

- `step * i * y.index.freq` her sıklıkta çalışır (günlük, aylık); seri
  `asfreq` ile düzenli olmalı.
- `window=None` genişleyen pencere; bir sayı verilirse kayan pencere.
- `forecast(train, h)` yalnızca `train`'i görüyor. Mevsim çarpanı, ortalama,
  doldurma gibi her hesap **bu fonksiyonun içinde** yapılmalı.

Kullanım:

```python
table = backtest(s, snaive, "2024-01-02", step=28, h=28, count=13)
print(table["mae"].agg(["mean", "std", "min", "max"]).round(2))
```

## Çakışan ve çakışmayan testler

| | Çakışmayan (`step = h`) | Çakışan (`step < h`) |
|---|---|---|
| Deney sayısı | Az | Çok |
| Deneyler bağımsız mı | Büyük ölçüde | Hayır: aynı günler birçok testte |
| Ne zaman | Veri bolsa | Veri kısaysa; ufka göre hata isteniyorsa |

Çakışan testlerde ortalama daha kararlı görünür, ama deneyler birbirinden
bağımsız olmadığı için standart sapma gerçek belirsizliği **küçümser**.

## Ne raporlanır

```python
table["mae"].mean()             # tipik basari
table["mae"].std()              # donemden doneme oynaklik
table["mae"].max()              # en kotu donem
table["mae"].idxmax()           # ne zaman
table["bias"].mean()            # sistematik kayma
```

En kötü deneyin **ne zaman** olduğuna bak: hep aynı mevsimdeyse (yıl sonu,
bayram haftası) model o dönemi bilmiyordur ve çözüm bir takvim değişkenidir
(Bölüm 18), daha karmaşık bir model değil.

## İki yöntemi karşılaştırmak

Aynı başlangıçlar, aynı ufuk, aynı ölçü. Sonra deney deney farka bak:

```python
diff = table_a["mae"] - table_b["mae"]
print(round(diff.mean(), 2), round(diff.std(), 2), int((diff < 0).sum()), len(diff))
```

- Farkın ortalaması, farkın standart sapmasına göre küçükse: berabere.
- A, deneylerin yarısı civarında kazanıyorsa: berabere.
- A, deneylerin neredeyse hepsinde kazanıyorsa ve fark kayda değerse: A daha iyi.

Berabere kalan iki yöntemden **basit olanı** seç.

## Doğrulama ve test

```text
|----------- egitim -----------|--- dogrulama deneyleri ---|--- test deneyleri ---|
                                 ayar burada secilir          bir kez, en sonda
```

- Ayar denemelerinin hepsi doğrulama deneylerinde.
- Test deneylerine en sonda, **tek bir** aday için bakılır.
- Test sonucunu görüp ayar değiştirdiysen yeni bir test dönemine ihtiyacın var.
- Son kullanım için model, doğrulama ve test dahil **bütün veriyle** yeniden
  eğitilir.

## `TimeSeriesSplit`

```python
from sklearn.model_selection import TimeSeriesSplit

splitter = TimeSeriesSplit(n_splits=5, test_size=28, gap=0, max_train_size=None)
```

| Argüman | Anlamı |
|---|---|
| `n_splits` | Deney sayısı |
| `test_size` | Her testin uzunluğu (ufuk) |
| `gap` | Eğitimin sonu ile testin başı arasında atlanan satır sayısı |
| `max_train_size` | Verilirse kayan pencere; verilmezse genişleyen |

`gap` ne için? 7 gün sonrasını tahmin eden bir modelin özelliklerinde dünkü
değer varsa, test gününden önceki 6 gün tahmin anında bilinmiyordur. `gap=6`
o günleri eğitimden de testten de çıkarır.

Satır **konumu** döndürür, tarih değil: `s.iloc[train_idx]`. Seri sıralı ve
düzenli aralıklı olmalı.

## Sızıntı belirtileri

- Test hatası, eğitim hatasından **küçük**.
- Çok adımlı hata, tek adımlı hatayla neredeyse aynı.
- Karmaşık model temel yöntemi inanılmaz bir farkla geçiyor (beceri > 0.8).
- Gerçek kullanıma geçince hata bir anda katlanıyor.

Birini görürsen düzeneği satır satır izle: `forecast` fonksiyonuna giren her
sayının tarihi `cut`'tan büyük olmamalı.
