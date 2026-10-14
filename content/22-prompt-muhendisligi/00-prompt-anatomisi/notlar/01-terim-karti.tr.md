| Terim | Anlamı |
|---|---|
| **Prompt** (istem) | Modele gönderilen mesajların tamamı: talimat, bağlam, girdi |
| **Sistem mesajı** | Modelin rolünü ve kurallarını veren, her çağrıda yeniden gönderilen mesaj |
| **Kullanıcı mesajı** | Bu çağrıda işlenecek iş ya da kullanıcının sorusu |
| **Rol** | Modelin kim gibi davranacağı ("destek asistanısın") |
| **Görev** | Modelden istenen iş ("bir kategoriye koy") |
| **Bağlam** | İş için gereken bilgi: kategoriler, kurallar, belgeler |
| **Biçim** | Cevabın nasıl görüneceği ("yalnızca kategori adı") |
| **Örnek yanıt** | Bu modülde önceden yazılmış yanıt; bir modelin ölçümü değildir |
| **Ayrıştırma** (parsing) | Cevaptan programın kullanacağı değeri çıkarmak |
| **Doğrulama** (validation) | Çıkan değerin izin verilen değerlerden biri olup olmadığını denetlemek |

**Akılda tut:**

- Eksik bıraktığın parçayı model kendi tahminiyle doldurur.
- Katı ayrıştırıcı derste altı örnek yanıtın üçünü kabul etti, üçünü
  `needs_review` diye ayırdı; gevşek ayrıştırıcı iki kategori arasında
  kalan bir yanıta bile tek kategori verdi.
- Sınıflandırma promptunda kısa mesajların token'larının %73–78'i
  sabit sistem mesajıydı; o kısım her çağrıda yeniden ödenir.
