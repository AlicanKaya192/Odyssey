`cv_accuracy(X, y, k)` fonksiyonunu yaz: karıştırmadan `k` ardışık kata
böl (ilk `n % k` kat birer fazla); her katta en yakın merkez modelini
**yalnızca eğitim** kısmıyla eğit, test kısmında doğruluğu ölç. Doğrulukların
ortalamasını `round(..., 3)` ile döndürsün. `centroid_fit` ve
`centroid_predict` hazır.

**Beklenen çıktı:**

```
0.917
```
