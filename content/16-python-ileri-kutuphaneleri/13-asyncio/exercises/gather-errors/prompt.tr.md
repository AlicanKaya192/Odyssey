`safe_all(values)` her değer için `check(value)`'ı `gather` ile birlikte
çalıştırsın ve sonuçları **verilen sırayla** döndürsün. Hata veren değerin
yerine `"error"` yazılsın. `return_exceptions=True` kullan ve sonra
`isinstance(sonuç, Exception)` olanları değiştir.

**Beklenen çıktı:**

```
[10, 'error', 30]
```
