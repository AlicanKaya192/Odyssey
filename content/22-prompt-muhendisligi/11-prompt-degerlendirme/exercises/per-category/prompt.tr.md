`per_category(version)` salt okunur `shop_data.py`'deki
`RECORDED[version]` cevaplarını `TICKETS`'in etiketleriyle karşılaştırsın
ve her kategori için temizlenmiş cevabın (`strip`, `lower`, sondaki `.` ve
`!` atılmış) doğru olduğu mesaj sayısını bir sözlük olarak döndürsün
(anahtarlar `LABELS` sırasıyla).

**Beklenen çıktı:**

```
v1 [6, 7, 4, 8, 6]
v2 [8, 8, 6, 7, 7]
```
