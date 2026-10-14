Bir LLM uygulaması yazarken her çağrı için bir **token bütçesi** düşünmek
işe yarar:

| Parça | Ne kadar? | Nasıl küçülür? |
|---|---|---|
| Sistem mesajı | Her çağrıda aynı | Kısa ve net talimat; gereksiz örnekleri çıkar |
| Geçmiş | Her mesajla büyür | Son N mesaj, önemli bilgileri ayrı tut, eski kısmı özetle |
| Eklenen belgeler | Belgenin boyu | Yalnızca ilgili parçaları gönder (RAG bölümleri) |
| Yeni soru | Genelde küçük | — |
| Cevap (`max_tokens`) | İstenen uzunluk | Gereken kadar; kısa cevap iste |

Toplam pencereye sığmalı: `giren + max_tokens ≤ pencere`.

**Kontrol listesi:**

1. Her çağrıdan önce `count_message_tokens` ile giren token'ı ölç
   (gerçek uygulamada modelin kendi parçalayıcısıyla).
2. Pencereye sığmıyorsa önce geçmişi kırp, sonra belgeleri azalt; sistem
   mesajını ve yeni soruyu atma.
3. Kırptığın geçmişte önemli bir bilgi varsa (ad, tercih, karar) onu sistem
   mesajına taşı.
4. Cevaptaki `length`'i denetle: cevap kesildiyse sınırı artır ya da
   cevabı eksik diye işaretle.
5. Maliyeti çağrı başına kaydet; toplamı uygulamanın ölçeğiyle çarp.

**Sık hatalar:**

- **Pencereyi yalnızca girdiyle hesaplamak.** `max_tokens` da pencereye
  sayılır; derste 29 + 50 > 60 olduğu için istek reddedildi.
- **Geçmişi körlemesine kırpmak.** Derste ad unutuldu ve son soruya
  "bilmiyorum" cevabı geldi.
- **Tek sohbetin maliyetine bakıp ölçeği unutmak.** 0,000690 birimlik
  sohbet 100 000 kez yapılınca 68,95 birim.
- **Token sayısını kelime sayısı sanmak.** Uzun kelimeler ve noktalama ayrı
  token tutar.
