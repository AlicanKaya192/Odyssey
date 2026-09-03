Bir modeli eğittiğin veriyle sınamak, öğrenciye sınav sorularını önceden
vermek gibi. Bu yüzden veri **ikiye ayrılıyor** — ve bu alıştırmada o
ayrımı elle yapacaksın.

**Yapman gerekenler:**

1. Kayıtların **%70'inin** kaç kayıt ettiğini hesapla.
2. İlk bu kadarını **eğitim**, kalanını **test** olarak ayır.
3. Eğitim ve test kayıt sayılarını **yan yana** yazdır.
4. Test kümesinin **ilk kaydını** yazdır.
5. **Yalnızca eğitim** kayıtlarının not ortalamasını iki ondalığa
   yuvarlayarak yazdır.

**Beklenen çıktı:**

```
7 3
('Ela', 83)
69.86
```

**Son satır bu alıştırmanın asıl konusu.** Ortalamayı bütün veriden
hesaplamak kolay olurdu; ama o ortalama daha sonra bir tahmin olarak
kullanılacaksa, test kayıtlarının bilgisini içeriyor demektir. Modelin
görmemesi gereken veri, hesabına da girmemeli.

Gerçekte bu ayrımı `train_test_split` yapıyor — bir sonraki bölümde. Önce
ne yaptığını bilmen gerekiyor.
