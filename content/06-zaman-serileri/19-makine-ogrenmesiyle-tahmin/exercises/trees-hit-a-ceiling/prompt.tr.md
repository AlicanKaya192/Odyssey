Gradyan artırmanın büyüyen bir seride neden geride kaldığını gör ve hedefi
değiştirerek düzelt.

**Yapman gerekenler:**

1. Eğitim verisindeki en yüksek `y` değerini ve 2024'teki en yüksek `y`
   değerini aynı satıra yazdır.
2. `HistGradientBoostingRegressor(random_state=0)` modelini düzey üzerinde kur
   ve 2024'ü tahmin et. En yüksek tahminini (bir ondalık) yazdır.
3. Test hatasını bütün 2024 için ve yalnızca Aralık 2024 için iki ondalıkla
   aynı satıra yazdır.
4. Hedefi farka çevir: `target = table["y"] - table["lag7"]`. Özelliklerden
   `lag7`'yi çıkar; `lag1`, `lag2`, `lag14`, `mean7`, `mean28` sütunlarından
   da `lag7`'yi çıkar (model hiçbir yerde ham düzeyi görmesin). Aynı modeli bu
   tabloda kur.
5. Tahmini düzeye çevir (model çıktısı + `lag7`) ve 3. adımdaki iki hatayı bu
   model için yazdır.
6. Yeni modelin en yüksek tahminini (bir ondalık) yazdır.

**Beklenen çıktı:**

```
462 503
415.7
14.63 22.47
11.74 10.87
494.5
```

Düzey üzerinde kurulan ağacın en yüksek tahmini, eğitimde gördüğü en yüksek
değerin bile altında; Aralık'ta hata bu yüzden büyük. Hedef fark olunca model
"geçen haftaya göre ne kadar değişir" sorusunu öğreniyor; düzeyi `lag7`
taşıyor ve tahmin artık eğitimdeki tavanı aşabiliyor.
