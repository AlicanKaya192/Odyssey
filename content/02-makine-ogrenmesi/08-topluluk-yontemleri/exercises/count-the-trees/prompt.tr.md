Orman kaç ağaçtan oluşmalı? Bölüm 05 ve 07'de derinliği artırmak bir
noktadan sonra zarar veriyordu. Burada da öyle mi?

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır.
2. Şu ağaç sayılarını dene: **1, 5, 25, 100, 300**.
3. Her biri için eğitim ve test doğruluğunu ölç, tek satır yazdır:
   **ağaç sayısı, eğitim, test**.
4. 25 ağacın test skoru ile 300 ağacınki aynıysa `same`, farklıysa
   `different` yazdır.

**Beklenen çıktı:**

```
1 0.947 0.72
5 0.993 0.84
25 1.0 0.9
100 1.0 0.9
300 1.0 0.9
same
```

**Tek ağaçla 0.72, 25 ağaçla 0.90.** Ağaç eklemek işe yarıyor — ama bir
yere kadar. 25'ten sonra hiçbir şey değişmiyor.

**Şimdi asıl önemli olana bak: eğitim sütunu 1.000'de sabit ama test
sütunu DÜŞMÜYOR.**

Bu, bölüm 05'te gördüğün her şeyin tersi. Orada derinlik artınca eğitim
1.000'e çıkıyor, test düşüyordu — aşırı öğrenme. Burada eğitim 1.000'de
ama test düşmüyor.

**Sebebi:** her ağaç veriyi farklı gördüğü için farklı şeyler ezberliyor.
Ezberler birbiriyle kesişmediğinden ortalama temiz kalıyor. Yüz ağacın
ortak yanlışı yok.

**Alınacak sonuç:** `n_estimators` bir denge parametresi değil, bir
**maliyet** parametresi. Artırmak modeli bozmuyor, yalnızca yavaşlatıyor.
100-300 arası yaygın bir başlangıç; daha fazlası genelde boşa zaman.

**Uyarı:** bu yalnızca **orman** için doğru. Gradyan artırmada ağaç sayısını
artırmak aşırı öğrenmeye yol açabiliyor, çünkü orada ağaçlar birbirini
düzeltiyor ve sonunda gürültüyü de düzeltmeye başlıyorlar.
