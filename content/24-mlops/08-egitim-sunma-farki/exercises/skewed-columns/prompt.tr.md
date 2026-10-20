Eğitimdeki ve sunma anındaki sütun ortalamaları aynı sırayla veriliyor. `skewed_columns(names, trained, live, tolerance)` fonksiyonunu yaz ve farkı büyük olan sütunların adlarını sırayla döndür:

- Fark büyük: `abs(live - trained) > tolerance * abs(trained)`.
- Eğitimdeki ortalama `0` ise oran kurulamaz: canlıdaki de `0` değilse işaretle.

**Beklenen çıktı:**

```
['monthly_fee', 'support_calls', 'is_pro']
[]
```
