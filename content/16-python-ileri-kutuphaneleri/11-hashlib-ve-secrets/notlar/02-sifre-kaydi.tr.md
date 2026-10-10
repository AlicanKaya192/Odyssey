Gerçek bir uygulamada tuz, özet ve tekrar sayısı veritabanında **tek bir
metin** olarak saklanır. Biçim, algoritmanın adını ve ayarını da taşır; böylece
ayar yıllar içinde değişse bile eski kayıtlar doğrulanabilir. (Django gibi
çerçeveler benzer bir biçim kullanır.)

```python
import hashlib
import hmac
import secrets

ITERATIONS = 200_000


def make_record(password, iterations=ITERATIONS):
    salt = secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${key.hex()}"


def verify(password, record):
    _, rounds, salt_hex, key_hex = record.split("$")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(rounds))
    return hmac.compare_digest(key.hex(), key_hex)


def needs_upgrade(record):
    return int(record.split("$")[1]) < ITERATIONS


record = make_record("correct horse")
print(record.split("$")[:2], len(record))
print(verify("correct horse", record), verify("correct horse!", record))
old = make_record("correct horse", 100_000)
print(verify("correct horse", old), needs_upgrade(old))
```

```text
['pbkdf2_sha256', '200000'] 118
True False
True True
```

## Kaydın parçaları

`pbkdf2_sha256$200000$<tuz>$<özet>`:

- **Algoritma adı:** ileride `scrypt`'e geçilirse hangi kaydın hangi yolla
  doğrulanacağı buradan anlaşılır.
- **Tekrar sayısı:** bilgisayarlar hızlandıkça sayı artırılır. Eski kayıt
  kendi sayısını taşıdığı için yine doğrulanıyor (`old` → `True`).
- **Tuz ve özet** onaltılık metin: veritabanında düz metin sütununa sığar.

## Ayarı yükseltmek

Kullanıcının şifresini bilmeden özetini yeniden hesaplayamazsın. Ama
kullanıcı **giriş yaptığı anda** şifre elinde: doğrulama başarılıysa ve
`needs_upgrade(record)` doğruysa, `make_record(password)` ile yeni kayıt
yazılır. Böylece kayıtlar giriş yapıldıkça sessizce güçlenir.

## Yapma

- Şifreyi ya da özetini günlük dosyasına (log) yazmak.
- "Şifremi unuttum"da eski şifreyi e-postayla göndermek: geri çözülemiyorsa
  gönderilemez de. Doğrusu `secrets.token_urlsafe` ile tek kullanımlık,
  süreli bir bağlantı.
- Kendi özet algoritmanı icat etmek.
