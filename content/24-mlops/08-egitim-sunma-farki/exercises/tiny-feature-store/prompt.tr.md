Dersteki `FeatureStore` sınıfını yaz ve iki boşluğu kapat:

- `write(customer, day, values)`: müşterinin geçmişine `[day, values]` ekler (tarihler artan sırayla yazılıyor).
- `offline(customer, day)`: o tarihte ya da öncesinde yazılmış son değerler; yoksa ya da müşteri hiç yoksa `None`.
- `online(customer)`: müşterinin en son yazılan değerleri; müşteri hiç yoksa `None`.

**Beklenen çıktı:**

```
training C7: {'support_calls': 1}
training C9: None
serving C7: {'support_calls': 4}
serving C5: None
```
