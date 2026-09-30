`stores.csv` dört mağazanın 2024 günlük satışı, uzun biçimde: `date`,
`store`, `sales`. Onu geniş biçime çevir ve eksikleri gör.

**Yapman gerekenler:**

1. Dosyayı `parse_dates=["date"]` ile oku.
2. Her mağazanın satır sayısını sözlük olarak yazdır:
   `long.groupby("store").size().to_dict()`.
3. Geniş biçime çevir:
   `long.pivot(index="date", columns="store", values="sales")`. Şeklini
   (`shape`) yazdır.
4. Her sütundaki `NaN` sayısını sözlük olarak yazdır.
5. D mağazasının ilk geçerli tarihini `"%Y-%m-%d"` biçiminde yazdır
   (`first_valid_index()`).

**Beklenen çıktı:**

```
{'A': 366, 'B': 366, 'C': 314, 'D': 245}
(366, 4)
{'A': 0, 'B': 0, 'C': 52, 'D': 121}
2024-05-01
```

Uzun tabloda 1291 satır vardı; geniş tabloda 1464 hücre var. Aradaki 173
hücre, uzun tabloda hiç satırı olmayan günler: C'nin pazarları ve D'nin
açılmadan önceki dört ayı.
