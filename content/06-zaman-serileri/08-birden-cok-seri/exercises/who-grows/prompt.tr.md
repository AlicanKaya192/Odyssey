Ham satışlarda A her zaman önde. Büyümeyi karşılaştırmak için serileri
aynı noktadan başlat.

**Yapman gerekenler:**

1. `stores.csv` dosyasını oku ve geniş biçime çevir.
2. Aylık ortalamaları hesapla: `wide.resample("ME").mean()`.
3. Mayıs 2024'ü 100 kabul eden endeksi kur:
   `monthly / monthly.loc["2024-05-31"] * 100`.
4. Aralık 2024 endeks değerlerini bir ondalığa yuvarlayıp sözlük olarak
   yazdır.
5. Çeyreklik toplamlardan her mağazanın payını (yüzde) hesapla ve son
   çeyreğin paylarını bir ondalığa yuvarlayıp sözlük olarak yazdır.
6. A'nın payının ilk çeyrekten son çeyreğe kaç **puan** değiştiğini bir
   ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
{'A': 120.3, 'B': 116.8, 'C': 114.1, 'D': 182.2}
{'A': 35.7, 'B': 19.7, 'C': 22.9, 'D': 21.7}
-8.1
```

En küçük mağaza en hızlı büyüyen. A'nın payı düştü ama kendi satışı yüzde 20
arttı: pay, paydaya yeni bir mağaza girdiği için küçüldü.
