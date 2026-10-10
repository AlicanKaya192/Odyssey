`prep_frame(rows)` `size`'ı medyanla dolduran ve `city`'yi one-hot kodlayan bir
`ColumnTransformer` kursun (`verbose_feature_names_out=False`), çıktıyı
`set_output(transform="pandas")` ile DataFrame yapsın. `[sütunlar,
üçüncü_satırın_size_değeri]` döndürsün (`float`).

**Beklenen çıktı:**

```
size
city_Ankara
city_Bursa
city_Izmir
95.0
```
