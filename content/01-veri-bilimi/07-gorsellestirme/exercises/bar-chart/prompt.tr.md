Şehirlerin not ortalamasını bir **çubuk grafikle** göstereceksin ve
çizdiğin grafiği göreceksin.

Veri `students.csv` dosyasında; ilk satırları şöyle:

```text
name,city,age,hours,score
Ada,Ankara,21,12,82
Kerem,Izmir,23,6,74
Mina,Ankara,22,14,91
Deniz,Bursa,25,4,68
Efe,Ankara,21,11,88
Sila,Izmir,24,8,76
...
```

**Yapman gerekenler:**

1. `pandas` ve `matplotlib.pyplot` kütüphanelerini içe aktar, dosyayı oku.
2. Şehre göre not ortalamasını hesapla.
3. Bir tuval ve çizim alanı oluştur (`plt.subplots()`), ortalamaları çubuk
   olarak çiz: yatayda şehirler, dikeyde ortalamalar.
4. Başlığı `Average score by city`, x eksenini `City`, y eksenini `Score`
   yap.
5. Grafiği **`chart.png`** adıyla kaydet.
6. Sırayla yazdır: çubuk sayısı, başlık, iki eksen etiketi (aralarında
   ` | ` ile).

**Beklenen çıktı:**

```
4
Average score by city
City | Score
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**Çubuk grafik kategorileri karşılaştırır.** Grupladığında elinde bir seri
oluyor: `index` şehirler, `values` sayılar. `ax.bar` ikisini ayrı istiyor,
bu yüzden `ax.bar(averages.index, averages.values)` yazılıyor.

`plt.show()` yazmana gerek yok; burada pencere yok, grafiği dosyaya
kaydediyorsun.
