Sınıflandırmada iki tür hata var ve ikisi neredeyse hiçbir zaman aynı
ağırlıkta değil. Bu notun tamamı tek bir sorunun etrafında: **yanlış alarm
mı daha pahalı, kaçırmak mı?**

## İki hata

| Hata | Ne oluyor | Maliyeti |
|---|---|---|
| **Yanlış pozitif (FP)** | Olmayanı var sandın | Boşa harcanan kaynak, gereksiz endişe |
| **Yanlış negatif (FN)** | Olanı kaçırdın | Gözden kaçan durum, geç kalınmış müdahale |

Doğruluk (accuracy) ikisini tek sayıya karıştırıp bu farkı **siliyor.**
İki modelin doğruluğu aynı olabilir ama biri kaçırıyor, öteki yanlış alarm
veriyor — ve bu fark her şeyi değiştiriyor.

## Karar tablosu

| Alan | Pahalı olan | Öncelik | Eşik |
|---|---|---|---|
| Kanser taraması | Hastayı kaçırmak | Recall | Düşür |
| Dolandırıcılık tespiti | Kaçan işlem | Recall | Düşür |
| Arıza öngörüsü | Patlayan makine | Recall | Düşür |
| Spam filtresi | Gerçek e-postayı silmek | Precision | Yükselt |
| İçerik önerisi | Kötü öneri | Precision | Yükselt |
| Otomatik kredi onayı | Batak krediye onay | Precision | Yükselt |
| İşe alım ön elemesi | İyi adayı elemek | Recall | Düşür |

**Ortak nokta:** bir tarafta bir şeyi **kaçırmanın** bedeli, öteki tarafta
**gereksiz iş yapmanın** bedeli var. Hangisi büyükse ölçü o.

## Sorulacak sorular

**1. Bir kaçırma geri alınabilir mi?**

Kaçan hastalık teşhisi ilerliyor; kaçan spam ise silinip geçiliyor.
Geri alınamayan hatalar recall'a ağırlık verdiriyor.

**2. Yanlış alarmın ardından ne oluyor?**

Bir insan kontrol ediyorsa yanlış alarm ucuz — sadece zaman. Otomatik bir
işlem tetikleniyorsa pahalı.

**3. Sonuç kime gidiyor?**

Uzmana giden bir liste geniş olabilir (recall). Doğrudan kullanıcıya giden
bir karar temiz olmalı (precision).

**4. Kaç tane pozitif var?**

Bin kayıtta on pozitif varsa recall'ı yükseltmek yüzlerce yanlış alarm
getiriyor. Dengesiz veride takas çok daha sert.

## Eşikle ayar yapmak

Modeli yeniden eğitmeden karar noktası kaydırılabiliyor:

```python
probability = model.predict_proba(X_test)[:, 1]

screening = (probability >= 0.30).astype(int)   # kacirma azalir
spam_filter = (probability >= 0.80).astype(int) # yanlis alarm azalir
```

| Eşik | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Düşük | ↑ | ↑ | ↓ | ↓ | ↑ |
| Yüksek | ↓ | ↓ | ↑ | ↑ | ↓ |

**Bedava iyileşme yok.** Eşik oynatmak bir hatayı azaltırken ötekini
artırıyor. Gerçek iyileşme ancak daha iyi bir model ya da daha iyi
özelliklerle geliyor.

## Eşik nerede seçilir

Eşik bir **hiperparametre**: doğrulama kümesinde seçiliyor, test kümesinde
değil. Test kümesine bakıp eşik ayarlamak, test skorunu dürüst olmaktan
çıkarıyor.

Pratik yol:

1. Modeli eğitim kümesinde eğit.
2. Doğrulama kümesinde birçok eşiği dene, precision ve recall'ı çıkar.
3. Problemin gerektirdiği eşiği seç ("recall en az 0.90 olsun" gibi).
4. Test kümesinde **bir kez** ölç.

## Bir kısıt koymak

Çoğu gerçek projede karar şöyle veriliyor: **bir tarafa alt sınır konup
öteki en iyilenir.**

- "Recall en az %90 olsun, precision'ı elinden geldiğince yükselt."
  → Hastalık taraması.
- "Precision en az %95 olsun, recall'ı elinden geldiğince yükselt."
  → Otomatik onay sistemi.

Bu kısıt teknik bir karar değil; alan bilgisiyle, işi yapan kişiyle
konuşarak belirleniyor. Modeli kuran kişi bu sayıyı tek başına
uyduramıyor.

## F1 ne zaman yeterli

F1 precision ve recall'ı eşit ağırlıkta topluyor. Bu ancak iki hatanın
maliyeti gerçekten yakınsa doğru.

Değilse ağırlıklı hâli kullanılıyor:

```python
from sklearn.metrics import fbeta_score

fbeta_score(y_test, prediction, beta=2)     # recall'a agirlik
fbeta_score(y_test, prediction, beta=0.5)   # precision'a agirlik
```

`beta > 1` recall'ı, `beta < 1` precision'ı öne çıkarıyor. `beta=1` F1'in
kendisi.

## Raporlarken

Tek sayı yeterli değil. Bir sınıflandırma sonucu şunları taşıyor:

- Precision ve recall **ayrı ayrı** (F1 varsa ek olarak)
- Karışıklık matrisinin dört sayısı
- Taban çizginin doğruluğu
- Hangi eşiğin kullanıldığı
- Her sınıfta kaç kayıt olduğu (`support`)

**Eşiği yazmak özellikle önemli:** aynı model farklı eşiklerle bambaşka
sayılar üretiyor ve eşik yazılmamışsa sonuç tekrar edilemiyor.
