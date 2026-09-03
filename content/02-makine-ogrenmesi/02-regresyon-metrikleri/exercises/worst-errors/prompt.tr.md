Ölçüler tek sayı veriyor. Şimdi o sayının arkasına bakacak ve modelin
**hangi kayıtta** en çok yanıldığını bulacaksın.

**Yapman gerekenler:**

1. Alışıldık akışı kur: oku, `area` ile `price`'ı al, ayır
   (`random_state=42`), eğit, test tahminlerini üret.
2. Kalıntıları hesapla (`gerçek - tahmin`).
3. Kalıntıların **ortalamasını** iki ondalıkla yazdır.
4. **En büyük mutlak kalıntıyı** iki ondalıkla yazdır.
5. O kaydın **metrekaresini ve yaşını** yan yana, tam sayı olarak yazdır.
6. Kaç kalıntının pozitif, kaçının negatif olduğunu yan yana yazdır.

**Beklenen çıktı:**

```
-3.78
43.87
130 26
4 6
```

**Üçüncü satır bu alıştırmanın asıl bulgusu.** Modelin en çok yanıldığı ev
**26 yaşında** — veri kümesindeki en yaşlı evlerden biri. Model yaşı
bilmiyor, çünkü `X`'e yalnızca `area` koyduk. Tam olarak orada tökezliyor.

**Bu bir tesadüf mü, desen mi?** Tek kayıt söyleyemez. Bir sonraki alıştırma
bütün kalıntıları yaşa karşı çizip cevaplayacak.

**Birinci satır bir tuzak:** kalıntı ortalaması -3.78, sıfıra yakın. Bu bir
başarı işareti **değil**. Doğrusal regresyonun kalıntıları zaten sıfır
etrafında dengeleniyor; yöntemin bir sonucu. Ortalamaya değil **dağılıma**
bakılıyor.

**Son satır** dengeyi gösteriyor: 4 pozitif, 6 negatif. Belirgin bir
sistematik sapma yok — asıl sorun yönde değil, büyüklükte.
