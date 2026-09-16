Bir yılın aylık satışlarını **çizgi grafikle** göstereceksin.

Veri `sales.csv` dosyasında:

```text
month,sales
Jan,120
Feb,135
Mar,128
Apr,150
May,162
Jun,158
...
```

**Yapman gerekenler:**

1. İçe aktarmaları yaz ve dosyayı oku.
2. Ayları x, satışları y ekseninde gösteren bir çizgi grafik çiz; noktaları
   `marker="o"` ile işaretle.
3. Başlığı `Monthly sales`, y eksenini **birimiyle birlikte**
   `Sales (thousands)` yap.
4. Grafiği **`chart.png`** adıyla kaydet.
5. Sırayla yazdır: çizgi sayısı, satışın en yüksek olduğu ay, yıl sonu ile
   yıl başı arasındaki fark, y etiketi.

**Beklenen çıktı:**

```
1
Dec
110
Sales (thousands)
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**İki şey öğreniyorsun:**

- **Çubuk kategorileri karşılaştırır, çizgi bir şeyin nasıl değiştiğini
  gösterir.** Grafikte yıl boyunca yükselen bir eğilim ve arada küçük
  düşüşler görüyorsun; tabloda bu kadar kolay görünmüyordu.
- **Y etiketinde birim var.** Sadece `Sales` yazsaydın okuyan kişi adet mi,
  lira mı, bin lira mı diye tahmin etmek zorunda kalırdı.

En yüksek ayı bulurken `idxmax()` satırın **index'ini** veriyor; ayın adını
o satırdan `loc` ile alıyorsun.
