Eline yeni bir zaman serisi geçtiğinde modele dokunmadan önce bu soruları
sırayla sor. Her birinin kodu ilerideki bölümlerde; burada **neye**
baktığın önemli.

## İlk bakış listesi

1. **Sıklık ne?** Saatlik mi, günlük mü, aylık mı? Karışık mı?
2. **Başlangıç ve bitiş ne?** Kaç gözlem var, kaç yıl ediyor?
3. **Eksik zaman damgası var mı?** Her gün için bir satır olmalıysa 1096 gün
   için 1096 satır var mı?
4. **Tekrarlanan zaman damgası var mı?** Aynı güne iki satır düşmüş mü?
5. **Değer neyi ölçüyor?** Bir **toplam** mı (günün satışı), bir **anlık
   değer** mi (akşam kapanış fiyatı, o anki sıcaklık)? Haftalığa çevirirken
   birini toplarsın, ötekinin ortalamasını ya da son değerini alırsın.
6. **Çiz.** Bütün seriyi, sonra bir ay gibi dar bir aralığı.
7. **Trend var mı?** Yıl yıl ortalamalara bak.
8. **Mevsimsellik var mı, uzunluğu kaç?** Haftanın günü, ay, günün saati.
9. **Kırılma var mı?** Serinin seviyesi bir noktada kalıcı olarak değişmiş mi?
10. **Saat dilimi ne?** Saatlik veride özellikle: UTC mi, yerel saat mi?
11. **Ayırma planı ne?** Hangi tarihe kadar eğitim, hangisinden sonra test?

## Sık yapılan hatalar

| Hata | Neden yanlış |
|---|---|
| Satırları karıştırmak (`sample(frac=1)`, `shuffle=True`) | Sıra verinin kendisi; karışınca bilgi kayboluyor |
| Rastgele ayırma (`train_test_split`) | Gelecek eğitime, geçmiş teste düşüyor; skor gerçek dışı |
| Tarihi metin olarak bırakmak | Tarih işlemleri çalışmıyor; gün önde yazılmışsa sıra bozuluyor |
| Eksik günleri görmemek | "Bir önceki satır" artık "dün" değil |
| Döngüyü mevsimsellik sanmak | Takvime bağlı olmayan tekrarı sabit uzunlukla modellemek |
| Toplam ile anlık değeri aynı toplamak | Fiyatı haftalığa çevirirken toplamak anlamsız bir sayı veriyor |
| Çizmeden modellemek | Kırılmayı, aykırı değeri, eksik aralığı kaçırmak |

## Neye "zaman serisi" denmez

Her tarih sütunu olan tablo zaman serisi değil. Bir müşteri tablosunda
`signup_date` sütunu olması onu zaman serisi yapmıyor: satırlar hâlâ farklı
müşteriler. Soru şu: **satırlar aynı şeyin zaman içindeki ölçümleri mi?**
Evetse zaman serisi.
