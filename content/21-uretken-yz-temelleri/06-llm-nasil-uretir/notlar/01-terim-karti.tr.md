| Terim | Anlamı |
|---|---|
| **Büyük dil modeli** (LLM) | Çok büyük metin üzerinde eğitilmiş, sıradaki token'ı tahmin eden model |
| **Token** | Modelin işlediği birim: kelime, kelime parçası ya da işaret |
| **Sohbet şablonu** (chat template) | Mesaj listesini rol işaretleriyle tek diziye çeviren biçim |
| **Rol** | Mesajın sahibi: `system` (genel talimat), `user`, `assistant` |
| **Durma işareti** | Modelin cevabın bittiğini gösteren özel token'ı |
| **`max_tokens`** | Üretilecek token sayısının üst sınırı |
| **Bitiş nedeni** (finish reason) | `stop`: cevap tamam; `length`: sınırda kesildi |
| **Sıcaklık** | Örnekleme rastgeleliği; 0 = her adımda en olası token |
| **Halüsinasyon** | Dayanağı olmayan bir soruya akıcı ama yanlış metin üretmek |
| **Durumsuz API** (stateless) | Model önceki çağrıları hatırlamaz; geçmiş her çağrıda gönderilir |

**Akılda tut:**

- Model soruya cevap vermez, metni devam ettirir; şablon cevabın nereden
  başlayacağını söyler.
- `length` gören program cevabın eksik olduğunu bilmeli.
- Sıcaklık 0 cevabı tekrarlanabilir yapar, doğru yapmaz. Oyuncak model
  bilmediği ülkede sıcaklık 0'da tek ve yanlış bir cevap verdi.
