`two_processes.csv` Bölüm 12'den: `x` bir AR(1), `y` bir MA(1) süreciyle
üretildi, ikisi de katsayı 0.7 ile. Bunu bilmiyormuş gibi davran ve modele
sor.

**Yapman gerekenler:**

1. Dosyayı tarih indeksli `w` tablosu olarak oku.
2. Her seri için iki model kur: `order=(1, 0, 0)` ve `order=(0, 0, 1)`.
   AIC'lerini bir ondalıkla `seri AR_aic MA_aic` biçiminde alt alta yazdır.
3. Her seri için AIC'si küçük olan modelin katsayısını (`ar.L1` ya da
   `ma.L1`) iki ondalıkla `seri tür katsayı` biçiminde yazdır (tür `AR` ya da
   `MA`).
4. `x` serisine gereğinden büyük bir model kur: `order=(2, 0, 0)`. İkinci AR
   katsayısını (`ar.L2`) ve p-değerini (`fit.pvalues["ar.L2"]`) iki ondalıkla
   aynı satıra yazdır.
5. Aynı modelin AIC'sini AR(1)'in AIC'siyle birlikte bir ondalıkla aynı
   satıra yazdır (önce AR(1)).

**Beklenen çıktı:**

```
x 1622.9 1744.9
y 1722.5 1625.2
x AR 0.69
y MA 0.7
-0.02 0.64
1622.9 1624.7
```

AIC iki seride de doğru türü yüz puandan fazla farkla seçiyor ve katsayıyı
0.7 dolayında buluyor. Fazladan eklenen ikinci AR terimi sıfıra yakın,
p-değeri büyük ve AIC'yi **kötüleştiriyor**: gereksiz terimin üç işareti
birden.
