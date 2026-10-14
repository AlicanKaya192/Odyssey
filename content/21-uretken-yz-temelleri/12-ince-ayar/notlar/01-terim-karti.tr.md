| Terim | Anlamı |
|---|---|
| **Ön eğitim** (pre-training) | Çok büyük veriyle genel bir görevde (sıradaki token) ilk eğitim |
| **İnce ayar** (fine-tuning) | Önceden eğitilmiş modeli yeni veriyle eğitmeye devam etmek |
| **Dondurmak** (freeze) | İnce ayarda bir katmanın ağırlıklarını güncellememek |
| **Felaket düzeyinde unutma** | Yeni veriyle ince ayardan sonra eski görevin bozulması |
| **Tekrar** (replay) | İnce ayar verisine eski görevden örnek karıştırmak |
| **Talimatla ince ayar** | (Talimat, iyi cevap) çiftleriyle ince ayar |
| **Tercihle hizalama** | İkili tercihlerden öğrenip modeli tercih edilen cevaplara yöneltmek |
| **Ödül modeli** | Bir cevaba tercih puanı veren model |
| **Bradley–Terry** | a'nın b'ye tercih olasılığı σ(r(a) − r(b)) |
| **En iyi n** (best-of-n) | n cevaptan ödülü en yüksek olanı seçmek |
| **Ödülü kandırma** (reward hacking) | Ödülün ölçtüğü şeyin artıp istenenin artmaması |

**Akılda tut:**

- Bölümde yalnızca yeni veriyle ince ayar eski görevi %6,5'e düşürdü; 50
  eski örnek karıştırınca %94,5–98'de kaldı.
- Ödül modeli gizli ağırlıklara yakın değerleri yalnızca tercihlerden
  öğrendi; ödülle 8 cevaptan seçmek doğruyu %50'den %99'a çıkardı.
- Yanlı etiketçilerden öğrenilen ödül uzun cevapları seçti; doğruluk %78'de
  kaldı.
