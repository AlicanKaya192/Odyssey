# TLS El Sıkışması

Tarayıcının adres çubuğundaki `https` bu modülün hemen her bölümünü bir
arada kullanır: anahtar değişimi, anahtar türetme, sertifika, imza, HMAC ve
doğrulanmış şifreleme. Hepsini birleştiren protokolün adı **TLS**
(Transport Layer Security). Bu bölümde TLS 1.3 el sıkışmasını, ağa hiç
çıkmadan, bellekteki küçük bir benzetimle adım adım kuruyoruz.

## TLS ne sağlar

| Özellik | Hangi parça |
|---|---|
| Gizlilik | Anahtar değişimi + doğrulanmış şifreleme (AES-GCM, ChaCha20-Poly1305) |
| Bütünlük | Doğrulanmış şifreleme; el sıkışmada HMAC (Finished) |
| Sunucunun kimliği | Sertifika zinciri + sunucunun imzası (CertificateVerify) |
| İleri gizlilik | Her bağlantıda geçici Diffie-Hellman |

## El sıkışmanın akışı

<figure class="fig">
<div class="flow">
<span class="node">ClientHello</span>
<span class="arrow">→</span>
<span class="node">ServerHello</span>
<span class="arrow">→</span>
<span class="node acc">Sertifika + imza</span>
<span class="arrow">→</span>
<span class="node acc">Finished</span>
<span class="arrow">→</span>
<span class="node ok">Şifreli veri</span>
</div>
<figcaption>TLS 1.3: istemci ilk mesajında anahtar payını gönderir; sunucunun cevabından sonra trafik şifrelidir.</figcaption>
</figure>

1. **ClientHello:** desteklenen sürümler, şifre takımları ve istemcinin
   Diffie-Hellman **anahtar payı** (key share).
2. **ServerHello:** seçilen sürüm ve takım, sunucunun anahtar payı. Bu
   noktada iki taraf ortak sırrı hesaplayabilir; sonraki her şey şifreli.
3. **Certificate + CertificateVerify:** sunucunun sertifika zinciri ve
   şimdiye kadarki mesajların özetine attığı imza.
4. **Finished:** iki taraf da bütün el sıkışmanın özetine bir HMAC
   gönderir; yolda tek bir bayt değiştiyse burada yakalanır.

## Anahtar payı ve döküm özeti

Mesajları sözlük olarak kuruyoruz. İki taraf da gidip gelen her mesajı
sırayla bir özete katar: bu **döküm özeti** (transcript hash), el
sıkışmanın neye benzediğini iki tarafın da aynı biçimde gördüğünü
kanıtlamakta kullanılır.

```python
import hashlib
import hmac
import json

p, g = 4294967291, 5
client_secret, server_secret = 1234567, 7654321
client_hello = {"type": "client_hello", "versions": ["TLSv1.3"],
                "suites": ["TLS_AES_128_GCM_SHA256", "TLS_CHACHA20_POLY1305_SHA256"],
                "key_share": pow(g, client_secret, p)}
server_hello = {"type": "server_hello", "version": "TLSv1.3",
                "suite": "TLS_AES_128_GCM_SHA256",
                "key_share": pow(g, server_secret, p)}


def transcript_hash(messages):
    h = hashlib.sha256()
    for m in messages:
        h.update(json.dumps(m, sort_keys=True).encode())
    return h.digest()


client_shared = pow(server_hello["key_share"], client_secret, p)
server_shared = pow(client_hello["key_share"], server_secret, p)
th = transcript_hash([client_hello, server_hello])
print(client_shared == server_shared)
print(len(th))
```

```text
True
32
```

İki mesaj gidip geldi ve iki taraf aynı ortak sırra ulaştı (Diffie-Hellman
ve Eliptik Eğriler bölümü). Gerçek TLS'te anahtar payı çoğunlukla X25519
eğrisiyle yapılır.

## Anahtarları türetmek

Ortak sır, Anahtar Türetme bölümündeki HKDF'den geçer. Etikete döküm
özeti de eklenir; böylece anahtarlar yalnızca bu el sıkışmaya özgü olur.
İstemciden sunucuya ve sunucudan istemciye giden trafik **ayrı**
anahtarlarla şifrelenir.

