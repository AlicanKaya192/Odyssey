Önceki alıştırmada tek bir ayrımın 16.16 ile 21.56 arasında herhangi bir
sayı verebildiğini gördün. Çözüm: bir kez değil, **beş kez** ölç ve
ortalamasını al.

Çapraz doğrulama veriyi beş parçaya bölüyor ve her parçayı sırayla test
yapıyor. Her kayıt tam bir kez test ediliyor, tam dört kez eğitimde
kullanılıyor.

**Yapman gerekenler:**

1. Veriyi hazırla; yine **ayırma**, çapraz doğrulama bölmeyi kendisi
   yapıyor.
2. `KFold` kur: **5 kat**, `shuffle=True`, `random_state=42`.
3. `cross_val_score` ile doğrusal regresyonu ölç.
   `scoring="neg_mean_absolute_error"` kullan.
4. Skorların işaretini çevirip iki ondalığa yuvarla ve listeyi yazdır.
5. **Ortalamayı ve yayılımı** (standart sapma) yan yana yazdır (iki
   ondalık).
6. Önceki alıştırmada `random_state=2` ile **17.07** çıkmıştı. Bu sayı
   katların en düşüğü ile en yükseği **arasında** kalıyorsa `inside`,
   kalmıyorsa `outside` yazdır.

**Beklenen çıktı:**

```
[14.97, 15.96, 19.29, 19.63, 12.64]
16.5 2.65
inside
```

**İki sayı birden çıkıyor ve ikincisi en az birincisi kadar değerli.**

- **16.50** modelin beklenen hatası — beş ölçümün ortalaması, tek bir
  ayrımdan çok daha sağlam.
- **2.65** o sayının ne kadar oynadığı. Katlar 12.64 ile 19.63 arasında
  geziniyor.

**Üçüncü satır bir kontrol.** Tek ayrımdan gelen 17.07, katların aralığının
içinde kalıyor — yani o sayı yanlış değildi, yalnızca **tek bir çekiliş**ti.

**Bunun pratik sonucu:** iki modelin ortalaması 16.5 ve 17.2 ise ve yayılım
2.65 ise, aradaki 0.7'lik fark gürültünün içinde kalıyor. "Şu model daha
iyi" demeden önce farkın yayılımdan büyük olması gerekiyor.

**`neg_` öneki tuhaf ama sebebi var:** sklearn her skoru "büyük olan iyidir"
diye ele alıyor. Hata için bu ters olduğundan işaret çevriliyor.

**`float()` neden gerekiyor:** NumPy sayılarını doğrudan listeye koyarsan
çıktıda `[np.float64(14.97), ...]` görünüyor. `float()` bunu temizliyor.
