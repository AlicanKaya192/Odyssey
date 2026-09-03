Bir önceki alıştırmada `18.5` çıktı. Bu iyi mi kötü mü?

Cevap sayının kendisinde değil, **kıyas noktasında**. Şimdi o noktayı
kuracak ve modeli ona karşı ölçeceksin.

**Yapman gerekenler:**

1. Dosyayı oku, `area` ile `price`'ı al, veriyi **aynı şekilde** ayır
   (dörtte biri test, `random_state=42`).
2. Taban çizgiyi kur: **eğitim** verisinin fiyat ortalaması. İki ondalıkla
   yazdır.
3. Taban çizginin test kümesindeki ortalama mutlak hatasını hesapla —
   her test kaydına aynı sayıyı tahmin ederek.
4. Modeli eğit ve onun ortalama mutlak hatasını hesapla.
5. İki hatayı **yan yana** yazdır: önce taban çizgi, sonra model (iki
   ondalık).
6. Model taban çizgiyi geçtiyse `better`, geçemediyse `worse` yazdır.

**Beklenen çıktı:**

```
312.87
82.29 18.5
better
```

**Birinci satır** taban çizginin tahmini: her eve 312.87 diyor. Kötü bir
tahmin ama bir tahmin — ve ölçülebiliyor.

**İkinci satır** işin özü. 82.29 hiçbir şey öğrenmeden ulaşılan hata; 18.5
metrekareye bakınca ulaşılan hata. Aradaki fark **modelin kattığı değer**:
hatanın %77'si.

Model 85 verseydi çıktı `worse` olurdu ve o üç satırlık kodun atılması
gerekirdi. Taban çizgi tam olarak bu kararı verebilmek için kuruluyor.

**Sıra önemli:** taban çizgi modelden **önce** hesaplanıyor. Sonra
hesaplandığında modelin sayısını görmüş oluyorsun ve beklentini ona göre
ayarlaman kolaylaşıyor.
