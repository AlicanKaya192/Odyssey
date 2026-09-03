Bölüm 07 "tek ağaç kararsız" diyerek bitti ama bunu ölçmedik. Şimdi
ölçeceksin — ve ormanın onu ne kadar söndürdüğünü göreceksin.

**Yöntem:** eğitim verisinden her seferinde farklı bir %10'unu çıkarıp iki
modeli de yeniden eğit. Test kümesi hiç değişmiyor, yani skorlar
karşılaştırılabilir.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır.
2. `seed` değerini **0'dan 5'e** kadar değiştirerek altı tur yap. Her turda:
   - Eğitim verisinin **%90'ını** o tohumla örnekle, etiketleri eşle.
   - Bir **ağaç** eğit (`max_depth=3`, `random_state=42`).
   - Bir **orman** eğit (`n_estimators=200`, `random_state=42`).
   - İkisinin de test doğruluğunu ve **ağacın kök eşiğini** saklayın.
3. Üç listeyi ayrı satırlarda yazdır: ağaç skorları, orman skorları,
   kök eşikleri.
4. Son satırda iki aralığı yan yana yazdır: ağacın (en yüksek − en düşük)
   ve ormanınki (iki ondalık).

**Beklenen çıktı:**

```
[0.92, 0.88, 0.78, 0.8, 0.8, 0.84]
[0.9, 0.84, 0.86, 0.9, 0.9, 0.92]
[16.5, 15.5, 16.5, 18.5, 28.5, 18.5]
0.14 0.08
```

**Birinci satır: ağaç 0.78 ile 0.92 arasında geziniyor.** Model aynı model,
test kümesi aynı test kümesi. Değişen tek şey hangi %10'un düştüğü — ve
skor 14 puan oynuyor.

**Üçüncü satır daha rahatsız edici.** Kök bölünmesinin eşiği 15.5'ten
28.5'e çıkıyor. Yani modelin **kuralı** değişiyor: bir turda "ayda 16'dan
az girenler", başka bir turda "28'den az girenler".

Bunu bir paydaşa "keşfettiğimiz kural" diye sunduğunu düşün. On satır
sonra başka bir kural bulacaktın.

**İkinci satır: orman 0.84 ile 0.92 arasında.** 8 puanlık aralık, 14
yerine. Aynı gürültü, yarı yarıya sönmüş.

**Neden sönüyor:** tek ağacın hatası büyük ölçüde rastgele — şu satır düştü
diye eşik kaydı. Rastgele hataların ortalaması alındığında birbirini
götürüyor. Yüz ağaç yüz farklı örneklem gördüğü için yüz farklı yerde
yanılıyor ve ortalama sabitleniyor.

**Söndürmüyor, azaltıyor.** 0.08 hâlâ sıfır değil; topluluk sihir değil,
istatistik.