```python
def hkdf_extract(salt, secret):
    return hmac.new(salt, secret, hashlib.sha256).digest()


def hkdf_expand(prk, info, length=32):
    out, block, counter = b"", b"", 1
    while len(out) < length:
        block = hmac.new(prk, block + info + bytes([counter]), hashlib.sha256).digest()
        out += block
        counter += 1
    return out[:length]


prk = hkdf_extract(b"toy-tls", client_shared.to_bytes(4, "big"))
client_key = hkdf_expand(prk, b"c hs traffic" + th)
server_key = hkdf_expand(prk, b"s hs traffic" + th)
print(client_key != server_key)
print(len(client_key), len(server_key))
```

```text
True
32 32
```

## Sunucunun kimliği

Anahtar değişimi tek başına sunucunun kim olduğunu söylemez. Sunucu,
Sertifikalar ve PKI bölümündeki gibi doğrulanan sertifikasını gönderir ve
**o sertifikadaki anahtarla döküm özetini imzalar**. İstemci imzayı
sertifikadaki açık anahtarla doğrular: anahtar payını gönderenin, o
sertifikanın özel anahtarına sahip olduğunu böyle anlar.

```python
n, e = 104717 * 104743, 65537
d = pow(e, -1, (104717 - 1) * (104743 - 1))
signed = int.from_bytes(th, "big") % n
cert_verify = pow(signed, d, n)
print(pow(cert_verify, e, n) == signed)
```

```text
True
```

## Finished: değiştirilen el sıkışma yakalanır

Arada biri ClientHello'daki şifre takımı listesini zayıf bir takımla
değiştirmeye çalışırsa (**sürüm ya da takım düşürme**, downgrade) ne olur?
Sunucu değiştirilmiş mesajı görür ve kendi döküm özetini ondan hesaplar.
Finished'daki HMAC iki tarafın özetinin aynı olmasını şart koşar:

```python
finished_key = hkdf_expand(prk, b"finished")
client_finished = hmac.new(finished_key, th, hashlib.sha256).digest()

changed = dict(client_hello, suites=["TLS_WEAK_SUITE"])
server_view = transcript_hash([changed, server_hello])
server_expects = hmac.new(finished_key, server_view, hashlib.sha256).digest()
same = hmac.new(finished_key, th, hashlib.sha256).digest()
print(hmac.compare_digest(client_finished, same))
print(hmac.compare_digest(client_finished, server_expects))
```

```text
True
False
```

Değişmemiş el sıkışmada Finished tuttu; değiştirilmiş olanda tutmadı ve
bağlantı kurulmaz. (Benzetimde iki taraf aynı `finished_key`'i kullanıyor;
gerçek TLS'te her yönün Finished anahtarı ayrı türetilir.)

## Sürümler ve şifre takımları

- **TLS 1.3** yalnızca beş şifre takımı tanımlar; üçü yaygın:
  `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`,
  `TLS_CHACHA20_POLY1305_SHA256`. Hepsi doğrulanmış şifreleme.
- **TLS 1.2** hâlâ kullanılır ama yalnızca güçlü (AEAD ve geçici
  anahtarlı) takımlarla.
- **SSL 3.0, TLS 1.0 ve 1.1** artık kullanılmaz; sunucu ve istemcide
  kapatılır.
- **HSTS** başlığı tarayıcıya "bu siteye yalnızca `https` ile bağlan" der;
  ilk bağlantıdan sonra şifresiz bağlantıya düşülmez.

## Özet

- TLS; anahtar değişimini, KDF'yi, sertifikayı, imzayı, HMAC'i ve
  doğrulanmış şifrelemeyi tek protokolde birleştirir.
- **ClientHello / ServerHello** anahtar paylarını taşır; ortak sır HKDF ile
  **yön başına ayrı** anahtarlara çevrilir.
- Sunucu, sertifikasındaki anahtarla **döküm özetini imzalar**.
- **Finished** HMAC'i, yolda değiştirilmiş bir el sıkışmayı yakalar.
- Yalnızca TLS 1.3 ve güçlü takımlarla TLS 1.2; eski sürümler kapatılır.
