Model çoğu zaman tek başına çalışmaz: önce veri ölçeklenir, kodlanır,
eksikler doldurulur. Sunarken bu adımların **hepsi** eğitimdekiyle aynı
olmalı.

## Ölçekleyiciyi unutmak (ölçtük)

Eğitimde veriyi `StandardScaler` ile ölçekleyip bir k-NN modeli eğittik;
sunarken yalnızca modeli kullandık ve ham ölçüleri verdik:

```text
çiçek                 ham girdi   ölçekli girdi
5.1, 3.5, 1.4, 0.2    2           0
5.9, 3.0, 4.2, 1.5    2           1
6.7, 3.0, 5.2, 2.3    2           2
```

Ham girdiyle model 150 çiçeğin **hepsine** `2` (virginica) dedi: doğruluk
0,953'ten 0,333'e düştü. Hiçbir hata, hiçbir uyarı yok. API'de en tehlikeli
hata türü bu: her şey çalışıyor gibi görünüyor.

## Çözüm: bütün hattı kaydetmek

ML patikasındaki Pipeline bölümünü hatırla:

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

pipe = make_pipeline(StandardScaler(), KNeighborsClassifier())
pipe.fit(iris.data, iris.target)
joblib.dump(pipe, "model.joblib")
```

Sunarken `joblib.load("model.joblib").predict(row)` ham girdiyi alıp önce
ölçekliyor, sonra tahmin ediyor (ölçtük: `6.7, 3.0, 5.2, 2.3` → `2`).
API'nin ölçeklemeyi bilmesi gerekmiyor; hat içinde.

## Kural

**Eğitimde `fit` edilen her şey aynı dosyada kaydedilir.** Ölçekleyiciyi
ayrı, modeli ayrı kaydetmek; ya da ölçeklemeyi API'de elle yeniden yazmak
bir gün mutlaka ayrışır.

## Sürüm uyumu

`joblib` ile kaydedilen model, kaydeden scikit-learn sürümüyle yüklenmeli.
Farklı sürümde uyarı ya da hata çıkabilir. Bu yüzden `requirements.txt`'te
sürüm sabitlenir (`scikit-learn==...`); Docker imajı da aynı sürümle kurulur.
