Aynı tabloda üç modeli karşılaştır ve eğitim ile test hatası arasındaki
uçuruma bak.

**Yapman gerekenler:**

1. Üç model kur (hepsi `train[columns]`, `train["y"]` üzerinde):
   - `"linear"`: `LinearRegression()`
   - `"forest"`: `RandomForestRegressor(n_estimators=200, random_state=0)`
   - `"boosting"`: `HistGradientBoostingRegressor(random_state=0)`
2. Her biri için eğitim hatasını, test hatasını (MAE, iki ondalık) ve ikisinin
   oranını (test / eğitim, bir ondalık) `ad eğitim test oran` biçiminde alt
   alta yazdır.
3. Test hatası mevsimsel naiften (`test["lag7"]`) küçük olan modellerin
   adlarını liste olarak yazdır.

**Beklenen çıktı:**

```
linear 10.89 11.51 1.1
forest 4.31 12.87 3.0
boosting 4.79 14.63 3.1
['linear', 'forest']
```

Doğrusal modelde iki hata neredeyse aynı. Ağaç tabanlı iki model eğitim
verisini çok iyi "biliyor" ama testte doğrusal modelin gerisinde: 700 satır,
binlerce yaprağı olan bir modeli beslemeye yetmiyor. Gradyan artırma
mevsimsel naifi bile geçemiyor. Düşük eğitim hatası bir başarı değil, bir
uyarı.
