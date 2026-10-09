`best_alpha(X, y, alphas, k)` fonksiyonunu yaz: her `α` için `k` katlı
çapraz doğrulama MSE'sini hesapla (katlar `np.array_split(np.arange(n), k)`,
karıştırma yok) ve hatası en küçük `α`'yı döndürsün. `ridge` hazır.

**Beklenen çıktı:**

```
0.01
```
