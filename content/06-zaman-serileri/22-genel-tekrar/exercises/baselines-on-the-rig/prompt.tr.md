Doğrulama düzeneğini kur ve üç taban çizgiyi ölç: 13 başlangıç, her birinde
28 günlük tahmin.

Başlangıç kodunda `y` ve `cuts` hazır.

**Yapman gerekenler:**

1. `backtest(forecast)` fonksiyonunu yaz. `forecast(train, index)` biçiminde
   bir fonksiyon alır (28 değerlik dizi döndürür). Her kesimde eğitim
   `y.loc[:cut]`, test sonraki 28 gün; MAE hesaplanır. Ortalama MAE'yi ve en
   kötü deneyin MAE'sini bir ondalıkla demet olarak döndürsün.
2. Üç tahmin fonksiyonu yaz:
   - `naive`: eğitimin son değeri, 28 kez
   - `seasonal_naive`: eğitimin son 7 değeri, sırayla tekrar
   - `week_mean`: eğitimin son 28 gününün haftanın günü ortalaması, test
     günlerinin haftanın gününe göre (`index.dayofweek`)
3. Üçünün `backtest` sonucunu alt alta yazdır.
4. Test dönemindeki (3 Ocak 2024'ten sonra) ortalama günlük kiralamayı tam
   sayı olarak ve mevsimsel naif MAE'sinin bu ortalamaya yüzde oranını (tam
   sayı) aynı satıra yazdır.

**Beklenen çıktı:**

```
(112.2, 234.9)
(98.6, 199.1)
(86.9, 129.7)
410 24
```

Mevsimsel naif ortalama günün dörtte biri kadar yanılıyor ve en kötü deneyde
hatası iki katına çıkıyor. Dört haftanın gün ortalaması daha iyi ve çok daha
**istikrarlı** (en kötü deney 130). Bu seride tek bir gün çok gürültülü; taban
çizgi bile ortalama alarak kazanıyor. Yenilecek sayı artık 86.9.
