`trainable_count(n_in, n_hidden, n_out)` modeli kurup `[eğitilecek parametre
sayısı, toplam parametre sayısı]` döndürüyor. İlk katmanı (`model[0]`) dondur ve
eğitilecek sayıyı yalnızca `requires_grad` olanlardan hesapla.

**Beklenen çıktı:**

```
[51, 163]
[12, 67]
```
