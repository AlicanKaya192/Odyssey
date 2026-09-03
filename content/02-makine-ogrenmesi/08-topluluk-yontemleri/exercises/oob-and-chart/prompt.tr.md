Torbalamanın hoş bir yan ürünü var: her ağaç, eğitim verisinin yaklaşık
**üçte birini hiç görmüyor** — bootstrap örneklemine düşmeyen satırlar.
O satırlar o ağaç için hazır bir test kümesi.

sklearn bunu toplayıp **torba dışı skoru** (out-of-bag) veriyor: ayrı bir
doğrulama kümesi ayırmadan bir tahmin.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır.
2. Şu ağaç sayılarını dene: **10, 25, 50, 100, 200**. Her modele
   `oob_score=True` ver.
3. Her biri için tek satır yazdır: **ağaç sayısı, OOB skoru, test skoru**
   (üç ondalık). İkisini de listelerde birikt.
4. İki eğriyi aynı grafiğe çiz (`oob` ve `test` etiketleriyle,
   `marker="o"`), eksenleri `trees` ve `accuracy` diye adlandır, başlık
   koy, `legend` ekle ve `chart.png` olarak kaydet.
5. **En yüksek ağaç sayısındaki** OOB ile test skoru arasındaki farkı
   yazdır (mutlak değer, üç ondalık).

**Beklenen çıktı:**

```
10 0.873 0.86
25 0.873 0.9
50 0.88 0.88
100 0.893 0.9
200 0.887 0.9
0.013
```

Grafiğin çalıştırma sonrası **sonuç panelinde** görünecek.

**İki eğri birbirine yakın seyrediyor.** OOB, test skorunu iyi tahmin
ediyor — ve bunu **test kümesine hiç dokunmadan** yapıyor.

**Neden değerli:** çapraz doğrulama her kat için modeli baştan eğitiyor;
5 kat = 5 eğitim. OOB ise **zaten eğitilmiş** ağaçlardan hesaplanıyor, ek
maliyeti yok. Büyük veride bu ciddi bir fark.

**Ama test kümesinin yerini almıyor.** OOB eğitim verisinden geliyor;
model seçimi ve ayar için kullanılabiliyor, son rapor hâlâ el değmemiş
test kümesinde yapılıyor.

**Az ağaçta güvenilmez:** 10 ağaçta her satır ortalama 3-4 ağacın torba
dışında kalıyor, bu da gürültülü bir tahmin demek. Ağaç sayısı arttıkça
OOB kararlı hâle geliyor — grafikte de bunu görüyorsun.

**Bir koşul:** `oob_score` yalnızca `bootstrap=True` iken çalışıyor. Örneklem
yerine koyarak çekilmezse torba dışında kalan satır olmuyor.
