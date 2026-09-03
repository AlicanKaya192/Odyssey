## Kurulum

```python
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model = DecisionTreeRegressor(max_depth=3, random_state=42)
```

| Parametre | Ne yapıyor | Varsayılan |
|---|---|---|
| `max_depth` | En fazla kaç soru derinliği | `None` (sınırsız) |
| `min_samples_leaf` | Bir yaprakta en az kaç kayıt | 1 |
| `min_samples_split` | Bölünmek için en az kaç kayıt | 2 |
| `max_features` | Her bölünmede kaç özellik denenecek | Hepsi |
| `criterion` | `gini` / `entropy` (sınıflandırma), `squared_error` (regresyon) | `gini` |
| `ccp_alpha` | Budama gücü; büyüdükçe ağaç küçülüyor | 0.0 |
| `class_weight` | Dengesiz veride sınıflara ağırlık | `None` |

**`random_state` neden gerekiyor:** eşit derecede iyi iki bölünme varsa
ağaç aralarından rastgele seçiyor. Vermezsen her çalıştırmada farklı ağaç
çıkabiliyor.

## Ağacı okumak

**Metin olarak:**

```python
from sklearn.tree import export_text
print(export_text(model, feature_names=list(X.columns)))
```

**Çizim olarak:**

```python
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(11, 5))
plot_tree(model, feature_names=list(X.columns),
          class_names=["stays", "leaves"],
          filled=True, rounded=True, fontsize=9, ax=ax)
fig.savefig("chart.png")
```

Her kutuda dört satır var:

| Satır | Anlamı |
|---|---|
| `visits <= 18.5` | Bu düğümün sorusu (yapraklarda yok) |
| `gini = 0.425` | Safsızlık: 0 saf, 0.5 en karışık |
| `samples = 150` | Bu düğüme kaç kayıt düşmüş |
| `value = [104, 46]` | Sınıflara göre dağılım |
| `class = stays` | Çoğunluk sınıfı — yapraktaysa tahmin |

## Ağacın yapısına erişmek

```python
print(model.get_depth())              # gercek derinlik
print(model.get_n_leaves())           # yaprak sayisi
print(X.columns[model.tree_.feature[0]])          # kok bolunmenin ozelligi
print(round(model.tree_.threshold[0], 2))         # kok bolunmenin esigi
```

`tree_.feature` ve `tree_.threshold` dizileri düğüm sırasına göre; ilk
eleman her zaman kök.

## Özellik önemi

```python
for name, value in zip(X.columns, model.feature_importances_):
    print(name, round(float(value), 3))
```

Toplamları 1. O sütunla yapılan bölünmelerin safsızlığı ne kadar
düşürdüğünü anlatıyor.

**Üç tuzağı:**

| Tuzak | Sonucu |
|---|---|
| Önem sebep değil | "En önemli sütun" o sütunun sebep olduğunu göstermiyor |
| İlişkili sütunlar | Biri seçiliyor, ikizi sıfıra yakın önem alıyor |
| Çok değerli sütunlar | Sürekli sayısal sütunlar şişiyor; kimlik sütunu en tepeye çıkıyor |

Daha güvenilir bir yöntem `permutation_importance`: bir sütunu karıştırıp
skorun ne kadar düştüğüne bakıyor.

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10,
                                random_state=42)
```

## Karmaşıklığı sınırlamak

| Yol | Nasıl çalışıyor |
|---|---|
| `max_depth` | Kaba ama anlaşılır; kaç soru sorulacağını sınırlıyor |
| `min_samples_leaf` | Yapraktaki kayıt sayısına alt sınır; tek kaydı ezberlemeyi engelliyor |
| `min_samples_split` | Küçük düğümlerin bölünmesini engelliyor |
| `ccp_alpha` | Ağacı büyütüp sonra kesiyor; en esnek yol |

```python
DecisionTreeClassifier(max_depth=4, min_samples_leaf=5, random_state=42)
```

İkisini birlikte kullanmak yaygın: derinlik üst sınırı koyuyor,
`min_samples_leaf` derin dalların tek kayda inmesini engelliyor.

## Ölçekleme gerekmiyor

Ağaç `income <= 137500` diye soruyor. Ölçeklendikten sonra bu
`income_scaled <= 0.42` oluyor — **eşik değişiyor, sıralama değişmiyor.**

Ölçülen sonuç: ölçeklemesiz 0.80, ölçekli 0.80. Birebir aynı.

Aynı sebeple:

- Aykırı değerler ağacı bozmuyor (uç değer yalnızca "eşiğin üstünde").
- Sütunların birimleri karışık olabiliyor (yıl, lira, adet).
- Logaritma gibi dönüşümler bir şey değiştirmiyor.

**Kategorik sütunlar yine kodlanmalı:** sklearn'in ağacı metinle
çalışmıyor, `pd.get_dummies` gerekiyor.

## Regresyon ağacı

```python
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor(max_depth=3, random_state=42)
```

Aynı mantık, iki fark:

- Safsızlık yerine **varyans** düşürülüyor (`criterion="squared_error"`).
- Yaprakta sınıf yerine o gruptaki kayıtların **ortalaması** duruyor.

Bunun bir sonucu var: regresyon ağacı **basamaklı** tahmin üretiyor. Bir
yaprağa düşen bütün kayıtlar aynı sayıyı alıyor, yani sürekli bir eğri
çizemiyor.

Bölüm 05'te ölçülmüştü: araba verisinde ağacın MAE'si 64, doğrusal
regresyonunki 16.5. Sebebi tam olarak bu — ilişki doğrusalken basamaklarla
taklit etmek pahalıya geliyor.

## Sık yapılan hatalar

- **Derinliği sınırlamamak.** Varsayılan `None`; ağaç eğitim verisini
  ezberliyor.
- **Derinliği test tablosuna bakarak seçmek.** Çapraz doğrulama gerekiyor.
- **`random_state` vermemek.** Eşit bölünmelerde rastgelelik var.
- **Özellik önemini sebep sanmak.** En sık ve en pahalı yorum hatası.
- **Kimlik/numara sütununu veride bırakmak.** Ağaç onunla her kaydı
  ayırabiliyor.
- **Ölçekleme için zaman harcamak.** Zararı yok ama faydası da yok.
- **Tek bir ağaca güvenmek.** Birkaç satır değişince ağaç değişiyor;
  topluluk yöntemleri bunun için var.
