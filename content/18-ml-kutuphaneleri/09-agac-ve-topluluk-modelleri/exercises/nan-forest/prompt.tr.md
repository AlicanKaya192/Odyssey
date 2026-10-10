`nan_forest(rate)` eğitim verisindeki hücrelerin `rate` oranını `NaN` yapıyor.
Rastgele orman `NaN`'ı doğrudan kabul ettiği için bu eksikleri **doldurmadan**
eğitip test skorunu (3 basamak) döndürsün. Başlangıç kodu eksikleri 0 ile
dolduruyor (`np.nan_to_num`).

**Beklenen çıktı:**

```
0.9
0.893
```
