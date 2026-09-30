Özellik tablosuyla bir doğrusal regresyon kur ve temel yöntemlerle
karşılaştır. Başlangıç kodunda `table`, `columns`, `train` (2023 sonuna kadar)
ve `test` (2024) hazır.

**Yapman gerekenler:**

1. `LinearRegression().fit(train[columns], train["y"])` kur ve 2024'ü tahmin
   et.
2. Üç yöntemin test hatasını (MAE) iki ondalıkla aynı satıra yazdır: naif
   (`test["lag1"]`), mevsimsel naif (`test["lag7"]`), doğrusal model.
3. Doğrusal modelin eğitim ve test hatasını iki ondalıkla aynı satıra yazdır.
4. Modelin mevsimsel naife göre becerisini (`1 - MAE / MAE_snaive`) iki
   ondalıkla yazdır.
5. Katsayıları `ad katsayı` biçiminde, iki ondalıkla, mutlak değeri büyükten
   küçüğe sıralı olarak yazdır.

**Beklenen çıktı:**

```
41.1 13.87 11.51
10.89 11.51
0.17
dow 2.07
month 1.4
lag14 0.43
lag7 0.42
mean7 0.14
lag1 0.05
mean28 -0.03
lag2 -0.02
```

Doğrusal model mevsimsel naifi geçiyor ve eğitim ile test hatası birbirine
yakın: ezber yok. Gecikmeler arasında en büyük ağırlık `lag14` ve `lag7`'de:
model geçen haftaların **aynı gününe** yaslanıyor, `lag1` neredeyse sıfır.
`dow` ve `month` katsayıları büyük görünüyor ama birimleri başka (gün ya da ay
numarası başına); katsayılar ancak aynı ölçekteki özellikler arasında
karşılaştırılır. `dow`'u tek sayı olarak vermek de doğrusal model için iyi bir
kodlama değil (notlara bak).
