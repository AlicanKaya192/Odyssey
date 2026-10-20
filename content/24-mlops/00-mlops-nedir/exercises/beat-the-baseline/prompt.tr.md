Bir modelin doğruluğu tek başına bir şey söylemez; onu en basit tahminle karşılaştırmak gerekir. Bu veride en basit tahmin "herkes kalır" (`churned` = `0`).

Eğitim verisi (`X`, `y`) ve test verisi (`X_test`, `y_test`) hazır. Şunları yap:

- `LogisticRegression(max_iter=1000)` ile bir model eğit.
- Modelin test doğruluğunu `model.score(X_test, y_test)` ile ölç.
- "Herkes kalır" tahmininin doğruluğunu hesapla: test verisinde kalanların oranı, yani `1 - sum(y_test) / len(y_test)`.
- İkisini üç basamağa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
model accuracy: 0.813
always stay: 0.703
```
