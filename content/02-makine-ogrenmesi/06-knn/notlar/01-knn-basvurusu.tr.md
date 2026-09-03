## Kurulum

```python
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

model = KNeighborsClassifier(n_neighbors=5)
model = KNeighborsRegressor(n_neighbors=5)
```

| Parametre | Ne yapıyor | Varsayılan |
|---|---|---|
| `n_neighbors` | Kaç komşuya bakılacağı (`k`) | 5 |
| `weights` | `uniform` eşit oy, `distance` yakına ağırlık | `uniform` |
| `metric` | Uzaklık ölçüsü (`minkowski`, `manhattan`) | `minkowski` |
| `p` | `minkowski` üssü: 2 Öklid, 1 Manhattan | 2 |
| `algorithm` | `auto`, `kd_tree`, `ball_tree`, `brute` | `auto` |

`algorithm` yalnızca **hızı** değiştiriyor, sonucu değil. Büyük veride
tahmin süresini düşürüyor.

## Zorunlu adım: ölçekleme

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

model.fit(X_train_scaled, y_train)
model.predict(X_test_scaled)
```

**Ölçeklemeden KNN kurulmuyor.** Ölçülen bir örnekte ölçeklemesiz doğruluk
0.64, ölçekli 0.92 çıktı — ve 0.64, taban çizginin (0.70) altında.

Sebebi: uzaklık hesabı büyük aralıklı sütunun tekelinde kalıyor. Geliri
0-200.000 arasında olan bir sütunun yanında 1-50 arasındaki ziyaret sayısı
görünmüyor.

`fit` eğitimde, `transform` ikisinde. `fit_transform`'u teste uygulamak
sızıntı.

## `k` seçimi

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for k in (1, 3, 5, 7, 9, 15, 25):
    scores = cross_val_score(KNeighborsClassifier(k), X_train_scaled,
                             y_train, cv=skf, scoring="accuracy")
    print(k, round(float(scores.mean()), 3), round(float(scores.std()), 3))
```

| `k` | Davranış |
|---|---|
| 1 | Eğitimde kusursuz (her nokta kendine en yakın), testte zayıf |
| Küçük (3-7) | Gürültüye duyarlı, sınır parçalı |
| Orta (9-25) | Genelde dengeli |
| Çok büyük | Sınırlar bulanık; `k = n` olduğunda taban çizgi |

**İki kural:**

- **Tek sayı seç.** İkili sınıflandırmada oylar eşit kalmıyor.
- **Ortalamaya tek başına bakma.** Farklar yayılımdan küçükse çapraz
  doğrulama k'ları ayırt edemiyor; o zaman **daha büyük k** tercih ediliyor,
  çünkü tek bir komşuya bağlı değil.

Ölçülen bir örnekte CV kazananı `k=1` idi (0.913) ama yayılım 0.040'tı ve
bütün k'lar o aralıktaydı. Testte `k=1` 0.820, `k=25` 0.920 verdi.

## Komşuları görmek

```python
distances, indices = model.kneighbors(X_test_scaled[:1])
print(indices)      # egitim verisindeki satir numaralari
print(distances)    # o satirlara uzakliklar
```

Bu, KNN'in yorumlanabilir tarafı: modelin **hangi kayıtlara bakarak** karar
verdiğini gösteriyor. Katsayı yok ama gerekçe var.

## Elle hesaplama

```python
def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

pairs = sorted((distance(point, new_point), label)
               for point, label in training)
nearest = [label for _, label in pairs[:k]]

# siniflandirma: oy coklugu
prediction = max(set(nearest), key=nearest.count)

# regresyon: ortalama
prediction = sum(values) / len(values)
```

## Sık yapılan hatalar

- **Ölçeklemeyi atlamak.** En pahalı hata; model taban çizginin altına
  düşebiliyor.
- **Test kümesinde `fit_transform` çağırmak.** Sızıntı.
- **`k`'yı test kümesine bakarak seçmek.** Test artık eğitim verisi.
- **Çift `k` seçmek.** İkili sınıflandırmada oylar eşitlenebiliyor.
- **Eksik değerle çalışmaya kalkmak.** Uzaklık hesaplanamıyor; önce
  doldurulması gerekiyor.
- **Çok özellikle kullanmak.** Boyut laneti: elli sütunda "en yakın"
  kelimesi anlamını kaybediyor.
- **`weights="distance"`'ı otomatik iyi sanmak.** Ölçülen bir örnekte
  0.92'den 0.88'e düşürdü.

## Maliyet

| İşlem | KNN | Doğrusal regresyon |
|---|---|---|
| `fit` | Anında (veriyi saklıyor) | Hesap yapıyor |
| `predict` | Her satıra uzaklık | Tek çarpma-toplama |
| Bellek | Bütün eğitim verisi | İki sayı |

Bu yüzden KNN'e **tembel** model deniyor: işi tahmin anına erteliyor.

Büyük veride tahmin süresi sorun oluyor; `algorithm="kd_tree"` yardımcı
oluyor ama özellik sayısı arttıkça o da etkisini kaybediyor.
