# Özellik Seçimi

Bir tablodaki sütunların hepsi faydalı değildir: bazıları hiç değişmez,
bazıları hedefle ilgisiz gürültüdür. Gereksiz sütun modeli yavaşlatır,
yorumlamayı zorlaştırır ve küçük veride aşırı öğrenmeye zemin hazırlar.
`sklearn.feature_selection` sütunları üç yoldan eler: tek tek istatistikle
(**filtre**), bir modelin önem puanlarıyla (**gömülü**) ve modeli tekrar
tekrar eğiterek (**sarmalayıcı**). Hepsi dönüştürücüdür; bu yüzden
önceki bölümdeki kural geçerli: seçim **pipeline'ın içinde**.

## Hiç değişmeyen sütunlar: VarianceThreshold

```python
import numpy as np
from sklearn.feature_selection import VarianceThreshold

X = np.array([[0, 1.0, 5.0], [0, 2.0, 5.0], [0, 3.0, 5.1], [0, 4.0, 5.0]])
vt = VarianceThreshold(threshold=0.01).fit(X)
print(vt.variances_.round(4).tolist(), vt.get_support().tolist())
```

```text
[0.0, 1.25, 0.0019] [False, True, False]
```

- Varyansı eşiğin altında kalan sütun atılır: ilk sütun hep 0, üçüncüsü
  neredeyse sabit (0,0019). Hedefe bakmaz; sızıntı riski yoktur.
- Eşik ölçeğe bağlıdır: ölçeklenmemiş veride küçük birimli sütun haksız yere
  atılabilir. Genellikle yalnızca sabit sütunları atmak için (`threshold=0`).

## Bu bölümün verisi

Sonraki bloklar aynı yapay veriyi kullanıyor: 20 sütun, ama yalnızca **ilk
4'ü** hedefle ilgili (`n_informative=4`, `shuffle=False`), geri kalan 16
gürültü. Hangi yöntemin bunu bulduğunu göreceğiz.

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
kb = SelectKBest(f_classif, k=4).fit(X, y)
print(sorted(kb.get_support(indices=True).tolist()))
mi = SelectKBest(mutual_info_classif, k=4).fit(X, y)
print(sorted(mi.get_support(indices=True).tolist()))
print(kb.scores_[:6].round(1).tolist())
```

```text
[0, 1, 2, 3]
[0, 1, 2, 3]
[282.0, 99.1, 383.7, 77.5, 0.3, 0.0]
```

- **Filtre** yöntemi: her sütunu hedefle **tek başına** puanlar, en iyi `k`
  tanesini tutar. `f_classif` ortalama farklarına (ANOVA F), `mutual_info`
  doğrusal olmayan ilişkilere de bakar. İkisi de 0–3'ü buldu.
- Puanlar (`scores_`) büyük farkla ayrışıyor: bilgili sütunlar 77–384,
  gürültü sıfıra yakın.
- Zayıf yanı: sütunları **tek tek** değerlendirir. Yalnızca birlikte anlamlı
  olan iki sütunu ya da birbirinin kopyası iki sütunu ayırt edemez.

## Modelin önemine göre: SelectFromModel

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
l1 = LogisticRegression(penalty="l1", C=0.05, solver="liblinear")
sfm = SelectFromModel(l1).fit(X, y)
print(sfm.get_support(indices=True).tolist())
forest = RandomForestClassifier(n_estimators=100, random_state=8)
sft = SelectFromModel(forest, max_features=4, threshold=-float("inf")).fit(X, y)
print(sorted(sft.get_support(indices=True).tolist()))
```

```text
[0, 1, 2, 3]
[0, 1, 2, 3]
```

- **Gömülü** yöntem: bir model eğitilir, katsayı ya da önem puanı düşük
  sütunlar atılır.
- L1 cezalı lojistik regresyon (doğrusal modeller bölümünde) gereksiz
  sütunların katsayısını **tam sıfıra** indirir; sıfır olmayanlar seçilir.
  `C` küçüldükçe daha az sütun kalır.
- Ormanın önem puanlarıyla en iyi 4 sütun (`max_features=4`,
  `threshold=-inf` "eşik yok, yalnızca sayı" demek). İkisi de 0–3.

## Model eğiterek eleme: RFECV

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
rfe = RFECV(LogisticRegression(), step=1, cv=5).fit(X, y)
print(rfe.n_features_, rfe.get_support(indices=True).tolist())
print(rfe.ranking_[:8].tolist())
```

```text
3 [0, 1, 2]
[1, 1, 1, 2, 14, 13, 12, 16]
```

- **Sarmalayıcı** yöntem: model eğitilir, en zayıf sütun atılır, tekrar
  eğitilir... (`RFE`, recursive feature elimination). `RFECV` kaç sütunda
  duracağını çapraz doğrulamayla seçer.
- Burada 3 sütun seçti: 3. sütun bilgili ama zayıf (filtre puanı 77,5);
  çapraz doğrulamaya göre onu tutmak skoru artırmıyordu. `ranking_` atılma
  sırasıdır: 1 seçilenler, büyük sayı erken atılanlar.
- En pahalı yöntemdir: 20 sütun × 5 kat ≈ yüz kez eğitim. Çok sütunlu veride
  önce bir filtreyle azaltmak iyi olur.

## Kaç sütun?

```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

X, y = make_classification(n_samples=500, n_features=20, n_informative=4,
                           n_redundant=0, shuffle=False, random_state=8)
for k in [2, 4, 10, 20]:
    pipe = make_pipeline(SelectKBest(f_classif, k=k), LogisticRegression())
    print(k, round(cross_val_score(pipe, X, y, cv=5).mean(), 3))
```

```text
2 0.868
4 0.87
10 0.868
20 0.852
```

- Seçim pipeline'ın içinde, `k` çapraz doğrulamayla karşılaştırılıyor.
- 4 sütun 20 sütundan biraz iyi (0,870'e karşı 0,852): 16 gürültü sütunu
  modeli az da olsa yanıltıyordu. Fark küçük; 500 satır gürültüye dayanmaya
  yetiyor. Satır azaldıkça ve sütun arttıkça fark büyür.
- `k` bir hiperparametredir; elle denemek yerine bir sonraki bölümde
  `GridSearchCV` ile aranacak (`selectkbest__k`).

## Özet

- Sabit sütunlar `VarianceThreshold`; hedefe bakmaz.
- Filtre `SelectKBest(f_classif / mutual_info_classif, k=)`: hızlı, sütunları
  tek tek değerlendirir.
- Gömülü `SelectFromModel(L1 ya da orman)`; sarmalayıcı `RFECV`: pahalı ama
  sütunları birlikte değerlendirir.
- Seçim her zaman pipeline'ın içinde; kaç sütun tutulacağı çapraz
  doğrulamayla seçilir.
