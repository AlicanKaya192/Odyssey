İlk kez model kuran herkes bu listeden birkaçını görüyor. Çoğu tek satırlık
hata, ama mesajları ilk bakışta bir şey anlatmıyor.

## 1. `Expected 2D array, got 1D array instead`

```python
X = df["area"]          # Series - tek boyutlu
model.fit(X, y)         # hata
```

**Çevirisi:** "X'i tablo olarak vermemişsin."

```python
X = df[["area"]]        # DataFrame - iki boyutlu
```

Tek sayı için tahmin isterken de aynısı geçerli:

```python
model.predict(95)       # hata
model.predict([[95]])   # dogru
```

## 2. `This ... instance is not fitted yet`

```python
model = LinearRegression()
print(model.coef_)      # hata - henuz ogrenmedi
```

Alt çizgiyle biten değerler `fit` çağrıldıktan **sonra** oluşuyor. Aynı şey
`predict` için de geçerli.

## 3. `train_test_split`'in dönüş sırasını karıştırmak

```python
X_train, y_train, X_test, y_test = train_test_split(X, y)   # yanlis
```

Doğru sıra `X_train, X_test, y_train, y_test`. Yanlış yazınca **hata
alınmıyor** — kod çalışıyor, model saçma sonuç veriyor. Bu yüzden en
tehlikeli hatalardan biri.

Kontrol etmenin kolay yolu: `len(X_train)`, `len(X_test)`'ten büyük olmalı.

## 4. `random_state` vermemek

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
```

Kod çalışıyor ama her çalıştırmada başka bir MAE çıkıyor. İki modeli
karşılaştırmak imkânsız hâle geliyor: fark modelden mi geldi, ayrımdan mı
belli olmuyor.

## 5. Taban çizgiyi modelden sonra kurmak

Modelin MAE'sini görüp sonra taban çizgi hesaplamak, teknik olarak yanlış
değil ama insan doğasına aykırı: sayıyı gördükten sonra beklentini ona göre
ayarlıyorsun.

Taban çizgi **önce** kuruluyor. Geçilecek çizgi belliyken model kurmak,
sonucu gördükten sonra çizgi çizmekten farklı bir iş.

## 6. Eğitim verisinde ölçmek

```python
model.fit(X_train, y_train)
print(model.score(X_train, y_train))    # anlamsiz
print(model.score(X_test, y_test))      # dogru
```

Eğitim skoru modelin ne kadar ezberlediğini söylüyor, ne kadar
öğrendiğini değil. Yine de tamamen değersiz değil: **iki skoru birlikte**
görmek aşırı öğrenmeyi ortaya çıkarıyor (eğitim 0.99, test 0.62).

## 7. Katsayıları birbiriyle kıyaslamak

```python
print(model.coef_)      # [ 2.77 -3.35]
```

"3.35 daha büyük, demek ki yaş daha önemli" **yanlış**. Katsayı sütunun
birimine bağlı: metrekare 45-165 arasında geziniyor, yaş 0-30 arasında.
Birimleri farklı iki sayı kıyaslanmıyor.

Kıyaslamak için önce ölçeklemek gerekiyor — 4. bölümün konusu.

## 8. Katsayıyı sebep sanmak

Model "yaş -3.35" diyorsa bu bir **birliktelik**. "Evi yaşlandırmak fiyatı
düşürür" cümlesi modelden çıkmıyor; modelden çıkan cümle "yaşı büyük olan
evlerin fiyatı düşük çıkıyor".

## 9. Sütun adlarını eğitim ve tahminde farklı vermek

```python
model.fit(df[["area", "age"]], y)
model.predict(df[["age", "area"]])      # sirasi farkli - yanlis sonuc
```

Sütun **sırası** modelin öğrendiği sırayla aynı olmalı. pandas ile
çalışırken sklearn uyarı verebiliyor ama her durumda değil; iki yerde de
aynı listeyi kullanmak en güvenlisi.

## 10. Tahmin için ölçüyü ters sırayla çağırmak

```python
mean_absolute_error(prediction, y_test)   # MAE'de fark yaratmiyor
r2_score(prediction, y_test)              # R2'de yanlis sonuc
```

Sıra her zaman `(gerçek, tahmin)`. MAE simetrik olduğu için affediyor,
R² affetmiyor — ve yanlış sonuç hata vermeden geçiyor.

## 11. Ölçüyü problem türüne uydurmamak

Regresyonda `accuracy_score`, sınıflandırmada `mean_absolute_error`
çağırmak. Bazen hata veriyor, bazen anlamsız bir sayı üretiyor.

Hedef sayıysa MAE/RMSE/R², kategoriyse accuracy/precision/recall.

## 12. Eksik değerli veriyi doğrudan modele vermek

```
ValueError: Input contains NaN
```

sklearn eksik değerle çalışmıyor (ağaç tabanlı birkaç model dışında).
Modelden önce doldurmak ya da o satırları atmak gerekiyor — ve bu karar
**ayırmadan sonra** verilmeli, yoksa sızıntı oluyor. 4. bölümün konusu.
