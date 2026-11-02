# Parolaları Saklamak

Bir sistem kullanıcının parolasını denetleyebilmek için bir şey saklamak
zorundadır. Neyi ve nasıl sakladığı, bir gün veritabanı sızdığında ne
kadar kötü olacağını belirler. Bu bölümün sorusu şu: **veritabanın
çalınsa bile parolalar ele geçmesin diye ne saklamalısın?**

## Düz metin ve şifreleme: ikisi de yanlış

- **Düz metin** (plaintext): parolayı olduğu gibi saklamak. Veritabanını
  gören her kişi (saldırgan, meraklı bir çalışan, yedeği bulan biri) bütün
  parolaları okur. Kullanıcılar aynı parolayı başka yerde de kullandığı için
  zarar o siteyle de sınırlı kalmaz.
- **Şifreleme** (encryption): parolayı bir anahtarla şifrelemek. Daha iyi
  görünür ama şifreli metin anahtarla geri açılabilir. Anahtar çoğu zaman
  veritabanıyla aynı sunucudadır; ikisi birlikte sızarsa durum düz metinden
  farksızdır.

Parolayı geri açmaya **hiç gerek yok**. Sistem yalnızca "yazılan parola
doğru mu?" sorusuna cevap vermeli. Bunun için tek yönlü bir işlem
kullanılır: **özet** (hash).

## Düz özet neden yetmez?

Özet fonksiyonu bir metinden sabit uzunlukta bir değer üretir ve bu
değerden metne geri dönülemez. Parolanın özeti saklanır; girişte yazılan
parolanın özeti alınıp karşılaştırılır. Ama düz özetin iki sorunu var:

```python
import hashlib

users = [("ada", "sunshine1"), ("alan", "sunshine1"), ("grace", "Sunshine1")]
for user, password in users:
    digest = hashlib.sha256(password.encode()).hexdigest()
    print(f"{user:<6} {digest[:20]}")
```

```text
ada    284fff3bd254b48cca05
alan   284fff3bd254b48cca05
grace  4fe3c8595d0054272ecf
```

1. **Aynı parola, aynı özet.** Ada ile Alan'ın özetleri birebir aynı.
   Veritabanını gören biri, aynı parolayı kullananları hemen gruplar ve
   birini bulunca ötekini de bulmuş olur. Daha kötüsü: yaygın parolaların
   özetleri önceden hesaplanıp tablolara konmuştur (**önceden hesaplanmış
   tablo**, precomputed table; bunun yer kazandıran bir türüne **gökkuşağı
   tablosu**, rainbow table, denir). Tablo, özeti görünce parolayı bir
   bakışta söyler.
2. **Hız.** SHA-256 hızlı olsun diye tasarlanmıştır; büyük dosyaların
   özeti de çabuk alınsın. Parola için bu bir kusur: saldırgan çevrimdışı
   olarak saniyede milyarlarca parola dener (Parolalar bölümündeki
   "çevrimdışı" hız).

## Tuz: her kullanıcıya ayrı

Birinci sorunun çözümü **tuzdur** (salt): her kullanıcı için rastgele
üretilen ve parolayla birlikte özete giren bir değer. Tuz gizli değildir,
özetin yanında saklanır. İşi, aynı parolanın her kullanıcıda farklı bir
özet vermesini sağlamaktır:

```python
import secrets

salts = {}
for user in ["ada", "alan"]:
    salts[user] = secrets.token_bytes(16)
    print(user, len(salts[user]), "salt bytes")
ada = hashlib.sha256(salts["ada"] + b"sunshine1").digest()
alan = hashlib.sha256(salts["alan"] + b"sunshine1").digest()
print("same hash:", ada == alan)
```

```text
ada 16 salt bytes
alan 16 salt bytes
same hash: False
```

Artık iki kullanıcının parolası aynı olsa da özetleri farklı. Önceden
hesaplanmış tablolar da işe yaramaz: saldırganın her tuz için tabloyu
baştan hesaplaması gerekir, bu da tablonun bütün avantajını siler. Her
kullanıcının parolası **ayrı ayrı** denenmek zorundadır.

## Yavaş özet: anahtar germe

İkinci sorunun çözümü özeti bilerek **yavaşlatmaktır**. Bir girişte bir
kez özet almak için kullanıcıyı bir saniyenin küçük bir kesri kadar
bekletmek kimseyi rahatsız etmez; ama milyarlarca deneme yapmak isteyen
saldırgan için aynı yavaşlık her denemede tekrarlanır. Buna **anahtar
germe** (key stretching) denir.

