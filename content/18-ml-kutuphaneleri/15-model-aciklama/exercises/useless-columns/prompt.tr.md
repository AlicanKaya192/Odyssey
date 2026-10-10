`useless_columns(threshold)` **test verisindeki** permütasyon önemi
(`n_repeats=5`, `random_state=0`) `threshold`'dan küçük olan sütunların
adlarını döndürsün. Başlangıç kodu ormanın kendi önemini
(`feature_importances_`) kullanıyor ve anlamsız `row_id`'i atlıyor.

**Beklenen çıktı:**

```
['row_id', 'coin']
```
