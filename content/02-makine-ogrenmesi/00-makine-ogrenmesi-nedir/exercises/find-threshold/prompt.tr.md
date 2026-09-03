Bu alıştırmada bir model **eğiteceksin** — kütüphane olmadan.

Elinde on öğrencinin notu ve geçip geçmediği var. Geçme eşiğinin kaç
olduğunu bilmiyorsun; **veriden bulacaksın.**

**Yapman gerekenler:**

1. 30'dan 100'e kadar beşer beşer bütün eşikleri dene.
2. Her eşik için tahmin üret: nota bakıp eşiğin üstündeyse 1, değilse 0.
3. Tahminlerin kaçının gerçekle uyuştuğunu say ve oranı hesapla.
4. **En yüksek oranı veren** eşiği ve o oranı yan yana yazdır (oran iki
   ondalık).

**Beklenen çıktı:**

```
55 0.9
```

**İşte bu, öğrenmenin kendisi.** Yaptığın şey bir döngüyle parametre
aramaktı; doğrusal regresyonun yaptığı da aynı iş — yalnızca aradığı sayı
bir eşik değil, bir eğim ve bir kesişim, ve arama akıllıca yapılıyor.

Model %90'da kaldı, %100'e çıkmadı: veride 66 alıp kalan ve 60 alıp geçen
biri var. **Hiçbir eşik ikisini birden doğru yapamıyor.** Gerçek veri
böyle; kusursuz sonuç genelde bir hatanın işareti.
