Notların **dağılımını** bir histogramla göreceksin ve grafiği rapora
girecek kalitede kaydedeceksin.

Veri `students.csv`:

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

1. İçe aktarmaları yaz ve dosyayı oku.
2. `score` sütununun **histogramını** çiz, `bins=5` kullan.
3. Başlığı `Score distribution`, x eksenini `Score`, y eksenini `Students`
   yap.
4. Grafiği **`histogram.png`** adıyla kaydet; `dpi=150` ve
   `bbox_inches="tight"` kullan. Sonra tuvali kapat.
5. Sırayla yazdır: çubuk sayısı, her aralıktaki öğrenci sayısı (liste
   olarak), ortalama (bir ondalık) ile medyan yan yana, başlık.

**Beklenen çıktı:**

```
5
[2, 3, 3, 2, 2]
77.4 77.5
Score distribution
```

Çalıştırdıktan sonra grafiğin **sonuç panelinde** görünecek.

**Bilmen gerekenler:**

- **Histogram çubuk grafikten farklı:** orada kategoriler var, burada
  **sayı aralıkları**. Ortalama tek bir sayı veriyor, histogram **şekli**
  gösteriyor — tek tepe mi, iki tepe mi, uç değerler nerede.
- `ax.hist` üç şey döndürüyor: her aralıktaki sayı, aralıkların sınırları
  ve çizilen çubuklar. Listeyi ilk parçadan alıyorsun.
- `dpi=150` rapora koyulacak çözünürlük; `bbox_inches="tight"` kenardaki
  fazla boşluğu kırpıyor.
- `plt.close(fig)` tuvali kapatıyor. Döngüde grafik üretiyorsan şart: yoksa
  açık tuvaller birikiyor.
