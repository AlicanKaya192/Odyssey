## Dengesizliği ölçmek

```python
print(y.value_counts())
print(y.mean())              # ikili hedefte pozitif oranı
```

Kaba bir ölçek:

| Pozitif oranı | Durum |
|---|---|
| %40 - %50 | Dengeli; doğruluk okunabilir |
| %10 - %40 | Hafif dengesiz; doğruluğa dikkat |
| %1 - %10 | Ciddi dengesiz; doğruluk yanıltıyor |
| %1'in altı | Uç; anomali tespiti düşünülmeli |

## Ayırmada `stratify`

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
```

Dengesiz veride **zorunlu**. Yoksa test kümesinde pozitif sayısı şansa
kalıyor; %1'lik bir sınıfta hiç pozitif olmayan bir test kümesi bile
çıkabiliyor.

Aynı sebeple çapraz doğrulamada `StratifiedKFold` kullanılıyor.

## Sınıf ağırlığı

```python
LogisticRegression(max_iter=1000, class_weight="balanced")
RandomForestClassifier(n_estimators=200, class_weight="balanced")
DecisionTreeClassifier(class_weight="balanced")
```

`"balanced"` her sınıfa `n_ornek / (n_sinif * o_sinifin_sayisi)` ağırlığını
veriyor. Elle de yazılabiliyor:

```python
class_weight={0: 1, 1: 10}
```

Ölçülen etki: recall 0.286 → 0.667, precision 0.75 → 0.269.

**`class_weight` bir takas ayarı.** Recall'ü yükseltiyor, precision'ı
düşürüyor. Hangisinin doğru olduğu problemin maliyetine bağlı.

## Eşik

```python
probability = model.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.1).astype(int)
```

`predict()` her zaman 0.5 kullanıyor. Dengesiz veride bu neredeyse hiç
doğru yer değil.

Eşik taraması eğitim ya da doğrulama tarafında yapılır; test kümesine
bakarak eşik seçmek bölüm 05'teki sızıntının aynısı.

## Ölçüler

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix,
                             classification_report,
                             roc_auc_score, average_precision_score)
```

| Ölçü | Neye bakıyor | Dengesiz veride |
|---|---|---|
| `accuracy_score` | Doğru bilinen oranı | **Yanıltıyor** |
| `precision_score` | Pozitif dediklerinin ne kadarı doğru | Yararlı |
| `recall_score` | Gerçek pozitiflerin ne kadarı yakalandı | Yararlı |
| `f1_score` | İkisinin harmonik ortalaması | Yararlı |
| `roc_auc_score` | Sıralama yeteneği | **İyimser** |
| `average_precision_score` | PR eğrisinin altındaki alan | En duyarlısı |

Taban çizgileri:

| Ölçü | Rastgele modelin değeri |
|---|---|
| Doğruluk | En sık sınıfın oranı (burada 0.944) |
| ROC AUC | 0.5 |
| Ortalama precision | Pozitif oranı (burada 0.056) |

## Karışıklık matrisi

```python
print(confusion_matrix(y_test, prediction))
# [[352   2]     TN=352  FP=2
#  [ 15   6]]    FN=15   TP=6
```

Satırlar gerçek, sütunlar tahmin. Sol üstten sağ alta köşegen doğru
bilinenler.

Dengesiz veride **her zaman** bakılır: tek bir doğruluk sayısının
gizlediği her şey burada duruyor.

## Çapraz doğrulamada ölçü seçmek

```python
cross_val_score(model, X_train, y_train, cv=skf, scoring="average_precision")
```

Sık kullanılan `scoring` değerleri: `"accuracy"`, `"precision"`,
`"recall"`, `"f1"`, `"roc_auc"`, `"average_precision"`,
`"balanced_accuracy"`.

Ölçülen yayılımlar: `accuracy` 0.008, `recall` 0.188, `roc_auc` 0.028,
`average_precision` 0.144. Yayılımı sıfıra yakın bir ölçü hiperparametre
seçemiyor.

## Yeniden örnekleme

sklearn'de yok; `imbalanced-learn` paketinde:

```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
```

Üç kural:

1. **Yalnızca eğitim kümesine** uygulanır.
2. Çapraz doğrulamada **her katın içinde** yapılır, öncesinde değil.
3. `class_weight` çoğu durumda aynı işi veriyi bozmadan yapıyor; önce o
   denenir.

## Sık yapılan hatalar

- **Doğruluğu rapor etmek.** %94,4 hiçbir şey yapmayan modelin skoru.
- **`stratify` unutmak.** Test kümesindeki pozitif sayısı şansa kalıyor.
- **Yalnızca ROC AUC yazmak.** Dengesiz veride iyimser; ortalama precision
  da verilmeli.
- **Eşiği test kümesine bakarak seçmek.** Sızıntı.
- **Yeniden örneklemeyi ayırmadan önce yapmak.** Aynı satırın kopyası hem
  eğitimde hem testte çıkıyor — bölüm 04'teki sızıntının en sinsi hâli.
- **`class_weight="balanced"` deyip işi bitmiş saymak.** Precision'ın ne
  kadar düştüğüne bakılmadan verilen karar eksik.
- **Ortalama precision'ı 0.5 tabanıyla karşılaştırmak.** Onun tabanı
  pozitif oranı, burada 0.056.
