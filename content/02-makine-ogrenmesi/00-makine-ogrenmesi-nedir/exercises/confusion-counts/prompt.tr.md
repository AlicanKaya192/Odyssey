"%80 doğru" bir sayı, ama **hangi** %80? Bu alıştırmada o sayının içini
açacaksın.

Elinde on hastanın gerçek durumu (`1` hasta, `0` değil) ve bir modelin
tahmini var.

**Yapman gerekenler:**

1. Dört sayıyı hesapla:
   - **TP** — gerçek 1, tahmin 1 (hastayı buldu)
   - **TN** — gerçek 0, tahmin 0 (sağlıklıyı doğru bıraktı)
   - **FP** — gerçek 0, tahmin 1 (yok yere alarm)
   - **FN** — gerçek 1, tahmin 0 (**hastayı kaçırdı**)
2. Dördünü **tek satırda yan yana** yazdır: TP, TN, FP, FN.
3. Doğruluğu `(TP + TN) / toplam` olarak hesaplayıp iki ondalıkla yazdır.

**Beklenen çıktı:**

```
4 4 1 1
0.8
```

**İki hata aynı şey değil.** Bir FP, boşuna yapılan bir tetkik. Bir FN,
**gözden kaçan bir hasta**. Doğruluk ikisini de tek bir sayıya karıştırıp
"%80" diyor ve aradaki farkı siliyor.

Bu dört sayıya **karışıklık matrisi** deniyor ve sınıflandırmada asıl
bakılan şey o. 3. bölümün konusu.
