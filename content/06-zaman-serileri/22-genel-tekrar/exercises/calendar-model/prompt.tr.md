Taban çizgiyi (86.9) yen: gelecekte bilinen takvim özellikleriyle doğrusal bir
model kur ve hatanın kalanının nereden geldiğini ölç.

Başlangıç kodunda `features(index)` (trend, haftanın günü, yıllık Fourier,
tatil) ve `backtest(forecast)` hazır.

**Yapman gerekenler:**

1. `log_model(train, index)`: `LinearRegression`'ı `features(train.index)` ile
   `np.log(train)` üzerinde eğit; `index` için tahmini `np.exp` ile düzeye
   çevirip döndür. `backtest` sonucunu yazdır.
2. `level_model(train, index)`: aynısı, logaritmasız. Sonucu yazdır.
3. `weather_model(train, index)`: `log_model` ile aynı, ama özelliklere
   **gerçekleşen** havayı ekle: `features(...).join(weather)`. Sonucu yazdır.
4. Hava özellikli modeli bütün seriyle bir kez eğit. `rain` ve `holiday`
   katsayılarının `np.exp` değerini iki ondalıkla aynı satıra yazdır (çarpan
   olarak etki).
5. `log_model`'in ortalama MAE'sinin, dört haftalık gün ortalamasına (86.9)
   göre yüzde kaç düşük olduğunu tam sayı olarak yazdır.

**Beklenen çıktı:**

```
(65.1, 95.9)
(67.6, 104.7)
(20.9, 31.3)
0.62 1.14
25
```

Takvim modeli taban çizgiyi dörtte bir geçiyor; logaritma üzerinde kurmak hem
ortalamayı hem en kötü deneyi iyileştiriyor. Üçüncü satır bir model değil,
bir **sınır**: test günlerinin havası tahmin anında bilinmez. Ama kalan hatanın
nereden geldiğini gösteriyor: yağmurlu gün kiralamayı 0.62 katına indiriyor ve
model hangi günün yağmurlu olacağını bilmiyor.
