`moving_average(values, window)` fonksiyonunu yaz: değerleri sırayla
`deque(maxlen=window)`'a eklesin ve **her eklemeden sonra** penceredeki
değerlerin ortalamasını `round(..., 2)` ile bir listeye koysun. Pencere
dolmadan önce de o ana kadarki değerlerin ortalaması alınır.

**Beklenen çıktı:**

```
[10.0, 15.0, 20.0, 30.0, 40.0]
[5.0, 5.0, 5.0]
```
