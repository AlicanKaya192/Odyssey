Dört sayıdan başlayıp bütün ölçüler türüyor. Karışıklık matrisini bilmek,
geri kalanını ezberlemekten kurtarıyor.

## Karışıklık matrisi

```python
from sklearn.metrics import confusion_matrix
tn, fp, fn, tp = confusion_matrix(y_test, prediction).ravel()
```

| Kısaltma | Gerçek | Tahmin | Türkçesi |
|---|---|---|---|
| TN | 0 | 0 | Doğru negatif |
| FP | 0 | 1 | Yanlış pozitif — **yanlış alarm** |
| FN | 1 | 0 | Yanlış negatif — **kaçırma** |
| TP | 1 | 1 | Doğru pozitif |

sklearn matrisi `[[TN, FP], [FN, TP]]` sırasıyla döndürüyor: **satırlar
gerçek, sütunlar tahmin.** Sol üst köşe her zaman TN.

`ravel()` matrisi düz listeye çeviriyor, böylece dört değişkene tek satırda
dağıtılabiliyor.

## Ölçüler ve formülleri

| Ölçü | Formül | Cevapladığı soru |
|---|---|---|
| Accuracy | `(TP + TN) / toplam` | Kaçını doğru bildim? |
| Precision | `TP / (TP + FP)` | "1" dediklerimin kaçı gerçekten 1? |
| Recall | `TP / (TP + FN)` | Gerçek 1'lerin kaçını buldum? |
| Specificity | `TN / (TN + FP)` | Gerçek 0'ların kaçını buldum? |
| F1 | `2PR / (P + R)` | Precision ve recall'ın dengesi |

**Paydaya bakarak ayırt etmek:**

- Precision'ın paydası **senin tahminlerin**.
- Recall'ın paydası **gerçekte var olanlar**.

## Kod karşılıkları

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

accuracy_score(y_test, prediction)
precision_score(y_test, prediction)
recall_score(y_test, prediction)
f1_score(y_test, prediction)
print(classification_report(y_test, prediction))
```

`classification_report` hepsini **her sınıf için ayrı** veriyor; tek sayıya
bakmaktan çok daha bilgilendirici.

**`zero_division`:** hiç pozitif tahmin yapılmadıysa precision'ın paydası
sıfır oluyor. sklearn uyarı verip 0 döndürüyor; `zero_division=0` yazarak
uyarıyı susturabiliyorsun.

## Hangisi ne zaman

| Durum | Bakılacak ölçü |
|---|---|
| Sınıflar dengeli, hatalar eşit maliyetli | Accuracy |
| Kaçırmak pahalı (hastalık, dolandırıcılık) | **Recall** |
| Yanlış alarm pahalı (spam, öneri) | **Precision** |
| İkisi de önemli, tek sayı gerekiyor | F1 |
| Sınıflar çok dengesiz | Precision + recall + karışıklık matrisi |
| Eşikten bağımsız değerlendirme | ROC-AUC |

**Accuracy tek başına yalnızca sınıflar dengeliyken güvenilir.** Değilse
taban çizgi zaten yüksek çıkıyor ve sayı bir şey anlatmıyor.

## Taban çizgi

```python
most_common = y_train.mode()[0]
baseline = accuracy_score(y_test, [most_common] * len(y_test))
```

sklearn'in hazırı:

```python
from sklearn.dummy import DummyClassifier

dummy = DummyClassifier(strategy="most_frequent")
dummy.fit(X_train, y_train)
print(accuracy_score(y_test, dummy.predict(X_test)))
```

`strategy` seçenekleri: `most_frequent`, `stratified` (sınıf oranlarına
göre rastgele), `uniform` (eşit rastgele), `constant` (belirlediğin sınıf).

## Eşik

```python
probability = model.predict_proba(X_test)[:, 1]
prediction = (probability >= 0.4).astype(int)
```

`predict_proba` her sınıf için bir sütun döndürüyor; `[:, 1]` pozitif
sınıfın olasılığı.

| Eşik | Etkisi |
|---|---|
| Düşür | Recall ↑, precision ↓, daha çok yanlış alarm |
| Yükselt | Precision ↑, recall ↓, daha çok kaçırma |

**0.5 bir hesap sonucu değil, varsayılan.** Modeli yeniden eğitmeden
değiştirilebiliyor ve çoğu gerçek problemde değiştirilmesi gerekiyor.

Eşik seçimi de bir hiperparametre seçimi: **doğrulama** kümesinde yapılıyor,
test kümesinde değil.

## Çok sınıflı problemler

İkiden fazla sınıf varsa precision ve recall her sınıf için ayrı
hesaplanıyor, sonra ortalanıyor:

| Ortalama | Nasıl |
|---|---|
| `macro` | Sınıfların ortalaması; her sınıf eşit ağırlıkta |
| `weighted` | Kayıt sayısına göre ağırlıklı |
| `micro` | Bütün TP/FP/FN'ler toplanıp tek hesap |

```python
f1_score(y_test, prediction, average="macro")
```

Dengesiz veride `macro` ile `weighted` çok farklı çıkıyor: `weighted` büyük
sınıfın başarısını, `macro` küçük sınıftaki başarısızlığı öne çıkarıyor.

## Sık yapılan hatalar

- **`predict_proba` yerine `predict` kullanıp eşik oynatmaya çalışmak.**
  `predict` zaten 0/1 döndürüyor; eşik için olasılık gerekiyor.
- **`predict_proba`'nın sütununu karıştırmak.** `[:, 0]` negatif, `[:, 1]`
  pozitif sınıfın olasılığı.
- **Regresyon ölçüsü kullanmak.** Hedef kategoriyse MAE anlamsız.
- **Taban çizgiyi atlamak.** Dengesiz veride %90 doğruluk bir başarı
  olmayabilir.
- **Argümanları ters yazmak.** Sıra yine `(gerçek, tahmin)`; ters yazınca
  precision ile recall yer değiştiriyor ve hata alınmıyor.
