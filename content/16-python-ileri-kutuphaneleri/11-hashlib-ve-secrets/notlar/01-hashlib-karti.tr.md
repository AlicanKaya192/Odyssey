## hashlib

| Yazım | Ne yapar |
|---|---|
| `hashlib.sha256(b"...").hexdigest()` | 64 karakterlik özet |
| `.digest()` | 32 baytlık özet |
| `h = hashlib.sha256(); h.update(parça)` | parça parça özet |
| `hashlib.file_digest(f, "sha256")` | dosyanın özeti (`"rb"`) |
| `hashlib.pbkdf2_hmac("sha256", şifre, tuz, 200_000)` | şifre özeti |
| `hashlib.scrypt(şifre, salt=tuz, n=2**14, r=8, p=1)` | şifre özeti (bellek de harcar) |
| `hashlib.blake2b(veri, digest_size=8)` | hızlı, boyu seçilebilen özet |

## hmac

| Yazım | Ne yapar |
|---|---|
| `hmac.new(anahtar, mesaj, hashlib.sha256).hexdigest()` | imza |
| `hmac.compare_digest(a, b)` | sabit sürede karşılaştırma |

## secrets

| Yazım | Ne verir |
|---|---|
| `secrets.token_bytes(16)` | 16 rastgele bayt (tuz) |
| `secrets.token_hex(16)` | 32 onaltılık karakter |
| `secrets.token_urlsafe(32)` | adrese uygun 43 karakter |
| `secrets.choice(dizi)` | güvenli seçim |
| `secrets.randbelow(n)` | `0 … n-1` |

## Hatalar

| Hata | Sebep |
|---|---|
| `TypeError: Strings must be encoded before hashing` | metin `encode()` edilmedi |
| Şifre `sha256` ile saklandı | çok hızlı, tuzsuz: yanlış araç |
| Kod `random` ile üretildi | tahmin edilebilir: `secrets` kullan |
| Özetler `==` ile karşılaştırıldı | `hmac.compare_digest` kullan |
