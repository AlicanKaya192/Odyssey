| Teknik | Ne zaman? | Dikkat |
|---|---|---|
| Katı ayrıştırıcı | Cevap bir programa girecekse | Metnin içinde kategori arama; anlaşılmayan cevap `needs_review` |
| Net talimat + ayraç | Her prompt'ta | Kuralı ölçülebilir yaz; veriyi ayraçla ayır ve kaçır |
| Az örnekli prompt | Biçim ya da sınır örnekle daha iyi anlatılıyorsa | Örnekler kategorileri kapsasın; her örnek token |
| Adım adım düşündürmek | Çok adımlı akıl yürütmede | Hesabı kod yapsın; adımlı cevap çok daha uzun |
| Yapılı çıktı | Cevap veri olarak kullanılacaksa | Ayrıştır, şemayla doğrula, bir kez onar |
| Sistem mesajı | Rol, ton, kurallar her çağrıda gerekiyorsa | Ayarlardan kur, sürüm özetini sakla; gizli bilgi yazma |
| Şablon | Aynı prompt farklı verilerle | Eksik değişken hata versin; uzun metni ortadan kes |
| Zincir | Bir iş küçük, denetlenebilir adımlara bölünüyorsa | Düşen adım zinciri durdursun |
| Araç çağırma | Model güncel veriye ya da bir işleme ihtiyaç duyuyorsa | Çağrıyı doğrula; geri alınamaz işte onay; cevabı sonuca dayandır |
| Ajan döngüsü | Adım sayısı baştan belli değilse | Tur ve token sınırı; tekrar eden çağrıyı yakala |
| Bellek | Sohbet uzadığında | Son mesajlar + ayrı tutulan önemli bilgiler; özet bilgi düşürebilir |
| Değerlendirme | Her değişiklikte | Biçim ve doğruluk ayrı; küçük farkta bootstrap aralığı |
| Injection savunması | Dış metin okunduğunda, araç varsa | Katmanlı: dedektör, en az yetki, onay, çıktı denetimi |
| Yeniden deneme | Geçici hatalarda | Üstel bekleme + jitter, deneme ve süre sınırı, yedek cevap |
| Önbellek | Aynı istek tekrar ediyorsa | Anahtar cevabı etkileyen her şeyi içersin; kişisel veriyi paylaşma |
| Sistemli iyileştirme | Prompt'u geliştirirken | Geliştirme kümesinde karar, teste en sonda bir kez bakış |

**Modülün sayıları (hepsi kayıtlı yanıt ya da oyuncak modelle):**

- Sistem mesajı kısa mesajlarda token'ların %73–78'i; bitirme projesinde
  40 mesajda %67.
- Kalıp dedektörü: kesinlik 0,8, duyarlılık 0,57.
- Ezber: geliştirmede 1,00, testte 0,75.
- Asistan: onarımsız 9/10, onarımla 10/10.
