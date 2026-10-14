| Terim | Anlamı |
|---|---|
| **Yapılı çıktı** (structured output) | Cevabın JSON gibi alanları belli bir biçimde istenmesi |
| **Şema** (schema) | Hangi alanların, hangi türde ve hangi değerlerle geleceğinin tanımı |
| **Ayrıştırma** (parsing) | Metni JSON'a çevirmek; zararsız ekleri (kod bloğu, öndeki cümle) temizleyerek |
| **Doğrulama** (validation) | Ayrıştırılan veriyi şemaya göre denetlemek: alan, tür, izin verilen değer, kalıp |
| **Onarım döngüsü** | Geçersiz cevabı hata mesajıyla modele geri gönderip yeniden sormak |
| **Deneme sınırı** | Onarım döngüsünün en fazla kaç kez döneceği |

**Akılda tut:**

- Derste altı örnek yanıttan dördü ayrıştırıldı, yalnızca üçü şemaya
  uydu.
- Tek tırnaklı nesne JSON değil; kesilmiş JSON'un sebebi `max_tokens`
  (`finish_reason` `length`).
- Şemayı zorlayan bir API ayarı yalnızca biçimi garanti eder; değerin
  doğru seçildiğini program denetler.
- Onarımda ikinci çağrının giren token'ı 16'dan 114'e çıktı; hata
  mesajları okunur cümleler olmalı.