Python'un standart kütüphanesindeki `hashlib.pbkdf2_hmac` bunu yapar:
özeti binlerce kez art arda alır. Kaç kez alınacağı **yineleme sayısıdır**
(iterations). PBKDF2-HMAC-SHA256 için bugünkü öneri 600 000 yinelemedir.

```python
salt = bytes.fromhex("8f2a1c9e5b7d3f60a4c2e8b1d6f09a37")
key = hashlib.pbkdf2_hmac("sha256", b"sunshine1", salt, 600_000)
print(len(key), key.hex()[:32])
```

```text
32 95ac3727b4efa2fe0c28c480179ffa87
```

Bu örnekte tuz sabit yazıldı, çıktı her çalıştırmada aynı olsun diye.
Gerçekte tuz her kullanıcı için `secrets.token_bytes(16)` ile üretilir.

Ne kadar yavaş? Bu bilgisayarda ölçelim, süreleri değil yalnızca
karşılaştırmayı yazdıralım:

```python
import time

start = time.perf_counter()
for _ in range(10_000):
    hashlib.sha256(salt + b"sunshine1").digest()
fast = (time.perf_counter() - start) / 10_000
start = time.perf_counter()
hashlib.pbkdf2_hmac("sha256", b"sunshine1", salt, 600_000)
slow = time.perf_counter() - start
print("at least 10000 times slower:", slow > fast * 10_000)
```

```text
at least 10000 times slower: True
```

Tek bir SHA-256 ölçülemeyecek kadar kısa sürdüğü için on bin tanesinin
ortalaması alındı. Saldırganın saniyede yapabileceği deneme sayısı da en az aynı oranda
düşer: saniyede on milyar deneme, en fazla bir milyona iner. Parolalar bölümündeki
"çevrimdışı" satırı, iyi saklanmış parolalar için bu yüzden geçersizdir.

## Ne saklanır?

Doğrulamak için özetin yanında **algoritmanın adı**, **yineleme sayısı**
ve **tuz** da gerekir. Yaygın bir yol, hepsini tek bir metinde,
`$` işaretiyle ayırarak saklamaktır:

```python
import hmac


def make_record(password, salt, iterations):
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${key.hex()}"


def verify(password, record):
    algorithm, iterations, salt_hex, key_hex = record.split("$")
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, int(iterations))
    return hmac.compare_digest(key.hex(), key_hex)


record = make_record("sunshine1", salt, 1000)
print(record[:46] + "...")
print(verify("sunshine1", record), verify("sunshine2", record))
```

```text
pbkdf2_sha256$1000$8f2a1c9e5b7d3f60a4c2e8b1d6f...
True False
```

Doğrulama, kaydın içindeki tuz ve yineleme sayısıyla aynı hesabı yeniden
yapar ve sonucu karşılaştırır. Karşılaştırma `==` ile değil
`hmac.compare_digest` ile yapılır: `==` ilk farklı karakterde durur ve
geçen süre ipucu verebilir.

Kayıtta yineleme sayısının yazılı olmasının bir faydası daha var: ileride
öneri yükselince eski kayıtlar bozulmaz. Kullanıcı bir sonraki girişinde
doğru parolayı yazdığında parola yeni sayıyla yeniden özetlenip kaydedilir.

## Başka algoritmalar

PBKDF2 standart kütüphanede olduğu için bu derste onu kullanıyoruz. Parola
saklamak için tasarlanmış başka algoritmalar da var: **bcrypt**,
**scrypt** (`hashlib.scrypt`) ve **Argon2**. scrypt ve Argon2 yalnızca
zaman değil **bellek** de harcar; bu, çok sayıda paralel çekirdekli
donanımla yapılan saldırıları da pahalılaştırır. Yeni bir sistemde güncel
öneri genelde Argon2id'dir. Hangisi seçilirse seçilsin kurallar aynı:
tuzlu, yavaş, parametreleri kayıtta.

## Özet

- Parolalar düz metin ya da şifreli değil, **tuzlu ve yavaş özet** olarak
  saklanır.
- Düz özetin sorunları: aynı parola aynı özeti verir (önceden hesaplanmış
  tablolar) ve çok hızlıdır.
- **Tuz** her kullanıcıya ayrı, rastgele ve gizli değildir.
- **Anahtar germe** (PBKDF2, bcrypt, scrypt, Argon2) her denemeyi pahalı
  yapar.
- Kayıtta algoritma, yineleme sayısı, tuz ve özet birlikte durur;
  doğrulama `hmac.compare_digest` ile yapılır.
