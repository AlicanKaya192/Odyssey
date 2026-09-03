Üç ölçüyü kütüphane çağırmadan kuracaksın. Formülü bir kez elle yazmak,
sonraki bütün bölümlerde o sayıların ne anlattığını bilmeni sağlıyor.

Elinde sekiz evin gerçek fiyatı ve bir modelin tahminleri var.

**Yapman gerekenler:**

1. Her kayıt için **kalıntıyı** hesapla (`gerçek - tahmin`) ve listeyi
   olduğu gibi yazdır.
2. **MAE**'yi hesapla: kalıntıların mutlak değerlerinin ortalaması. İki
   ondalıkla yazdır.
3. **MSE**'yi hesapla: kalıntıların karelerinin ortalaması.
4. **RMSE**'yi hesapla: MSE'nin karekökü.
5. MSE ile RMSE'yi **yan yana** yazdır (iki ondalık).

**Beklenen çıktı:**

```
[12, -7, -15, 15, -15, 30, -8, 10]
14.0
241.5 15.54
```

**Birinci satırdaki işaretlere bak.** Pozitif kalıntı, modelin **düşük**
tahmin ettiği anlamına geliyor; negatif kalıntı yüksek tahmin ettiği.
Toplamları alsaydın +12 ile -15 birbirini götürürdü ve model olduğundan iyi
görünürdü. Hem mutlak değer hem kare tam olarak bunu engelliyor.

**MAE 14.0, RMSE 15.54.** RMSE daha büyük — ve her zaman büyük ya da eşit
olacak. Aradaki fark, listedeki `30`'dan geliyor: kare almak büyük hatayı
orantısız cezalandırıyor. Fark ne kadar büyükse, birkaç büyük hatanın
olduğuna o kadar emin olabilirsin.

**MSE'nin 241.5 çıkması dikkat çekici:** birimi hedefin biriminin karesi
olduğu için sayı kendi başına hiçbir şey anlatmıyor. Karekökü alınmasının
sebebi bu.
