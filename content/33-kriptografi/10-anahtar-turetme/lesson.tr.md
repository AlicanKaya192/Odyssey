# Anahtar Türetme

Önceki bölümlerde anahtarlar hep hazırdı: `b"enc-key-..."` gibi sabit
baytlar. Gerçek bir programda anahtar bir yerden **gelir**: kullanıcının
parolasından ya da iki tarafın paylaştığı tek bir ana sırdan. Anahtar
türetme fonksiyonu (key derivation function, **KDF**) bu kaynağı doğru
uzunlukta, güçlü anahtarlara çevirir.

## Parola neden doğrudan anahtar olmaz

Bir parola, şifreleme anahtarından üç yönden farklıdır:

- **Uzunluğu değişir.** AES-256 tam 32 bayt ister; `"sunflower"` 9 bayt.
- **Rastgele değildir.** İnsanlar tahmin edilebilir parolalar seçer;
  32 baytlık rastgele bir anahtarın taşıdığı belirsizliğe hiç yaklaşmaz.
- **Hızlı özet yetmez.** `sha256(parola)` uzunluk sorununu çözer ama
  saniyede milyonlarca kez hesaplanabilir; parolayı tahminle bulmaya
  çalışan biri için de o kadar hızlıdır.

Parolaları Saklamak bölümünde aynı sorunu parola saklarken görmüştük:
çözüm **tuzlu ve kasıtlı olarak yavaş** bir fonksiyondu. Paroladan anahtar
türetmek de aynı araçlarla yapılır.

## PBKDF2: tuz ve tekrar sayısı

`hashlib.pbkdf2_hmac` parolayı tuzla birlikte HMAC'ten **binlerce kez**
geçirir ve istenen uzunlukta anahtar verir.

```python
import hashlib

password = b"correct horse battery staple"
salt1 = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
salt2 = bytes.fromhex("00112233445566778899aabbccddeeff")

key1 = hashlib.pbkdf2_hmac("sha256", password, salt1, 100_000, dklen=32)
again = hashlib.pbkdf2_hmac("sha256", password, salt1, 100_000, dklen=32)
key2 = hashlib.pbkdf2_hmac("sha256", password, salt2, 100_000, dklen=32)
print(len(key1))
print(key1 == again)
print(key1 == key2)
```

```text
32
True
False
```

Üç şey görülüyor:

- Anahtar tam istenen uzunlukta (`dklen=32`).
- Aynı parola + aynı tuz **her zaman aynı anahtarı** verir; bu yüzden şifre
  çözen taraf anahtarı yeniden türetebilir.
- Tuz değişince anahtar değişir. Tuz **gizli değildir**, şifreli verinin
  yanında saklanır; görevi, aynı parolayı kullanan iki kişinin aynı anahtara
  sahip olmamasıdır.

**Tekrar sayısı** (burada 100 000) fonksiyonu kasıtlı olarak yavaşlatır.
Meşru kullanıcı anahtarı bir kez türetir ve farkı hissetmez; parolayı
tahminle arayan biri ise her tahmin için bu bedeli öder. Güncel öneriler
SHA-256 ile PBKDF2 için yüz binlerce tekrardır (örneğin 600 000); bu
dersteki sayılar örnekleri hızlı tutmak için küçük.

## scrypt: bellek de harcatmak

PBKDF2 yalnızca zaman harcatır ve özel donanımda çok hızlı paralel
çalıştırılabilir. **scrypt** buna bellek şartı ekler: her türetme belirli
bir miktar bellek ister.

```python
import hashlib

password = b"correct horse battery staple"
salt = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
key = hashlib.scrypt(password, salt=salt, n=2**14, r=8, p=1, dklen=32)
print(len(key))
print(128 * 8 * 2**14 // 2**20, "MB")
```

```text
32
16 MB
```

`n` maliyet çarpanı, `r` blok boyu, `p` paralellik. Kullanılan bellek
yaklaşık `128 × r × n` bayt: bu ayarla 16 MB. Bugün parolalar için en çok
önerilen KDF **Argon2id**; standart kütüphanede yok, ayrı bir kütüphaneyle
kullanılır. Fikir aynı: tuz, zaman ve bellek.

## HKDF: tek sırdan birçok anahtar

Doğrulanmış Şifreleme bölümünde şifreleme ve MAC için **iki ayrı anahtar**
gerektiğini gördük. Elde tek bir güçlü ana sır varsa (paroladan türetilmiş
ya da anahtar değişiminden gelmiş) ikisi bundan türetilir. Bunun standart
yolu **HKDF**: önce sırrı tuzla bir **ara anahtara** (PRK) çeker, sonra her
amaç için farklı bir **etiketle** (`info`) genişletir.

```python
import hashlib
import hmac


def hkdf_extract(salt, secret):
    return hmac.new(salt, secret, hashlib.sha256).digest()


def hkdf_expand(prk, info, length):
    out, block, counter = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]


master = bytes.fromhex("9f" * 32)
prk = hkdf_extract(b"app-salt-v1", master)
enc_key = hkdf_expand(prk, b"encryption", 32)
mac_key = hkdf_expand(prk, b"mac", 32)
print(enc_key == mac_key)
print(len(hkdf_expand(prk, b"long", 80)))
```

```text
False
80
```

Aynı ana sırdan iki **bağımsız** anahtar çıktı; `info` etiketi değişince
anahtar da değişiyor. Genişletme, bloklar birleştirilerek istenen uzunluğa
kadar sürüyor (80 bayt için üç blok). HKDF **hızlıdır**: girdisi zaten
güçlü bir sır olmalıdır. Parola gibi zayıf bir girdi için önce PBKDF2,
scrypt ya da Argon2 gelir.

## Hangi KDF ne zaman

| Girdi | Kullanılacak | Neden |
|---|---|---|
| Kullanıcı parolası | Argon2id, scrypt ya da PBKDF2 | Yavaş ve tuzlu olmalı |
| Güçlü ana sır | HKDF | Hızlı; amaç başına ayrı anahtar |
| Rastgele anahtar gerekiyor | `secrets.token_bytes(32)` | Türetmeye gerek yok |

## Özet

- Parola **doğrudan anahtar yapılmaz**: uzunluğu değişir, rastgele değildir.
- Paroladan anahtar **yavaş ve tuzlu** bir KDF ile türetilir: PBKDF2,
  scrypt ya da Argon2id.
- **Tuz** gizli değildir, verinin yanında saklanır; **tekrar sayısı**
  tahmin etmeyi pahalılaştırır.
- **HKDF** tek güçlü sırdan, farklı `info` etiketleriyle birbirinden
  bağımsız anahtarlar türetir.
- Şifreleme ve MAC anahtarı aynı sırdan ama **farklı etiketle** türetilir.
