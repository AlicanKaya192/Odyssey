Eşik bir ödünleşimdir: yükseldikçe daha çok ilgisiz metin reddedilir, ama
daha çok gerçek talep de cevapsız kalır. Birkaç eşik için üç oranı yan yana
koyalım:

```python
inside = engine.scores(queries).max(axis=1)
outside = [engine.scores(texts).max(axis=1) for texts in [reviews, world]]
for t in [0.3, 0.35, 0.4, 0.45, 0.5]:
    rejected = [round(float((top < t).mean()), 3) for top in outside]
    print(t, round(float((inside >= t).mean()), 3), *rejected)
```

```text
0.3 1.0 0.41 0.952
0.35 0.995 0.424 0.952
0.4 0.96 0.55 0.952
0.45 0.898 0.676 0.952
0.5 0.769 0.732 0.952
```

Sütunlar: eşik, cevaplanan gerçek talepler, reddedilen yorumlar, reddedilen
küçük dünya cümleleri.

- Eşik 0,3'ten 0,5'e çıkınca reddedilen yorumlar %41'den %73,2'ye çıkıyor;
  ama cevaplanan gerçek talepler %100'den %76,9'a iniyor. Her dört
  müşteriden biri cevapsız kalır.
- Küçük dünya cümlelerinde oran hep %95,2. Geçen %4,8'i "the bus is slow",
  "the taxi stopped at the depot" gibi cümleler: "slow" ve "stopped"
  taleplerde de geçiyor ("the website is very slow", "stopped working") ve bu
  cümleler yüksek puan alıyor; bu aralıktaki hiçbir eşik onları ayırmıyor.
- Eşiği sınav kümesine bakarak değil, **ayrı** bir doğrulama kümesinde
  seçmek gerekir; yoksa ölçülen oranlar iyimser çıkar. Burada gerçek
  taleplerin %5'ini kaybetmeyi göze aldık; bu oran bir ürün kararıdır,
  model kararı değil.
- Daha iyi ayrım için puanın yanında başka işaretler kullanılır: sorgunun
  sözlükteki kelime oranı, ilk iki sonuç arasındaki fark ya da "konu
  dışı" örneklerle eğitilmiş ayrı bir sınıflandırıcı.
