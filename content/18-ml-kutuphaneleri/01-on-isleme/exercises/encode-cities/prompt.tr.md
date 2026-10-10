`encode_cities(train, test)` şehirleri `OneHotEncoder` ile kodlasın: eğitim
şehirleriyle `fit`, test şehirleriyle `transform`. Testte eğitimde görülmemiş
şehir olabilir; hata vermemeli (`handle_unknown="ignore"`). Şunu döndürsün:

- `"names"`: `get_feature_names_out()` adları (liste)
- `"test"`: kodlanmış test, `int` liste listesi

Veriyi `pd.DataFrame({"city": ...})` olarak ver.

**Beklenen çıktı:**

```
['city_Ankara', 'city_Bursa', 'city_Izmir']
[[0, 0, 0], [0, 1, 0]]
```
