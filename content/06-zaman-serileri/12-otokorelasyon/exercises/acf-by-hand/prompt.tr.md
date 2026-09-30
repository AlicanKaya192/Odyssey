Günlük satışın ilk 7 gecikmesindeki otokorelasyonu önce elle, sonra
`acf` ile hesapla.

**Yapman gerekenler:**

1. 1'den 7'ye her gecikme için `s.corr(s.shift(k))` hesapla; iki ondalığa
   yuvarlayıp liste olarak yazdır.
2. `acf(s, nlags=7)` çağır; gecikme 0'ı atıp (`[1:]`) iki ondalığa yuvarlayıp
   liste olarak yazdır.
3. `acf` sonucunda en yüksek değerin hangi gecikmede olduğunu yazdır (gecikme
   0 hariç).
4. `acf` dizisinin uzunluğunu ve ilk elemanını aynı satıra yazdır.

**Beklenen çıktı:**

```
[0.69, 0.28, 0.11, 0.1, 0.27, 0.68, 0.96]
[0.69, 0.28, 0.11, 0.1, 0.26, 0.67, 0.94]
7
8 1.0
```

İki liste çok yakın ama aynı değil: `acf` her gecikmede serinin tamamının
ortalamasını ve varyansını kullanıyor. İkisi de aynı hikâyeyi anlatıyor: en
güçlü bağ 7 gün öncesiyle.
