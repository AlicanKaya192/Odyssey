Yapılı bir cevabı kullanan programın akışı:

| Adım | Ne yapılır? | Düşerse |
|---|---|---|
| 1 | `finish_reason`'a bak | `length`: `max_tokens`'ı artır ya da kısaltılmış şema iste |
| 2 | Metni olduğu gibi `json.loads` ile dene | 3. adıma geç |
| 3 | Kod bloğu işaretlerini at, yeniden dene | 4. adıma geç |
| 4 | İlk `{` ile son `}` arasını dene | Geçersiz JSON: onarım döngüsü |
| 5 | Şemaya göre doğrula | Hata listesiyle onarım döngüsü |
| 6 | Deneme sınırı dolduysa | İnsana ya da `needs_review` yoluna gönder |

**Şema yazarken:**

- Her alanın adını, türünü ve izin verilen değerlerini talimatta açıkça
  yaz; mümkünse bir örnek JSON göster.
- "Bilinmiyorsa `null`" gibi boş değer kuralını söyle; yoksa model bir
  değer uydurabilir.
- Alan sayısını gerektiği kadar tut; her alan hem token hem hata
  olasılığı ekler.

**Hata mesajları:**

- Kısa, okunur ve düzeltmeyi söyleyen cümleler: "urgent must be true or
  false".
- İzin verilen değerleri mesajda say; model neyi seçeceğini görür.
- Kişisel veri ya da iç kural içermesin; mesaj modele gidiyor.

**Sık hatalar:**

- **JSON olmayan cevabı tahminle düzeltmek.** Hangi biçimlerin kabul
  edildiği belirsizleşir.
- **Ayrıştırılan JSON'u doğru sanmak.** Derste geçerli bir JSON'da üç
  şema hatası vardı.
- **Sınırsız onarım.** Her deneme daha çok token gönderir; sınır koy.
