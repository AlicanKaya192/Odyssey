Fiyat serisinin ve günlük değişiminin korelogramını güven bandıyla
karşılaştır.

**Yapman gerekenler:**

1. `outside(x, nlags=20)` adında bir fonksiyon yaz: `acf(x, nlags=nlags)`
   hesaplasın, bandı `1.96 / np.sqrt(len(x))` olarak alsın ve gecikme 0 hariç,
   mutlak değeri bandı aşan **gecikme numaralarını** liste olarak döndürsün.
2. Günlük değişim (`k.diff().dropna()`) için bandı üç ondalığa yuvarlayıp
   yazdır.
3. Günlük değişimde bandı aşan gecikmeleri yazdır.
4. Fiyatın kendisinde bandı aşan gecikme **sayısını** yazdır.
5. Fiyatın ACF'sini 1, 10 ve 20. gecikmelerde iki ondalığa yuvarlayıp liste
   olarak yazdır.

**Beklenen çıktı:**

```
0.07
[2]
20
[0.99, 0.87, 0.76]
```

Günlük değişimde 20 gecikmeden yalnızca biri bandı aşıyor; %95'lik bir bantta
şans eseri beklenen de bu kadar. Fiyatın kendisinde 20'nin 20'si dışarıda ve
çok yavaş sönüyor: bu hafıza değil, trend.
