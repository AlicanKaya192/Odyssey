Abone sayısının büyümesi bir yerde yavaşlamış. Günü bul ve tahmine etkisini
gör.

Başlangıç kodunda `s` (abone sayısı), `t` (0'dan başlayan gün sayacı) ve `y`
(değerler, numpy dizisi) hazır.

**Yapman gerekenler:**

1. Bütün seriye tek doğru uydur (`np.polyfit(t, y, 1)`); eğimi iki ondalıkla
   yazdır.
2. Bu doğrunun kalıntısını hesapla. İlk günün kalıntısını, en büyük kalıntıyı,
   onun gününü (`"%m-%d"`) ve son günün kalıntısını (tam sayılar) aynı satıra
   yazdır.
3. Kırılma gününü ara: 30 ile `len(y) - 30` arasındaki her `k` için iki
   parçaya ayrı birer doğru uydur ve kalıntı kareleri toplamını topla; en
   küçüğü veren `k`'yi bul. Kırılma gününü (`"%Y-%m-%d"`) ve iki eğimi (iki
   ondalık) aynı satıra yazdır.
4. 30 gün sonrası (`t = len(y) - 1 + 30`) için iki tahmin yap: tek doğruyla ve
   yalnızca son 60 güne uydurulan doğruyla. İkisini tam sayı olarak aynı
   satıra yazdır.
5. Grafik çiz: seri, tek doğru ve iki parçalı doğru. `chart.png` olarak kaydet.

**Beklenen çıktı:**

```
8.98
-284 332 07-17 -356
2024-07-17 11.99 5.04
4832 4373
```

Tek doğrunun eğimi (günde 9 abone) iki dönemin hiçbirini anlatmıyor: önce 12,
sonra 5. Kalıntının uçlarda eksi, ortada artı olması (ters V) bunun imzası.
Tahminde fark büyük: tek doğru bir ay sonrası için 460 abone fazla söylüyor.
