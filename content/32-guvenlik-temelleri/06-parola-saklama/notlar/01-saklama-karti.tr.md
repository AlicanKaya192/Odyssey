## Ne saklanır, ne saklanmaz

| Yöntem | Sızınca ne olur? | Karar |
|---|---|---|
| Düz metin | Bütün parolalar okunur | Asla |
| Şifreli | Anahtar da sızarsa hepsi açılır | Parola için değil |
| Düz özet (SHA-256) | Aynı parolalar gruplanır, tablolarla ve hızla bulunur | Hayır |
| Tuzlu özet | Tablolar işe yaramaz ama deneme hâlâ hızlı | Yetmez |
| **Tuzlu ve yavaş özet** | Her parola ayrı ve pahalı denenir | **Evet** |

## Terimler

- **Tuz** (salt): kullanıcı başına rastgele değer, özetin yanında saklanır,
  gizli değildir. `secrets.token_bytes(16)`.
- **Anahtar germe** (key stretching): özeti bilerek yavaşlatmak.
- **Yineleme sayısı** (iterations): PBKDF2'nin özeti kaç kez aldığı;
  PBKDF2-HMAC-SHA256 için bugünkü öneri 600 000.
- **Önceden hesaplanmış tablo / gökkuşağı tablosu** (rainbow table):
  yaygın parolaların özetlerinden parolaya giden hazır tablo; tuz bunu
  boşa çıkarır.
- **Biber** (pepper): bütün kullanıcılar için ortak, veritabanında
  **değil** ayrı bir yerde (ayar dosyası, donanım güvenlik modülü)
  tutulan gizli değer. Yalnızca veritabanı sızarsa ek koruma sağlar.

## Python

```python
import hashlib
import hmac
import secrets

salt = secrets.token_bytes(16)
key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)
record = f"pbkdf2_sha256$600000${salt.hex()}${key.hex()}"
same = hmac.compare_digest(key, other_key)
```

## Doğrulama adımları

1. Kaydı `$` işaretinden böl: algoritma, yineleme, tuz, özet.
2. Algoritma tanınmıyorsa ya da kayıt bozuksa `False` (güvenli
   başarısızlık).
3. Yazılan parolayla aynı tuz ve yinelemeyle yeniden hesapla.
4. `hmac.compare_digest` ile karşılaştır.
5. Doğruysa ve yineleme sayısı eskiyse yeni sayıyla yeniden kaydet.
