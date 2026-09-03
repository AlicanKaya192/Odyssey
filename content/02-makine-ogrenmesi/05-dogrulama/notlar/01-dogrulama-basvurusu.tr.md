## Çapraz doğrulama

```python
from sklearn.model_selection import KFold, cross_val_score

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=kf,
                         scoring="neg_mean_absolute_error")

print([round(-s, 2) for s in scores])
print(round(-scores.mean(), 2), round(scores.std(), 2))
```

| Parametre | Ne yapıyor |
|---|---|
| `n_splits` | Kaç parçaya bölüneceği (5 ve 10 yaygın) |
| `shuffle` | Bölmeden önce karıştırma; sıralı dosyalarda gerekli |
| `random_state` | `shuffle=True` ile birlikte sonucu sabitliyor |

**Kaç kat:** 5 hızlı ve genelde yeterli. 10 daha güvenilir ama iki kat
pahalı. Veri çok azsa kat sayısı kayıt sayısına kadar çıkabiliyor
(`LeaveOneOut`).

## Katlama türleri

| Sınıf | Ne zaman |
|---|---|
| `KFold` | Regresyon, sıradan durum |
| `StratifiedKFold` | Sınıflandırma; her kat sınıf oranını koruyor |
| `TimeSeriesSplit` | Zaman serisi; geçmiş eğitim, gelecek test |
| `GroupKFold` | Aynı gruba ait kayıtlar (aynı hasta, aynı müşteri) ayrılmasın diye |

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
```

**`cross_val_score` sınıflandırmada varsayılan olarak zaten
`StratifiedKFold` kullanıyor** — ama `cv=kf` diye açıkça `KFold` verirsen o
korumayı kendi elinle kapatmış oluyorsun.

## Skor adları

`scoring` bir metin alıyor ve **büyük olan iyidir** kuralına göre çalışıyor.
Hata ölçüleri bu yüzden negatif geliyor.

| `scoring` | Ne veriyor |
|---|---|
| `neg_mean_absolute_error` | -MAE |
| `neg_root_mean_squared_error` | -RMSE |
| `r2` | R² (zaten büyük olan iyi) |
| `accuracy` | Doğruluk |
| `precision`, `recall`, `f1` | Sınıflandırma ölçüleri |
| `roc_auc` | Eğri altındaki alan |

```python
print(round(-scores.mean(), 2))    # hata olculerinde isaret cevriliyor
print(round(scores.mean(), 3))     # r2 ve accuracy'de cevrilmiyor
```

## Daha fazla bilgi: `cross_validate`

```python
from sklearn.model_selection import cross_validate

result = cross_validate(model, X, y, cv=kf,
                        scoring=["neg_mean_absolute_error", "r2"],
                        return_train_score=True)

print(result["test_neg_mean_absolute_error"])
print(result["train_neg_mean_absolute_error"])
```

`return_train_score=True` **eğitim skorlarını da** veriyor — aşırı öğrenmeyi
görmek için gereken şey tam olarak bu.

Birden çok ölçüyü tek çalıştırmada alabiliyorsun; her biri
`test_<ad>` anahtarıyla dönüyor.

## Öğrenme eğrisi

Elle:

```python
sizes = [10, 20, 30, 45, 60, 79]
for n in sizes:
    model.fit(X_train[:n], y_train[:n])
    train_error = mean_absolute_error(y_train[:n], model.predict(X_train[:n]))
    test_error = mean_absolute_error(y_test, model.predict(X_test))
```

sklearn ile:

```python
from sklearn.model_selection import learning_curve

sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=kf, scoring="neg_mean_absolute_error",
    train_sizes=[0.2, 0.4, 0.6, 0.8, 1.0])
```

`learning_curve` her boyut için **çapraz doğrulama** yapıyor, o yüzden
elle yazılandan daha güvenilir; karşılığında daha yavaş.

## Okuma

| Görünen | Teşhis | Yapılacak |
|---|---|---|
| Eğitim düşük, test yüksek, arada büyük açıklık | Aşırı öğrenme | Modeli basitleştir, veri ekle, düzenlileştir |
| İkisi de yüksek ve yakın | Yetersiz öğrenme | Modeli karmaşıklaştır, özellik ekle |
| İkisi de düşük ve yakın | İyi | Bir şey yapma |
| Eğriler buluştu, hâlâ yüksek | Veri sınırına gelinmiş | Yeni **özellik** ya da farklı model |
| Eğriler arasında açıklık kapanmıyor | Veri az | **Daha çok veri** işe yarar |

## Ayar seçme sırası

```python
# 1. Testi bir kenara koy
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 2. Ayarlari EGITIM tarafinda capraz dogrulamayla sec
best_score, best_depth = None, None
for depth in (2, 3, 5, 8, None):
    scores = cross_val_score(
        DecisionTreeRegressor(max_depth=depth, random_state=42),
        X_train, y_train, cv=kf, scoring="neg_mean_absolute_error")
    if best_score is None or scores.mean() > best_score:
        best_score, best_depth = scores.mean(), depth

# 3. Secilen ayarla butun egitim verisinde egit
model = DecisionTreeRegressor(max_depth=best_depth, random_state=42)
model.fit(X_train, y_train)

# 4. Teste BIR KEZ bak
print(mean_absolute_error(y_test, model.predict(X_test)))
```

Dördüncü adımdaki sayı rapora giren sayı. Ondan sonra ayar değiştirip
tekrar bakmak, test kümesini tüketiyor.

## Sık yapılan hatalar

- **Ayarı test kümesine bakarak seçmek.** Test artık eğitim verisi.
- **Çapraz doğrulamayı bütün veride yapıp sonra aynı veride test etmek.**
  Sızıntı; test kümesi ayrı durmalı.
- **Yalnızca ortalamaya bakmak.** Yayılım (std) sayının ne kadar
  oynadığını söylüyor; küçük farklar yayılımın içinde kaybolabiliyor.
- **Sınıflandırmada `KFold` kullanmak.** Dengesiz veride bir kat azınlık
  sınıfından hiç kayıt almayabiliyor.
- **`shuffle=True` ile `random_state` vermemek.** Her çalıştırmada farklı
  katlar, farklı sonuç.
- **Zaman serisinde rastgele katlama.** Gelecek geçmişe sızıyor.
