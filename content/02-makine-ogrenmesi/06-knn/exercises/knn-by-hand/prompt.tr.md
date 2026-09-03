Bölüm 00'da en yakın **tek** komşuyu bulmuştun. Şimdi `k` komşuya bakıp
**oylama** yapacaksın — ve `k`'nın cevabı değiştirdiğini göreceksin.

**Yapman gerekenler:**

1. Yeni noktanın her noktaya olan Öklid uzaklığını hesapla, iki ondalığa
   yuvarla.
2. `(uzaklık, etiket)` ikililerini **küçükten büyüğe** sırala.
3. Sıralı uzaklıkları liste hâlinde yazdır.
4. `k` değerini **1, 3 ve 5** yaparak sırayla:
   - en yakın `k` komşunun etiketlerini al
   - oy çokluğuna göre kazananı belirle
   - tek satır yazdır: **k, etiketler, kazanan**

**Beklenen çıktı:**

```
[0.71, 1.0, 2.92, 3.61, 4.03, 4.24, 4.3, 4.61]
1 ['A'] A
3 ['A', 'B', 'B'] B
5 ['A', 'B', 'B', 'A', 'B'] B
```

**İkinci ve üçüncü satıra dikkat: cevap değişti.**

`k=1` **A** diyor — en yakın komşu 0.71 uzaklıkta ve etiketi A.

`k=3` **B** diyor — üç komşudan ikisi B.

Aynı veri, aynı nokta, farklı sonuç. Demek ki `k` küçük bir ayrıntı değil;
**modelin kendisi.** Bir sonraki alıştırmalarda `k`'yı nasıl seçeceğin
konusuna geleceğiz.

**Tek sayı seçmenin sebebi de burada:** `k=2` olsaydı ve komşulardan biri A
biri B olsaydı oylar eşit kalırdı. İkili sınıflandırmada tek sayı seçmek bu
yüzden alışkanlık.
