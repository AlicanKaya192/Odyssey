Haftanın günlerine göre ortalama satışı çubuk grafiğiyle göster.

**Yapman gerekenler:**

1. Dosyayı oku ve haftanın gününe göre ortalamayı hesapla:
   `s.groupby(s.index.dayofweek).mean()`.
2. `labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]` ile çubuk
   grafiği çiz (`ax.bar(labels, profile.values)`) ve `chart.png` olarak
   kaydet.
3. Çubuk sayısını yazdır (`len(ax.patches)`).
4. Dikey eksenin alt sınırını yazdır (`ax.get_ylim()[0]`).
5. En yüksek ve en düşük günün adını ve ortalamasını (bir ondalık) alt alta
   yazdır.
6. Hafta sonu (cumartesi ve pazar) ortalamasının hafta içi ortalamasına
   oranını iki ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
7
0.0
Sat 336.1
Mon 217.6
1.33
```

Dikey eksen sıfırdan başlıyor: matplotlib çubuk grafiğinde bunu kendisi
yapıyor. Çubuğun boyu değeri anlattığı için doğrusu da bu; ekseni yukarıdan
başlatsaydın cumartesi ile pazartesi arasındaki fark olduğundan çok daha
büyük görünürdü.
