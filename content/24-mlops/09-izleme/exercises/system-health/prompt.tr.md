İstek kayıtları bir liste: her biri `{"ms": süre, "status": durum kodu}`. `system_health(requests)` fonksiyonunu yaz ve bir sözlük döndür:

- `"p95_ms"`: sürelerin p95'i, sıra yöntemiyle (sırala, `ceil(0.95 * n)`'inci eleman).
- `"error_rate"`: durum kodu 500 ya da üstü olanların payı.
- `"rejected_rate"`: durum kodu tam 422 olanların payı (şemaya uymayan istek).

Paylar üç basamağa yuvarlanmış.

**Beklenen çıktı:**

```
p95: 250
errors: 0.2
rejected: 0.1
```
