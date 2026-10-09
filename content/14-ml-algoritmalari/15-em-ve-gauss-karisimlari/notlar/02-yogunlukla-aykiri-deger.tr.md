Bir GMM yalnızca kümeleri değil, verinin **yoğunluğunu** da öğrenir: her
noktaya "bu değer bu veride ne kadar olası" sorusunun cevabını verir. Bu,
aykırı değer (anomali) bulmanın basit bir yolu: yoğunluğu çok düşük olan
nokta şüphelidir.

Dersteki `x` ile:

```python
g = GaussianMixture(2, n_init=5, random_state=0).fit(x[:, None])
scores = g.score_samples(x[:, None])       # her noktanın log-yoğunluğu
threshold = np.percentile(scores, 1)       # en düşük %1
print(round(threshold, 2), int((scores < threshold).sum()))
for v in (0.0, 4.0, 9.0, -5.0):
    s = g.score_samples([[v]])[0]
    print(v, round(float(s), 2), s < threshold)
```

```text
-4.05 5
0.0 -1.46 False
4.0 -2.2 False
9.0 -8.71 True
-5.0 -12.68 True
```

Eşiği verinin en düşük %1'lik log-yoğunluğuna koyduk (−4,05); eğitim verisinin
5 noktası bunun altında. Yeni değerlerden 0 ve 4 bileşenlerin ortasında,
log-yoğunlukları yüksek (−1,46 ve −2,2). 9 ve −5 ise eşiğin çok altında
(−8,71 ve −12,68): ikisi de aykırı sayılıyor. −5'in 9'dan daha aykırı
çıkmasının sebebi, sol bileşenin dar (varyansı 1,12), sağdakinin geniş
olması: sağa doğru yoğunluk daha yavaş düşüyor.

Eşiği seçmek bir karar: %1 demek, temiz veride de her yüz noktadan birini
"aykırı" diye işaretlemeyi kabul etmek. Gerçek bir uygulamada eşik, yanlış
alarmın maliyetine göre seçilir.
