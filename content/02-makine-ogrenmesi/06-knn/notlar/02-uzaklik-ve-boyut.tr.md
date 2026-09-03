KNN'in tamamı tek bir işlemin üstünde duruyor: **iki kayıt birbirine ne
kadar benziyor?** Bu notun konusu o işlemin nasıl hesaplandığı ve nerede
bozulduğu.

## Öklid uzaklığı

İki nokta arasındaki düz çizgi mesafesi:

```
d = ((x1 - x2)^2 + (y1 - y2)^2 + ...) ^ 0.5
```

```python
def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5
```

Kare almanın iki işi var: işareti yok ediyor ve büyük farkları öne
çıkarıyor. İkincisi ölçekleme sorununun kaynağı — bir sütundaki 100.000'lik
fark, ötekindeki 40'lık farkın yanında **kare alındığında** iyice eziyor.

## Öteki uzaklıklar

| Ölçü | Nasıl | Ne zaman |
|---|---|---|
| Öklid (`p=2`) | Düz çizgi | Varsayılan; sürekli sayısal sütunlar |
| Manhattan (`p=1`) | Eksenler boyunca | Aykırı değere daha dayanıklı, çok boyutta daha kararlı |
| Kosinüs | Aradaki açı | Metin/vektör verisi; büyüklük değil **yön** önemliyse |
| Hamming | Kaç konumda farklı | İkili ya da kategorik sütunlar |

```python
KNeighborsClassifier(n_neighbors=5, metric="manhattan")
```

**Kosinüs neden metinde:** iki belge aynı konudan bahsediyorsa kelime
oranları benziyor ama uzunlukları çok farklı olabiliyor. Öklid uzun belgeyi
uzak sayıyor; kosinüs yalnızca yöne baktığı için ikisini yakın buluyor.

## Ölçekleme neden zorunlu

Bir örnek, sayılarla. İki müşteri:

```
A: income 50.000, visits 10
B: income 51.000, visits 45
```

Öklid uzaklığı:

```
((51000 - 50000)^2 + (45 - 10)^2) ^ 0.5
= (1.000.000 + 1.225) ^ 0.5
= 1000.6
```

**Ziyaret sayısındaki 35'lik fark toplama 1.225 katıyor; gelirdeki 1.000'lik
fark 1.000.000 katıyor.** Sonuç neredeyse tamamen gelirden geliyor —
oysa ayrılma davranışında ziyaret sayısı çok daha belirleyici olabilir.

Ölçekledikten sonra iki sütun da ortalama 0, standart sapma 1 oluyor ve
farklar karşılaştırılabilir hâle geliyor.

Ölçülen sonuç: doğruluk **0.64 → 0.92**.

## Boyut laneti

Özellik sayısı arttıkça uzaklık anlamını kaybediyor. Bunu görmek için basit
bir deney:

```python
import numpy as np

rng = np.random.default_rng(0)
for d in (2, 10, 100, 1000):
    points = rng.random((500, d))
    first = points[0]
    distances = np.sqrt(((points[1:] - first) ** 2).sum(axis=1))
    oran = distances.min() / distances.max()
    print(d, round(float(oran), 3))
```

Boyut arttıkça **en yakın komşuyla en uzak komşu arasındaki oran 1'e
yaklaşıyor.** Yani her nokta her noktaya neredeyse eşit uzaklıkta oluyor ve
"en yakın" seçimi rastgeleye dönüşüyor.

### Neden oluyor

Her yeni özellik uzaklığa bir terim daha ekliyor. Terim sayısı arttıkça
toplamlar birbirine benziyor — tıpkı çok sayıda zar atıldığında toplamların
ortalamaya yığılması gibi.

### Ne yapılır

| Yol | Nasıl |
|---|---|
| Özellik seçimi | Hedefle ilgisi zayıf sütunları çıkar (eğitim tarafında!) |
| Boyut indirgeme | PCA ile birkaç bileşene indir (10. bölüm) |
| Alan bilgisi | Sütunları birleştirip anlamlı az sayıda özellik üret |
| Model değiştirme | Ağaçlar bu sorundan etkilenmiyor |

**Kaba bir ölçü:** on beşten fazla özellikte KNN'i taban çizgiyle
karşılaştırmadan kullanma. Otuz sütunda genelde daha basit modeller daha
iyi.

## Karar sınırının şekli

`k`, sınırın **düzgünlüğünü** belirliyor:

| `k` | Sınır | Risk |
|---|---|---|
| 1 | Parçalı, adacıklı | Gürültüyü ezberliyor |
| 5-15 | Dalgalı ama bütün | Genelde iyi |
| Çok büyük | Neredeyse düz | Gerçek ayrıntıları kaçırıyor |

Ölçülen bir örnekte `k=1` ile `k=15` **aynı test doğruluğunu** (0.90)
verdi ama sınırları bambaşkaydı: biri tek tek noktaların etrafına adacıklar
oymuş, öteki tek bir düzgün eğri çizmişti.

**Aynı sayı, farklı model.** Bu, tek bir ölçüye bakmanın neden yetmediğini
gösteren en somut örnek.

## Kategorik sütunlar

KNN sayıyla çalıştığı için kategorik sütunlar önce kodlanıyor (bölüm 04).
Ama bir incelik var: **one-hot kodlanmış sütunlar uzaklığa 0 ya da 1 olarak
giriyor**, ölçeklenmiş sayısal sütunlar ise -3 ile +3 arasında.

Yani kategorik sütunlar sayısal olanlardan daha az ağırlık taşıyor. Bunu
dengelemek gerekirse kodlanmış sütunlar da ölçekleniyor ya da ağırlık
verilmiş bir uzaklık ölçüsü kullanılıyor.

Çok kategorili bir sütun (şehir gibi) one-hot ile onlarca sütun ürettiği
için ayrıca boyut lanetini besliyor.

## Eksik değerler

Uzaklık hesabında eksik değer tanımsız: `NaN` ile hiçbir sayı arasında
mesafe yok. sklearn hata veriyor.

İki yol var: bölüm 04'teki gibi doldurmak, ya da **`KNNImputer`** kullanmak
— eksik değeri en yakın komşuların değeriyle dolduran bir araç.

```python
from sklearn.impute import KNNImputer

imputer = KNNImputer(n_neighbors=5)
imputer.fit(X_train)
X_train = imputer.transform(X_train)
```

Kendisi de KNN olduğu için **o da ölçekleme istiyor** ve **o da ayırmadan
sonra** uygulanıyor.
