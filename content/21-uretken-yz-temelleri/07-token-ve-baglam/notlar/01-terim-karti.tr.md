| Terim | Anlamı |
|---|---|
| **Token** | Modelin okuduğu ve ürettiği metin parçası |
| **Parçalayıcı** (tokenizer) | Metni token'lara bölen yöntem; her modelin kendisi vardır |
| **Bağlam penceresi** (context window) | Bir çağrıda işlenebilecek en fazla token (giren + çıkan) |
| **Giren token** (input tokens) | Gönderilen bütün mesajların token sayısı, rol işaretleri dahil |
| **Çıkan token** (output tokens) | Modelin ürettiği cevabın token sayısı |
| **`max_tokens`** | Cevap için ayrılan en fazla token; pencerede yer kaplar |
| **Geçmişi kırpmak** | Eski mesajları göndermeyip token'ı azaltmak; bilgi kaybettirir |
| **Kayıtlı yanıt** | Önceden yazılmış örnek yanıt; bir modelin ölçümü değildir |

**Akılda tut:**

- Bu bölümdeki sayaç basitleştirilmiş: noktalama 1, kelime başladığı her
  dört karakter için 1 token. Gerçek sayılar modelden modele değişir.
- Durumsuz API'de geçmiş her çağrıda yeniden gönderilir; toplam token
  mesaj sayısının karesiyle büyür (sekiz mesajda 1088, son çağrının 4,5
  katı).
- Maliyet = giren × giriş fiyatı + çıkan × çıkış fiyatı. Uzun sistem
  mesajı ve gereksiz geçmiş her çağrıda yeniden ödenir.
