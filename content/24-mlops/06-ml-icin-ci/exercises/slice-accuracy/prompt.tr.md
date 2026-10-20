Satırlar (her birinde `"churned"` ve dilimin sütunu var) ve modelin tahminleri aynı sırayla veriliyor. `slice_accuracy(rows, predictions, column)` fonksiyonunu yaz:

- Satırları `column` sütununun değerine göre grupla.
- Her grupta tahminin `"churned"` ile aynı olduğu satırların payını üç basamağa yuvarla.
- `[[değer, doğruluk], ...]` döndür, değerler **sıralı**.

**Beklenen çıktı:**

```
basic 0.667
pro 0.667
```
