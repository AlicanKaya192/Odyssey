Gerçek veride hücreler boş oluyor. Altı notun ikisi eksik; onları
bulacak, ortalamayla dolduracaksın.

**Yapman gerekenler:**

1. `scores` dizisi başlangıç kodunda hazır, içinde iki `np.nan` var.
2. Kaç tane eksik değer olduğunu bul, `missing` değişkeninde tut.
3. Eksikleri **saymadan** ortalamayı hesapla, `average` değişkeninde tut.
4. `scores` dizisinin bir **kopyasını** al (adı `filled` olsun) ve boş
   hücreleri bu ortalamayla doldur.
5. Sırayla yazdır: `missing`, `average`, `filled`, ve `filled` dizisinin
   ortalaması (iki basamağa yuvarlanmış).

**Beklenen çıktı:**

```
2
75.0
[80. 75. 90. 70. 75. 60.]
75.0
```

**İki tuzak var:**

- `scores.mean()` sana `nan` verir — tek bir eksik değer bütün sonucu
  bozuyor. `np.nanmean` gerekiyor.
- **Kopya almadan** doldurursan özgün diziyi bozarsın. NumPy'da atama ve
  dilim aynı veriye dokunuyor; `.copy()` şart.

Son satırdaki ortalamanın `average` ile aynı çıkması tesadüf değil: boşları
ortalamayla doldurmak ortalamayı değiştirmiyor. Bu, gerçek veri işlerinde
bilinçli olarak kullanılan bir yöntem.
