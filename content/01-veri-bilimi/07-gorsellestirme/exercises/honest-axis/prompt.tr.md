Aynı grafiği iki kez kaydedeceksin: bir kez **yanıltıcı**, bir kez
**dürüst**. İkisini yan yana görünce farkı unutmayacaksın.

Veri yine `students.csv`:

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

1. Dosyayı oku, şehre göre not ortalamasını hesapla ve çubuk grafik olarak
   çiz. Başlığı `Average score by city` yap.
2. Y eksenini **68 ile 90 arasına** sıkıştır ve **`misleading.png`**
   olarak kaydet. Eksenin alt ve üst sınırını yan yana, tam sayı olarak
   yazdır.
3. Aynı grafikte ekseni **0 ile 100 arasına** aç ve **`honest.png`** olarak
   kaydet. Sınırları yine yazdır.
4. En yüksek ortalamanın en düşüğe oranını iki ondalıkla yazdır.

**Beklenen çıktı:**

```
68 90
0 100
1.22
```

Çalıştırdıktan sonra iki grafik de **sonuç panelinde** görünecek.

**Oran neredeyse 1.2:** en iyi şehir en kötüsünden yaklaşık %20 önde. Şimdi
`misleading.png`'ye bak — orada fark **kat kat** görünüyor. Çünkü eksenin
alt kısmı kesildi ve çubuğun **uzunluğu** artık değerle orantılı değil.

**Kural:** çubuk grafikte ekseni sıfırdan başlat. Çizgi grafikte bu kural
yok; orada konu eğilim, büyüklük değil.
