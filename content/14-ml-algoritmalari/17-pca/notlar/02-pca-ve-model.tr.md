PCA çoğu zaman tek başına değil, bir modelden önce kullanılır: 64 özellik
yerine 20 bileşenle eğitmek daha hızlıdır. Peki ne kadar doğruluk kaybediliyor?
Dersteki rakam verisinde lojistik regresyonu farklı `k`'larla, 5 katlı çapraz
doğrulamayla ölçelim. Ölçekleme ve PCA `Pipeline` içinde: her katta yalnızca
eğitim parçasına uyuyorlar, test parçası sızmıyor.

```python
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

digits = load_digits()
for k in (5, 10, 20, 40, 64):
    model = make_pipeline(StandardScaler(), PCA(k),
                          LogisticRegression(max_iter=2000))
    score = cross_val_score(model, digits.data, digits.target, cv=5).mean()
    print(k, round(score, 3))
```

```text
5 0.771
10 0.84
20 0.899
40 0.914
64 0.92
```

64 bileşenin hepsiyle (yani yalnızca bir döndürme) doğruluk 0,92. 20 bileşenle
0,899, 40 ile 0,914: özelliklerin üçte birinden azıyla doğruluğun çoğu
korunuyor. 5 bileşende 0,771'e düşüyor; burada fazla bilgi atılmış.

Bu tablo PCA'nın bir **ödünleşim** (trade-off) olduğunu gösteriyor: daha az
özellik, daha hızlı model ve daha az aşırı uyum riski karşılığında biraz
doğruluk. `k`'yı da diğer ayarlar gibi çapraz doğrulamayla seçmek en
güvenlisi. Bir uyarı: PCA hedefi görmez; en çok varyans taşıyan yönler her
zaman sınıfları en iyi ayıran yönler değildir.
