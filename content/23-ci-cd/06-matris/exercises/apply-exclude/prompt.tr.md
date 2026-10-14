`apply_exclude(combos, exclude)` fonksiyonunu yaz. `exclude` listesindeki **herhangi bir** kurala uyan birleşimleri çıkarıp kalanları sırayla döndürsün.

Bir birleşim bir kurala, kuraldaki **her** anahtar–değer çifti birleşimde de aynıysa uyar. Kural tam birleşim olmak zorunda değil: `{"os": "windows-latest"}` bütün Windows birleşimlerine uyar.

**Beklenen çıktı:**

```
{'os': 'ubuntu-latest', 'python': '3.12'}
{'os': 'ubuntu-latest', 'python': '3.13'}
{'os': 'windows-latest', 'python': '3.13'}
2
```
