Bu alanın kelimeleri, tanıdık şeylerin yeni adları. Karşılıkları burada.

## Veri

| Terim | Ne demek |
|---|---|
| Örnek (sample, instance) | Tablodaki bir **satır**: bir ev, bir hasta |
| Özellik (feature, değişken) | Tahminde kullanılan bir **sütun** |
| Hedef (target, label, etiket) | Tahmin edilmek istenen sütun |
| Bağımsız değişken | Özelliğin başka adı — `X` |
| Bağımlı değişken | Hedefin başka adı — `y` |
| Boyut (dimension) | Özellik sayısı |

`X` büyük, `y` küçük yazılıyor: `X` bir tablo, `y` tek sütun.

## Öğrenme türleri

| Tür | Elinde ne var | Örnek |
|---|---|---|
| Gözetimli | Özellikler **ve** doğru cevaplar | Fiyat tahmini, spam tespiti |
| Gözetimsiz | Yalnızca özellikler | Müşteri kümeleme, boyut indirgeme |
| Pekiştirmeli | Ödül ve ceza | Oyun oynayan sistemler |

## Problem türleri

| Hedef | Problem | Ölçü |
|---|---|---|
| Sayı | Regresyon | MAE, RMSE, R² |
| İki kategori | İkili sınıflandırma | Accuracy, precision, recall, AUC |
| Çok kategori | Çoklu sınıflandırma | Accuracy, makro F1 |
| Etiket yok | Kümeleme | Silhouette, elbow |

## Süreç

| Terim | Ne demek |
|---|---|
| Eğitim kümesi (train set) | Modelin öğrendiği veri |
| Test kümesi (test set) | Modelin **hiç görmediği**, ölçüm için ayrılan veri |
| Doğrulama kümesi (validation) | Ayar denemek için ayrılan üçüncü parça |
| Eğitmek (fit) | Kuralı veriden çıkarmak |
| Tahmin (predict) | Kuralı yeni satıra uygulamak |
| Taban çizgi (baseline) | Öğrenmeyen en basit tahmin; kıyas noktası |

## Model davranışı

| Terim | Ne demek |
|---|---|
| Aşırı öğrenme (overfitting) | Eğitimde çok iyi, testte kötü — ezberlemiş |
| Yetersiz öğrenme (underfitting) | İkisinde de kötü — kural çok basit kalmış |
| Genelleme | Görmediği veride de çalışabilmesi |
| Yanlılık (bias) | Modelin sistematik olarak yanılması |
| Varyans (variance) | Veri biraz değişince sonucun çok değişmesi |

## Parametre ve hiperparametre

| Terim | Kim belirliyor |
|---|---|
| Parametre | **Model**, eğitim sırasında (doğrusal regresyonun eğimi) |
| Hiperparametre | **Sen**, eğitimden önce (KNN'in `k` değeri, ağacın derinliği) |

Ayrım pratik: parametreyi elle değiştirmiyorsun, hiperparametreyi
deneyerek seçiyorsun.

## sklearn'de her modelin aynı üç adımı

```python
model = BirModel()          # kur
model.fit(X_train, y_train) # ogren
tahmin = model.predict(X_test)
```

Doğrusal regresyon, karar ağacı, KNN — hepsi aynı üç çağrıyı taşıyor.
Model değiştirmek genelde tek satır değiştirmek demek. Bu tasarım, farklı
yöntemleri denemeyi ucuz hâle getiriyor.

## Sık görülen kısaltmalar

| Kısaltma | Açılımı |
|---|---|
| MAE | Mean Absolute Error — ortalama mutlak hata |
| MSE / RMSE | Mean Squared Error / karekökü |
| R² | Açıklanan varyans oranı |
| TP / TN / FP / FN | Doğru pozitif / doğru negatif / yanlış pozitif / yanlış negatif |
| ROC-AUC | Eğri altında kalan alan |
| CV | Cross validation — çapraz doğrulama |
| KNN | K-Nearest Neighbors |
| CART | Classification and Regression Tree |
| RF | Random Forest |
| GBM | Gradient Boosting Machine |
