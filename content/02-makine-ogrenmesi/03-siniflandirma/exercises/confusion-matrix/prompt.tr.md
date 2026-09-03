Doğruluk %85 çıktı. Peki **hangi** %85? Bu alıştırmada o sayının içini
açacaksın.

**Yapman gerekenler:**

1. Önceki alıştırmadaki akışı kur (aynı ayrım, aynı model).
2. **Karışıklık matrisini** hesapla ve `.tolist()` ile listeye çevirip
   yazdır.
3. Matristen dört sayıyı çıkar ve **tek satırda yan yana** yazdır:
   TN, FP, FN, TP.
4. Doğruluğu bu dört sayıdan hesapla: `(TN + TP) / toplam`. Üç ondalıkla
   yazdır.
5. Hangi hata türü daha çok? Yanlış pozitif fazlaysa `FP`, yanlış negatif
   fazlaysa `FN` yazdır.

**Beklenen çıktı:**

```
[[8, 5], [1, 26]]
8 5 1 26
0.85
FP
```

**Matrisin okunuşu:** satırlar **gerçek**, sütunlar **tahmin**. Sol üst
köşe her zaman TN.

```
                tahmin 0   tahmin 1
gercek 0            8          5      <- 5 yanlis pozitif
gercek 1            1         26      <- 1 yanlis negatif
```

**Son satır asıl bulgu.** Model 5 kez kalacak öğrenciye "geçti" dedi ama
yalnızca 1 kez geçecek öğrenciye "kaldı" dedi. Yani **"geçti" demeye
eğilimli**.

Bu iyi mi kötü mü? Modele değil, kararın ne için kullanıldığına bağlı:

- **Burs** kararıysa hak etmeyene burs vermek (FP) pahalı — bu model kötü.
- **Destek dersi** kararıysa ihtiyacı olanı kaçırmak (FN) pahalı — bu model
  iyi.

Aynı dört sayı, iki farklı sonuç. Doğruluk %85 diyerek bu ayrımı tamamen
gizliyordu.
