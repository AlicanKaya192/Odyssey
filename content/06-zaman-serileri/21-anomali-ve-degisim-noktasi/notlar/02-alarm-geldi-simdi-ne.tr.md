Dedektör yalnızca "burada bir şey var" der. Ne olduğuna sen karar verirsin.

## Beş soru

1. **Veri mi, dünya mı?** Önce ölçümden şüphelen: sensör takıldı mı, kayıt
   eksik mi geldi, saat dilimi mi kaydı, birim mi değişti? Anomalilerin büyük
   kısmı veri hattının kendisinden gelir.
2. **Tek mi, dizi mi?** Tek alarm bir anomali; aynı yönde art arda alarmlar bir
   düzey kayması.
3. **Başka serilerde de var mı?** Bütün mağazalarda aynı gün düşüş varsa neden
   ortaktır (tatil, sistem kesintisi); tek mağazadaysa yereldir.
4. **Bilinen bir olayla örtüşüyor mu?** Kampanya takvimi, bakım defteri, sürüm
   notları, resmi tatiller.
5. **Tekrar edecek mi?** Edecekse model öğrenmeli (Bölüm 18); etmeyecekse
   eğitimden önce onarılır (Bölüm 13).

## Karar tablosu

| Bulgu | Örnek | Yapılacak |
|---|---|---|
| Veri hatası | Takılı sensör, çift kayıt, −999 | Eksik say, doldur; kaynağı düzelt |
| Tek seferlik gerçek olay | Kesinti, tek kampanya | İşaretle, açıkla; eğitimde onar |
| Tekrar eden gerçek olay | Bayram, maaş günü | Değişken olarak modele ekle |
| Düzey kayması | Yeni müşteri, fiyat değişimi | Kaydet; referansı ve modeli yenile |
| Eğim değişimi | Büyüme yavaşladı | Trendi son dönemden öğren |
| Oynaklık değişimi | Makine gevşedi | Nedenini bul; ölçeği yenile |

## Olay defteri tut

Her alarm için bir satır: ne zaman, hangi seri, puan, ne olduğu, ne yapıldığı.

| Sütun | Neden |
|---|---|
| `timestamp`, `series` | Ne, nerede |
| `score`, `direction` | Ne kadar, hangi yönde |
| `label` (gerçek / yanlış / veri hatası) | Eşiği sonradan ölçebilmek için |
| `cause` | Bir dahaki sefere tanımak için |
| `action` | Onarıldı mı, modele eklendi mi |

Bu defter, Kısım 10'daki kesinlik–duyarlılık tablosunun **tek kaynağıdır**.
Etiketsiz bir dedektörün iyi olup olmadığı bilinemez.

## Dedektörün bakımı

- **Referansı yenile.** Düzey ya da oynaklık değişince eski profil ve ölçek
  geçersiz; yenilenmezse sürekli alarm.
- **Anomaliyi beklentiye sokma.** Ortanca kullan ya da işaretlenen günleri
  beklenti hesabından çıkar.
- **Alarm sayısını izle.** Haftalık alarm sayısı kendi başına bir seridir;
  birden artması bir değişim noktasıdır.
- **Sessizliği de izle.** Hiç alarm vermeyen dedektör ya çok iyi ya da
  bozuktur: veri akışı durmuş olabilir. "Son kayıt ne zaman geldi?" ayrı bir
  kontrol.

## Yanlış alarmı azaltmanın yolları

| Yol | Nasıl |
|---|---|
| Daha iyi beklenti | Bağlam ekle: saat, gün, tatil, kampanya |
| Onay iste | Art arda iki gözlem eşiği aşarsa alarm (gecikme pahasına) |
| İki düzey | Puan 3–5: günlük rapora yaz; 5 üstü: hemen haber ver |
| Birleştir | Aynı olaya ait alarmları tek bildirim yap |
| Bilinen olayları bastır | Planlı bakım, duyurulmuş kampanya |

## Sınırlar

- Dedektör, **beklentisinin bilmediği her şeyi** anomali sayar. İlk bayramda
  alarm vermesi hata değil, eksik bilgidir.
- Serinin başında yeterli geçmiş yoktur; ilk haftalar değerlendirilmez.
- Yavaş bir sürüklenme (her gün binde bir) ne eşiği ne CUSUM'u tetikler; uzun
  dönem karşılaştırması gerekir (bu ay ile geçen yılın aynı ayı).
- Çok serili sistemlerde (bin sensör) her seri için %1 yanlış alarm, her gün
  on yanlış alarm demektir: eşikler seri sayısına göre sıkılaştırılır.
