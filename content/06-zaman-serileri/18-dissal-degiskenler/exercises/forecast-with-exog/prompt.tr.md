Dış değişkenli modelden tahmin almak için gelecekteki değerleri de vermen
gerekir. Kasım 2024'ün ilk 28 gününü tahmin et.

Başlangıç kodunda `train`, `test` ve `columns` hazır. Bu alıştırmada gelecek
tablosu olarak `test[columns]`'ı, yani **gerçek** değerleri kullanacaksın;
bunun bir hile olduğunu bir sonraki alıştırmada ele alacağız.

**Yapman gerekenler:**

1. Dış değişkenli modeli kur (`order=(1, 0, 0)`,
   `seasonal_order=(0, 1, 1, 7)`).
2. 28 günlük tahmini al: `fit.forecast(28, exog=test[columns])`.
3. Aynı mertebeyle dış değişkensiz modelin 28 günlük tahminini al.
4. İki tahminin ortalama mutlak hatasını iki ondalıkla aynı satıra yazdır
   (önce değişkensiz).
5. Test dönemindeki kampanya günlerini `"%m-%d"` listesi olarak yazdır.
6. O günler için gerçek değeri, değişkensiz tahmini ve değişkenli tahmini tam
   sayıya yuvarlayıp gün başına bir satır yazdır.
7. Grafik çiz: gerçek değerler (gri) ve iki tahmin. `chart.png` olarak
   kaydet.

**Beklenen çıktı:**

```
17.56 11.07
['11-14', '11-15', '11-16']
285 285 294
314 286 304
243 211 223
```

Değişkensiz model kampanyanın geleceğini bilmiyor: üç günün ikisinde tahmini
gerçeğin 30 birim kadar altında. Değişkenli model tabloda `promo = 1` gördüğü
günlere ekleme yapıyor ve o iki günü yakalıyor. (İlk kampanya gününde satış
beklenenden düşük kalmış; tek tek günlerde gürültü hep olur, fark 28 günün
ortalamasında görünüyor.) Grafikte kampanya günlerindeki sıçramayı yalnızca
ikinci tahminin izlediğini göreceksin.
