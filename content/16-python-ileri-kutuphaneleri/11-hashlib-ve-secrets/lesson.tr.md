# hashlib ve secrets

Bir dosya indirdin; yolda bozulmadığını nasıl anlarsın? Kullanıcıların
şifrelerini nasıl saklarsın ki veritabanı çalınsa bile şifreler okunmasın?
Şifre sıfırlama bağlantısındaki rastgele kod nasıl üretilir? Üç sorunun da
cevabı standart kütüphanede: **`hashlib`** (özet / hash), **`hmac`** (anahtarlı
imza) ve **`secrets`** (güvenli rastgelelik).

## Özet (hash) nedir?

```python
import hashlib

text = "hello"
digest = hashlib.sha256(text.encode()).hexdigest()
print(digest)
print(hashlib.sha256(b"hello.").hexdigest())
print(len(digest), len(hashlib.sha256(b"hello").digest()))
try:
    hashlib.sha256(text)
except TypeError as error:
    print("TypeError:", error)
```

```text
2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
1589999b0ca6ef8814283026a9f166d51c70a910671c3d44049755f07f2eb910
64 32
TypeError: Strings must be encoded before hashing
```

- Bir **özet fonksiyonu** (hash function) her uzunlukta veriyi sabit
  uzunlukta bir parmak izine çevirir. SHA-256'nın parmak izi 32 bayt;
  `hexdigest()` onu 64 karakterlik onaltılık metin olarak verir, `digest()`
  baytların kendisini.
- **Aynı girdi her zaman aynı özeti verir**; tek bir nokta eklemek özetin
  tamamını değiştirir. Özetten girdiye geri dönülemez (tek yönlü).
- `hashlib` **bayt** ister: metin önce `encode()` ile baytlara çevrilir.

## Dosyanın parmak izi

```python
import hashlib
from pathlib import Path

rows = "".join(f"{i},{i * 3}\n" for i in range(10_000))
path = Path("report.csv")
path.write_bytes(("id,total\n" + rows).encode())
with path.open("rb") as file:
    whole = hashlib.file_digest(file, "sha256").hexdigest()
h = hashlib.sha256()
with path.open("rb") as file:
    while True:
        chunk = file.read(65_536)
        if not chunk:
            break
        h.update(chunk)
print(whole[:16], h.hexdigest() == whole)
print(path.stat().st_size)
```

```text
63eb0f6a51b36fa9 True
105193
```

- **`hashlib.file_digest(dosya, "sha256")`** ikili kipte açılmış dosyayı
  parça parça okuyup özetini çıkarır; dosya ne kadar büyük olursa olsun
  belleğe birden alınmaz.
- Aynı işi elle yapmak: bir özet nesnesi açıp her parçayı **`update`** ile
  vermek. Parçalar halinde vermek, hepsini bir kerede vermekle aynı özeti
  üretir.
- İndirme sayfalarındaki "SHA-256" satırı tam bunun için: indirdiğin
  dosyanın özetini hesaplayıp o satırla karşılaştırırsın; tek bayt bile
  farklıysa özetler tutmaz.

## Şifre saklamak: tuz ve yavaş özet

```python
import hashlib
import hmac
import secrets

print(hashlib.sha256(b"secret123").hexdigest()[:16])
print(hashlib.sha256(b"secret123").hexdigest()[:16])


def hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return salt, key


def check_password(password, salt, key):
    _, candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, key)


salt, key = hash_password("secret123")
print(len(salt), len(key))
right = check_password("secret123", salt, key)
wrong = check_password("Secret123", salt, key)
print(right, wrong)
other_salt, other_key = hash_password("secret123")
print(key == other_key)
```

```text
fcf730b6d95236ec
fcf730b6d95236ec
16 32
True False
False
```

- Şifre **asla düz metin** saklanmaz. Düz SHA-256 de yetmez: aynı şifre her
  zaman aynı özeti veriyor (ilk iki satır), yani çalınan bir tabloda aynı
  şifreyi kullananlar hemen görünür ve sık kullanılan şifrelerin özetleri
  önceden hesaplanmış listelerde aranabilir.
- **Tuz** (salt): her kullanıcıya rastgele 16 bayt. Şifre tuzla birlikte
  özetlenir; aynı şifre farklı tuzla farklı özet verir (son satır `False`).
  Tuz gizli değildir, özetin yanında saklanır.
