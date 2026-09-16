İç içe listeyi düzleştirip toplayacaksın.

Elindeki veri:

```python
rows = [[3, -1, 4], [0, 5], [-2, 8, 1]]
```

**Yapman gerekenler:**

1. `flat` — bütün sayılar tek bir listede (iç içe kavrama ile).
2. `positives` — yalnızca **sıfırdan büyük** olanlar, yine tek listede.
3. `total` — bütün sayıların toplamı. Burada liste kurma: `sum()` içine
   **üreteç ifadesi** yaz (köşeli parantez yok).

Sonra üçünü sırayla yazdır.

**Beklenen çıktı:**

```
[3, -1, 4, 0, 5, -2, 8, 1]
[3, 4, 5, 8, 1]
18
```

> İki `for` yan yana yazılıyor: önce dış liste, sonra iç liste.
