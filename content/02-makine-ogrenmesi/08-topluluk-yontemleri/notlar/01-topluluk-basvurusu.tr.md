## Rastgele orman

```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

model = RandomForestClassifier(n_estimators=200, random_state=42)
```

| Parametre | Ne yapıyor | Varsayılan |
|---|---|---|
| `n_estimators` | Kaç ağaç | 100 |
| `max_depth` | Her ağacın derinliği | `None` |
| `min_samples_leaf` | Yaprakta en az kaç kayıt | 1 |
| `max_features` | Her bölünmede denenecek özellik sayısı | `sqrt` |
| `bootstrap` | Örneklem yerine koyarak mı çekilsin | `True` |
| `oob_score` | Torba dışı skoru hesaplasın mı | `False` |
| `n_jobs` | Kaç çekirdek kullanılsın (`-1` hepsi) | `None` |
| `class_weight` | Dengesiz veride sınıf ağırlığı | `None` |

**`max_features` ormanın kalbi.** Her bölünmede özelliklerin yalnızca bir
alt kümesi deneniyor; bu, ağaçları birbirinden farklılaştırıyor. Hepsini
denemek ormanı basit torbalamaya çeviriyor ve ağaçlar birbirine benziyor.

**`n_estimators` aşırı öğrenme parametresi değil.** Artırmak sonucu
kötüleştirmiyor, yalnızca yavaşlatıyor. Ölçüldü: 25 ağaçta 0.90, 300 ağaçta
yine 0.90.

## Gradyan artırma

```python
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier(
    n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
```

| Parametre | Ne yapıyor |
|---|---|
| `n_estimators` | Kaç tur düzeltme |
| `learning_rate` | Her turun katkısı; küçük = güvenli ama yavaş |
| `max_depth` | Ağaçlar **sığ** tutuluyor (2-5 tipik) |
| `subsample` | Her turda verinin bir kısmı (< 1 ise stokastik) |

**`n_estimators` ile `learning_rate` birlikte ayarlanıyor.** Biri
düşerse öteki yükselmeli. Kaba bir başlangıç: `learning_rate=0.1` ve
`n_estimators=100`.

**Artırma aşırı öğrenebiliyor** — ormandan farklı olarak. Ağaç sayısını
artırmak bir noktadan sonra test skorunu düşürüyor.

Daha hızlısı:

```python
from sklearn.ensemble import HistGradientBoostingClassifier

model = HistGradientBoostingClassifier(random_state=42)
```

Büyük veride çok daha hızlı ve **eksik değerle çalışabiliyor** — sklearn'de
bunu yapabilen ender modellerden.

## İkisi arasındaki fark

| | Orman | Artırma |
|---|---|---|
| Ağaçlar | Paralel, bağımsız | Sırayla, birbirini düzelten |
| Ağaç derinliği | Derin | Sığ |
| Azalttığı | Varyans | Yanlılık |
| Aşırı öğrenme | Ağaç sayısıyla artmıyor | Artabiliyor |
| Ayar | Az; varsayılan iyi çalışıyor | Çok; birlikte ayarlanıyor |
| Hız | Paralelleşebiliyor (`n_jobs`) | Sıralı, paralelleşmiyor |

## Torba dışı skor (OOB)

```python
model = RandomForestClassifier(n_estimators=200, oob_score=True,
                               random_state=42)
model.fit(X_train, y_train)
print(round(float(model.oob_score_), 3))
```

Her ağaç eğitim verisinin yaklaşık **üçte birini** görmüyor; o satırlar
üzerinden skor hesaplanıyor. Ayrı doğrulama kümesi ayırmadan bir tahmin
veriyor.

Sınırları: yalnızca `bootstrap=True` iken çalışıyor, az ağaçta güvenilmez
oluyor ve **test kümesinin yerini almıyor**.

## Özellik önemi

```python
for name, value in zip(X.columns, model.feature_importances_):
    print(name, round(float(value), 3))
```

Ormanın önemi tek ağacınkinden **daha kararlı**: yüzlerce ağacın ortalaması
alınıyor ve her özellik defalarca deneniyor. Ölçüldü: tek ağaç `age`
sütununa 0.0 verirken orman 0.232 veriyor.

Aynı üç tuzak yine geçerli: sebep değil, ilişkili sütunlar önemi paylaşıyor,
çok değerli sütunlar şişiyor. Daha güvenilir yol yine
`permutation_importance`.

## Hız

```python
RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
```

`n_jobs=-1` bütün çekirdekleri kullanıyor. Ağaçlar bağımsız olduğu için
orman iyi paralelleşiyor; **artırma paralelleşmiyor**, çünkü her ağaç
öncekini bekliyor.

## Sık yapılan hatalar

- **`n_estimators`'ı aşırı öğrenme sanmak.** Ormanda artırmak zararsız.
- **Artırmada ağaç sayısını sınırsız artırmak.** Orada aşırı öğrenme
  gerçek.
- **Tek test skoruna bakıp topluluk gereksiz demek.** Ölçüldü: tek ayrımda
  ağaç 0.96 ile kazanıyor, çapraz doğrulamada 0.827 ile kaybediyor.
- **Ormanı ölçeklemek.** İçindekilerin hepsi ağaç; gereksiz.
- **`random_state` vermemek.** Orman baştan sona rastgelelik üzerine
  kurulu; vermezsen sonuç tekrar edilemiyor.
- **Yorumlanabilirlik beklemek.** 200 ağacın kuralı cümleye çevrilemiyor.
- **`oob_score`'u test skoru yerine koymak.** OOB eğitim verisinden
  geliyor.
