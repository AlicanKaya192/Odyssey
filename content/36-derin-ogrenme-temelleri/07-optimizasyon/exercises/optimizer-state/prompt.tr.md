`state_names(kind)` optimizer'ı kurup `(w²)`'nin toplamıyla tek bir adım atsın
ve `optimizer.state[w]`'deki anahtarları sıralı liste olarak döndürsün.

**Beklenen çıktı:**

```
sgd []
momentum ['momentum_buffer']
adam ['exp_avg', 'exp_avg_sq', 'step']
```
