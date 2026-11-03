## Ne sağlar

| Özellik | Yalnızca şifreleme | Yalnızca MAC | Doğrulanmış şifreleme |
|---|---|---|---|
| Gizlilik | Var | Yok | Var |
| Bütünlük | Yok | Var | Var |
| Kaynağın doğrulanması (anahtarı bilen) | Yok | Var | Var |

## Önce şifrele, sonra MAC

1. Düz metni nonce ile şifrele: `cipher = encrypt(enc_key, nonce, message)`.
2. Etiketi **nonce + şifreli metin** üzerinden hesapla:
   `tag = hmac(mac_key, nonce + cipher)`.
3. Gönder: `nonce + cipher + tag`.

Alıcı:

1. Paketi böl: nonce, şifreli metin, etiket (son 32 bayt).
2. Etiketi yeniden hesapla ve `hmac.compare_digest` ile karşılaştır.
3. Tutmazsa **dur**; tutarsa çöz.

## Anahtarlar

- Şifreleme anahtarı ile MAC anahtarı **ayrıdır**.
- İkisi tek bir ana sırdan türetilebilir (Anahtar Türetme bölümü).

## AAD

- Gizlenmez, ama etikete girer: değişirse paket reddedilir.
- Örnek: alıcı adı, sürüm, kayıt kimliği, paket başlığı.
- Etikete girerken **uzunluğuyla** birlikte yazılır; sınır belirsiz kalmasın.

## AEAD algoritmaları

| | AES-GCM | ChaCha20-Poly1305 |
|---|---|---|
| Anahtar | 16 / 24 / 32 bayt | 32 bayt |
| Nonce | 12 bayt | 12 bayt |
| Etiket | 16 bayt | 16 bayt |
| Güçlü yanı | Donanım desteğiyle çok hızlı | Donanım desteği olmadan da hızlı |
| Nonce tekrarı | Gizlilik ve doğrulama bozulur | Gizlilik ve doğrulama bozulur |
