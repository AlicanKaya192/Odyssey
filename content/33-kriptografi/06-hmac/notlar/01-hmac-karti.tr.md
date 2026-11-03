## MAC ne sağlar?

| Soru | Cevap |
|---|---|
| Mesaj değişti mi? | Bütünlük |
| Anahtarı bilen biri mi gönderdi? | Kimlik doğruluğu |
| Üçüncü kişiye kanıt? | **Hayır** (onun için imza) |

## Python kalıpları

- Etiket: `hmac.new(key, message, hashlib.sha256).hexdigest()`.
- Anahtar ve mesaj **bayt** olmalı (`b"..."` ya da `.encode()`).
- Doğrulama: beklenen etiketi yeniden hesapla, `hmac.compare_digest`.
- `hmac.compare_digest(a, b)` sabit süreli: zamanlamayı ele vermez.
- `==` ilk farklı baytta durur; etiket/parola/jeton karşılaştırmada **asla**.

## Kurallar

- `sha256(key + message)` **yazma**: uzatma saldırısına açık. `hmac`
  modülünü kullan.
- Doğrulanmış mesajda **önce etiketi denetle, sonra içeriği kullan.**
- Aynı anahtar şifreleme ve MAC için ayrı tutulur (Doğrulanmış Şifreleme
  bölümü); tek anahtarı iki işe bölmek için ayrı türetilir.

## HMAC ve imza

| | HMAC | Dijital imza |
|---|---|---|
| Anahtar | Ortak (simetrik) | Açık + özel (asimetrik) |
| Hız | Hızlı | Yavaş |
| Kim üretebilir? | Anahtarı bilen herkes | Yalnızca özel anahtar sahibi |
| İnkâr edilemezlik | Yok | Var |
