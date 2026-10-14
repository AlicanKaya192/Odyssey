| Terim | Anlamı |
|---|---|
| **Geçici hata** | Aynı isteğin biraz sonra başarılı olabileceği hata: istek sınırı (429), servis hatası (5xx) |
| **Kalıcı hata** | Tekrar göndermekle düzelmeyen hata: pencereye sığmama, bozuk istek, yanlış kimlik bilgisi |
| **Üstel geri çekilme** (exponential backoff) | Her denemede bekleme süresini ikiye katlamak: 1, 2, 4 saniye |
| **Jitter** (rastgele bekleme) | Beklemeye rastgelelik katmak; aynı anda hata alanlar aynı anda geri gelmesin |
| **İstek kimliği** (idempotency key) | Değiştiren isteğe konan kimlik; aynı kimlikli ikinci istek yeniden işlenmez |
| **Kesilen cevap** | `max_tokens`'a çarpan cevap; `finish_reason` `"length"` |
| **Önbellek** (cache) | Aynı isteğin cevabını saklayıp ikinci kez modele göndermemek |
| **Yedek cevap** (fallback) | Denemeler bitince kullanıcıya gösterilen dürüst mesaj |

**Akılda tut:**

- Derste iki geçici hatadan sonra üçüncü deneme cevap aldı (1 ve 2 saniye
  beklendi); pencereye sığmayan istek hiç beklenmeden hata verdi.
- 100 istemci aynı anda yeniden denediğinde jitter olmadan 80'i yeniden
  reddedildi; jitter ile en kalabalık dilimde 16 istek kaldı.
- 12 token'la başlayan JSON isteği iki kez kesildi; üç çağrıda 108 giren
  + 78 çıkan token ödendi, baştan 48 ile 36 + 42.
- Önbellek 100 isteğin 55'ini modele göndermedi.
