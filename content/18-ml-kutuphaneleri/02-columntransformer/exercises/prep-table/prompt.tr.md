`prep_table(rows)` `[size, city, id]` satırlarından bir DataFrame kursun ve
bir `ColumnTransformer` ile hazırlasın: `size` medyanla doldurulup
ölçeklensin, `city` `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`
ile kodlansın, `id` modele girmesin. `[şekil, adlar]` döndürsün: şekil
liste, adlar `get_feature_names_out()`. Başlangıç kodunda şehir parçası yok.

**Beklenen çıktı:**

```
[4, 4]
num__size
cat__city_Ankara
cat__city_Bursa
cat__city_Izmir
```
