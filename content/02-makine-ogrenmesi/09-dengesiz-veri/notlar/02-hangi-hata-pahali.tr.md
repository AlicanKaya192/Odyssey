Dengesiz veride bütün ayarlar tek bir soruya bağlanıyor: **iki hata
türünden hangisi daha pahalı?** Bu soruya cevap vermeden yapılan her eşik
ve ağırlık seçimi rastgele.

## İki hata

| | Adı | Ne oluyor |
|---|---|---|
| **FN** | Kaçırma (false negative) | Gerçek pozitife "negatif" dedin |
| **FP** | Yanlış alarm (false positive) | Gerçek negatife "pozitif" dedin |

Karışıklık matrisinde ikisi köşegenin dışındaki iki hücre. Toplamları
hatanın tamamı — ama **aynı şey değiller.**

## Recall'ün pahalı olduğu durumlar

Kaçırmanın bedeli yanlış alarmdan büyükse **recall** öne çıkıyor.

| Problem | Kaçırırsan | Yanlış alarm verirsen |
|---|---|---|
| Kanser taraması | Hasta tedavi görmüyor | Bir tetkik daha yapılıyor |
| Dolandırıcılık | Para gidiyor | Müşteri arayıp doğruluyor |
| Uçak bakımı | Arıza uçuşta çıkıyor | Fazladan kontrol |
| Deprem uyarısı | Hazırlıksız yakalanıyorsun | Boşuna tatbikat |

Ortak yanı: kaçırmanın sonucu **geri alınamaz**, yanlış alarmın sonucu
**can sıkıcı ama düzeltilebilir**.

Bu durumda `class_weight="balanced"` ve düşük eşik mantıklı.

## Precision'ın pahalı olduğu durumlar

Yanlış alarmın bedeli büyükse **precision** öne çıkıyor.

| Problem | Yanlış alarm verirsen | Kaçırırsan |
|---|---|---|
| Spam filtresi | Önemli e-posta çöpe gidiyor | Bir spam gelen kutusunda |
| İçerik kaldırma | Masum kullanıcı susturuluyor | Bir kötü içerik kalıyor |
| Kredi reddi | Ödeyecek müşteri kaybediliyor | Bir batak kredi |
| İşe alım eleme | İyi aday elenip haberi bile olmuyor | Bir kötü mülakat |

Ortak yanı: yanlış alarm **bir kişiye zarar veriyor** ve o kişi çoğu zaman
itiraz edemiyor.

Bu durumda yüksek eşik ve `class_weight` vermemek mantıklı.

## Sayıya dökmek

Maliyetler biliniyorsa eşik F1'e göre değil, doğrudan **beklenen maliyete**
göre seçilebiliyor:

```
maliyet = FN_sayisi * FN_bedeli + FP_sayisi * FP_bedeli
```

Örnek: bir kaçırma 400 lira, bir yanlış alarm 5 lira (arama maliyeti).

| Eşik | FN | FP | Maliyet |
|---|---|---|---|
| 0.50 | 15 | 2 | 15*400 + 2*5 = **6010** |
| 0.20 | 14 | 7 | 14*400 + 7*5 = **5635** |
| 0.10 | 8 | 25 | 8*400 + 25*5 = **3325** |
| 0.05 | 5 | 45 | 5*400 + 45*5 = **2225** |

Bu maliyetlerle **0.05 kazanıyor** — F1'in seçtiği 0.10 değil. Çünkü F1
precision ile recall'ü eşit önemde sayıyor; iş dünyası öyle saymıyor.

Yanlış alarm 5 lira değil de 100 lira olsaydı (diyelim ki her alarm bir
müşteriyi kaybettiriyor) tablo başka bir yeri gösterirdi:

| Eşik | Maliyet (FP = 100) |
|---|---|
| 0.50 | 6200 |
| 0.20 | 6300 |
| 0.10 | **5700** |
| 0.05 | 6500 |

**Aynı model, aynı olasılıklar, farklı karar.** Değişen tek şey bir sayı:
yanlış alarmın bedeli.

## Maliyet bilinmiyorsa

Çoğu zaman kimse "bir kaçırma kaç lira" sorusuna cevap veremiyor. O zaman:

1. **Tabloyu sun, karar verme.** Eşik taramasının çıktısını iş tarafına
   götür. "0.10'da 13 dolandırıcılık yakalıyoruz ve 25 müşteriyi boşuna
   arıyoruz" cümlesi, "F1 skorumuz 0.441" cümlesinden çok daha
   konuşulabilir.
2. **Bir kısıt belirleyin.** "Günde en fazla 30 yanlış alarm kaldırabiliriz"
   gibi bir sınır varsa eşik ondan çıkıyor.
3. **F1'i geçici çapa olarak kullan.** Hiçbir bilgi yoksa F1 makul bir
   başlangıç — ama bunun bir varsayım olduğu yazılmalı.

## Modele değil, karara bak

Bu bölümün ölçümlerinde model **hiç değişmedi**. Aynı lojistik regresyon,
aynı katsayılar, aynı olasılıklar. Değişen yalnızca:

- Ağırlıklar (`class_weight`)
- Kararın verildiği yer (eşik)
- Bakılan sayı (ölçü)

Recall 0.286'dan 0.762'ye çıktı, precision 0.75'ten 0.262'ye indi. Hiçbiri
yeni bir model değildi.

**Sonuç:** dengesiz veride kazanç çoğu zaman daha iyi bir modelden değil,
daha iyi bir karardan geliyor.