- **`pbkdf2_hmac`** özeti 200 000 kez tekrarlayarak bilerek **yavaş** hesaplar.
  Giriş yapan kullanıcı için fark edilmez, ama milyonlarca şifre deneyen
  saldırgan için her deneme pahalılaşır. (`hashlib.scrypt` da aynı amaçla,
  bellek de harcayarak çalışır.)
- Doğrulamada aynı tuzla yeniden hesaplanır ve **`hmac.compare_digest`** ile
  karşılaştırılır. `==` ilk farklı baytta durur; geçen süre ölçülerek
  özetin kaç baytının tuttuğu tahmin edilebilir. `compare_digest` her zaman
  aynı sürede karşılaştırır.

## İmza: hmac

```python
import hashlib
import hmac

KEY = b"server-side-secret"


def sign(message):
    return hmac.new(KEY, message.encode(), hashlib.sha256).hexdigest()


cookie = "user=ada;role=user"
tag = sign(cookie)
forged = "user=ada;role=admin"
print(hmac.compare_digest(tag, sign(cookie)))
print(hmac.compare_digest(tag, sign(forged)))
print(len(tag))
```

```text
True
False
64
```

- Bir mesajın **değiştirilmediğini** ve **bizden çıktığını** kanıtlamak için
  düz özet yetmez: mesajı değiştiren kişi yeni özeti de kendisi
  hesaplayabilir.
- **HMAC** özeti gizli bir **anahtarla** birlikte hesaplar. Anahtarı
  bilmeyen, değiştirdiği mesajın (`role=admin`) geçerli imzasını üretemez.
- Çerezler, şifre sıfırlama bağlantıları, sunucular arası mesajlar ve
  webhook'lar böyle imzalanır. Pickle bölümündeki "kendi dosyanın
  değiştirilmediğini doğrulamak" da budur: dosyanın baytları HMAC ile
  imzalanır, yüklemeden önce imza denetlenir.

## secrets: tahmin edilemeyen rastgelelik

```python
import random
import secrets
import string

random.seed(7)
first = [random.randint(0, 9) for _ in range(6)]
random.seed(7)
print(first == [random.randint(0, 9) for _ in range(6)])
token = secrets.token_urlsafe(32)
print(len(token), secrets.token_hex(16).isalnum())
alphabet = string.ascii_letters + string.digits
password = "".join(secrets.choice(alphabet) for _ in range(16))
print(len(password), all(c in alphabet for c in password))
```

```text
True
43 True
16 True
```

- **`random`** benzetim ve oyun için: tohumdan (seed) üretilir, aynı tohum
  aynı diziyi verir (ilk satır `True`). Birkaç çıktıyı gören biri sonrakileri
  tahmin edebilir; **güvenlik için kullanılmaz**.
- **`secrets`** işletim sisteminin güvenli kaynağını kullanır; tohumu yok,
  tekrar üretilemez.
  - `token_hex(16)`: 16 rastgele bayt, 32 onaltılık karakter.
  - `token_urlsafe(32)`: 32 bayt, adreste kullanılabilecek karakterlerle
    (43 karakter).
  - `choice(dizi)`, `randbelow(n)`: güvenli seçim ve sayı.
- Şifre sıfırlama kodu, oturum anahtarı, API anahtarı, tuz: hepsi `secrets`
  ile üretilir.

## Hangi algoritma?

| Algoritma | Kullan | Kullanma |
|---|---|---|
| SHA-256, SHA-512, BLAKE2 | dosya bütünlüğü, parmak izi, HMAC | şifre saklama (çok hızlı) |
| `pbkdf2_hmac`, `scrypt` | şifre saklama | dosya özeti (bilerek yavaş) |
| MD5, SHA-1 | güvenlik gerektirmeyen yinelenen dosya taraması | güvenlik (çakışma üretilebiliyor) |
| `hmac` | imza, mesajın değişmediğini kanıtlama | gizleme (mesajı şifrelemez) |

Özet **şifreleme değildir**: geri çözülemez ve bir şey gizlemez. Veriyi
gizlemek (sonra geri açmak) için şifreleme kütüphanesi gerekir; standart
kütüphanede yok, `cryptography` paketi bu iş için kullanılır.

## Özet

- `hashlib.sha256(baytlar).hexdigest()`; metin önce `encode()`.
- Büyük dosya `file_digest` ya da parça parça `update` ile.
- Şifre: rastgele tuz + `pbkdf2_hmac` (ya da `scrypt`); doğrulama
  `hmac.compare_digest`.
- İmza: `hmac.new(anahtar, mesaj, hashlib.sha256)`.
- Güvenlikle ilgili her rastgele değer `secrets` ile; `random` değil.
