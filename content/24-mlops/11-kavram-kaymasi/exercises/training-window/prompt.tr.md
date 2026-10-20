Son pencereyi seçen `training_window(rows, current_month, size)` fonksiyonunu yaz:

- `rows`: her biri `"month"` anahtarı taşıyan sözlükler.
- Ayı `current_month`'tan büyük olmayan ve son `size` ayın içinde kalan satırları döndür: `current_month - size < month <= current_month`.
- Satırların sırası korunsun. `size` `0` ise liste boştur.

**Beklenen çıktı:**

```
3
[2, 3]
[]
```
