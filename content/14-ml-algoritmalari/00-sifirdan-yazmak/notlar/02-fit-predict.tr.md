Bu modüldeki her model aynı iskeletle yazılıyor:

```python
class Model:
    def __init__(self, setting=1.0):
        self.setting = setting         # ayarlar: kullanıcı verir, fit değiştirmez

    def fit(self, X, y):
        self.learned_ = ...            # öğrenilenler: sonu _ ile biter
        return self

    def predict(self, X):
        return ...                     # learned_ ile tahmin
```

## Sözleşmenin üç kuralı

1. **Ayar ile öğrenilen ayrı.** `__init__` yalnızca ayarları saklar
   (öğrenme oranı, ağaç derinliği). Veriden çıkan her şey `fit`'te hesaplanır
   ve `_` ile biter. Böylece "bu sayı benim seçimim mi, verinin mi?" sorusu
   adından okunur.
2. **`fit` yalnızca eğitim verisini görür.** Ölçekleyicinin ortalamasını test
   verisi dahil hesaplamak, testten eğitime bilgi sızdırır (**veri
   sızıntısı**, data leakage); model gerçekte olduğundan iyi görünür.
   Doğrusu: `fit(X_train)`, sonra `transform(X_train)` ve `transform(X_test)`.
3. **`fit` `self` döndürür.** `Model().fit(X, y).predict(X_new)` zinciri
   böyle çalışır.

## scikit-learn ile karşılaştırma

Her bölümde aynı düzen: aynı veride bizim modelimiz ve scikit-learn'ünki
eğitilir, sonra

- sayısal sonuçlar için `np.allclose(ours, theirs)`,
- etiketler için `(ours == theirs).mean()` (kaçta kaçı aynı),
- başarı için aynı ölçü (doğruluk, hata kareleri ortalaması)

karşılaştırılır. Fark çıkarsa çoğu zaman bir ayrıntı: `ddof`, düzenlileştirme
gücünün nasıl ölçeklendiği, eşitlikte hangi sınıfın seçildiği, rastgele
başlangıç. Farkı açıklayabilmek, modeli anladığının işaretidir.
