Pipeline'ın adımları yalnızca `X`'i dönüştürür. Ama bazen dönüştürülmesi
gereken **hedefin kendisidir**: fiyat, gelir, bekleme süresi gibi sağa
çarpık, katlanarak büyüyen hedefler. `TransformedTargetRegressor` hedefi
eğitimden önce dönüştürür ve tahmini geri çevirir.

```python
import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(7)
X = rng.uniform(0, 3, size=(300, 1))
y = np.exp(1.0 + 1.2 * X[:, 0] + rng.normal(0, 0.3, 300))
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7)
plain = LinearRegression().fit(X_train, y_train)
logged = TransformedTargetRegressor(regressor=LinearRegression(),
                                    func=np.log, inverse_func=np.exp)
logged.fit(X_train, y_train)
print(round(plain.score(X_test, y_test), 3), round(logged.score(X_test, y_test), 3))
at_zero = [round(float(m.predict([[0.0]])[0]), 2) for m in (plain, logged)]
print(*at_zero)
print(round(float(logged.regressor_.coef_[0]), 2))
```

```text
0.645 0.807
-11.92 2.66
1.19
```

## Ne oldu?

- Hedef üstel büyüyor. Düz doğrusal model test R²'si 0,645 aldı ve x = 0'da
  **eksi** fiyat tahmin etti (−11,92): hiç olmayacak bir değer.
- `TransformedTargetRegressor` modeli `log(y)` üzerinde eğitti, tahmini `exp`
  ile geri çevirdi: R² 0,807, x = 0'da 2,66 (gerçek değer e¹ ≈ 2,72).
- İçteki model `log(y)`'nin eğimini öğrendi: 1,19 (veriyi üretirken 1,2
  kullandık).
- Elle `np.log(y)` ile eğitip tahmini `np.exp` ile çevirmek de olur, ama
  unutması kolay; skorlar ve çapraz doğrulama da yanlış ölçekte hesaplanır.
  Bu sınıf ikisini de doğru yapar ve bir pipeline'ın sonuna konabilir.

## Ne zaman?

- Hedef hep pozitif ve sağa çarpıksa (fiyat, gelir, süre) `np.log` /
  `np.exp`; sıfır olabiliyorsa `np.log1p` / `np.expm1`.
- Dönüşümü veriden öğrenmek istiyorsan `transformer=QuantileTransformer()` ya
  da `PowerTransformer()` verilir.
