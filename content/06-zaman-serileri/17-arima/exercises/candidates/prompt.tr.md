Günlük satış için dört mevsimsel ARIMA adayını üç ölçütle karşılaştır: AIC,
kalıntı testi ve test hatası.

Başlangıç kodunda `train`, `test` ve `candidates` (dört mertebe çifti) hazır.

**Yapman gerekenler:**

1. Her aday için modeli kur
   (`ARIMA(train, order=order, seasonal_order=seasonal).fit()`) ve şunları
   hesapla:
   - AIC (bir ondalık)
   - Ljung–Box p-değeri: kalıntının ilk 8 değerini at, 14 gecikme (üç
     ondalık)
   - 28 günlük tahminin ortalama mutlak hatası (iki ondalık)
2. Her aday için `order seasonal AIC p MAE` biçiminde bir satır yazdır.
3. AIC'si en küçük adayın mertebesini yazdır.
4. Ljung–Box p-değeri 0.05'in üstünde olan adayların mertebelerini liste
   olarak yazdır.

**Beklenen çıktı:**

```
(0, 0, 0) (0, 1, 0, 7) 8782.5 0.0 11.64
(1, 0, 0) (0, 1, 1, 7) 8423.1 0.0 14.9
(0, 1, 1) (0, 1, 1, 7) 8265.8 0.035 10.48
(1, 1, 1) (0, 1, 1, 7) 8258.7 0.311 10.44
(1, 1, 1)
[(1, 1, 1)]
```

İlk satır mevsimsel naifin ARIMA yazımı: yalnızca mevsimsel fark. İkinci aday
AIC'de ondan çok iyi ama test hatası daha kötü ve kalıntısında hafıza var:
AIC tek başına yetmiyor. Yalnızca son aday üç ölçütü birden sağlıyor: en
küçük AIC, temiz kalıntı, en küçük test hatası.
