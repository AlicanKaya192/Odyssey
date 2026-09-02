`score` sütunu metin tipinde ve içinde iki sahte değer var: `"abc"` ve
`"-1"`. İkisi de "bilinmiyor" demek ama farklı görünüyorlar.

**Yapman gerekenler:**

1. `score` sütununu sayıya çevir. Çevrilemeyen değerler **hata vermek
   yerine** boş kalsın.
2. `-1` değerini gerçek bir eksik değere (`np.nan`) çevir.
3. Sütunun değerlerini liste hâlinde yazdır.
4. Sütunun tipini yazdır.
5. Kaç eksik değer olduğunu yazdır.

**Beklenen çıktı:**

```
[82.0, 74.0, 91.0, 82.0, nan, 88.0, nan]
float64
2
```

**İki önemli nokta:**

- `astype(float)` deneseydin `"abc"` yüzünden **bütün program** hata
  verirdi. `pd.to_numeric(..., errors="coerce")` sorunu tek bir hücreye
  hapsediyor.
- `-1` sayıya çevriliyor ama **gerçek bir not değil**. Öyle bırakırsan
  ortalamaya karışıyor ve sonucu bozuyor. Gerçek veride `-1`, `999`,
  `"N/A"` gibi sahte eksikler çok yaygın.

Sonucun `float64` olmasının sebebi: tamsayı tipi `NaN` tutamıyor.
