Bir promptu göndermeden önce şu soruları sor:

| Soru | Eksikse ne olur? |
|---|---|
| Model kim gibi davranacak? | Ton ve ayrıntı düzeyini model seçer |
| Görev tek cümleyle açık mı? | Model başka bir iş yapabilir (özet yerine yorum gibi) |
| Gereken bilgi prompt'ta mı? | Model bilmediğini tahminle doldurur |
| Cevabın biçimi yazılı mı? | Program cevabı ayrıştıramaz |
| Girdi talimattan ayrı mı? | Girdideki bir cümle talimat gibi okunabilir |
| Cevap için ne kadar yer gerekiyor? | `max_tokens` küçükse cevap kesilir, büyükse pencerede yer kaplar |

**Program tarafında:**

1. Mesaj listesini bir fonksiyonla kur; sabit parçaları tek yerde tut.
2. Gönderilen isteği kaydet (rol, içerik, `max_tokens`, sıcaklık).
3. Cevabı katı ayrıştır; yalnızca zararsız farkları (boşluk, büyük harf,
   sondaki nokta) temizle.
4. İzin verilen değerler dışında kalan cevabı tahminle düzeltme;
   ayır (`needs_review`) ya da hata mesajıyla yeniden sor.
5. Sistem mesajının token sayısını ölç; çağrı sayısıyla çarp.

**Sık hatalar:**

- **Promptu tek uzun metin olarak elle yazmak.** Hangi parçanın ne işe
  yaradığı ve ne kadar yer tuttuğu görünmez olur.
- **Cevabı metnin içinde arayıp ilk eşleşeni almak.** Derste
  `"warranty, maybe payment"` yanıtından `warranty` çıktı; kararsızlık
  kayboldu.
- **Bir ilkenin işe yaradığını varsaymak.** Örnek yanıtlar bir modelin
  davranışını ölçmez; ilkenin etkisini kendi modelinde, kendi
  örneklerinle ölç.
