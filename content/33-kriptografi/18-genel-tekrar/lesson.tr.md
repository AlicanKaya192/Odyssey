# Genel Tekrar

Bu modül kriptografinin araç kutusunu adım adım kurdu: klasik şifrelerin
neden kırıldığından başlayıp özet, HMAC, simetrik ve doğrulanmış
şifreleme, anahtar türetme, açık anahtarlı kriptografi, imza, sertifika ve
TLS'e kadar. Bu bölüm hepsini bir arada görüyor; sonunda 40 karışık soru
ve birden çok bölümü birleştiren beş alıştırma var.

## Modülün haritası

| Konu | Ana fikir |
|---|---|
| **Kriptografi nedir** | Kodlama, özet ve şifreleme farklı şeylerdir; Kerckhoffs: güvenlik anahtarda, algoritma açık. |
| **Klasik şifreler** | Sezar, yerine koyma, Vigenère; iki temel hareket: yer değiştirme ve yer karıştırma. |
| **Klasik şifreleri kırmak** | Kaba kuvvet ve harf sıklığı; modern şifre kalıp sızdırmamalı. |
| **XOR ve tek kullanımlık şifre** | Kusursuz gizlilik dört koşulla; anahtar tekrar edilirse çöker; gizlilik bütünlük değildir. |
| **Özet fonksiyonları** | Belirleyici, sabit uzunlukta, çığ etkili; MD5 ve SHA-1 bütünlük için bırakıldı. |
| **HMAC** | Anahtarlı etiket; `compare_digest`; önce doğrula, sonra kullan. |
| **Simetrik şifreleme** | Akış ve blok şifreleri, nonce asla tekrarlanmaz, PKCS#7 dolgu, AES. |
| **Blok şifre kipleri** | ECB sızdırır; CBC rastgele IV ister; CTR akış şifresine çevirir. |
| **Doğrulanmış şifreleme** | Önce şifrele, sonra MAC; AAD; gerçekte AES-GCM, ChaCha20-Poly1305. |
| **Anahtar türetme** | Paroladan yavaş ve tuzlu KDF; güçlü sırdan HKDF ile ayrı anahtarlar. |
| **Modüler aritmetik** | `pow(a, e, n)`, ters, genişletilmiş Öklid, Fermat; tek yönlü işlemler. |
| **RSA** | `n = p * q`, `d = e⁻¹ mod phi`; dolgusuz RSA belirleyici: OAEP, karma şifreleme. |
| **Diffie-Hellman ve eğriler** | Anahtar göndermeden ortak sır; kimlik doğrulamaz; ileri gizlilik; ECDH. |
| **Dijital imza** | Özel anahtar imzalar, açık anahtar doğrular; inkâr edilemezlik; Ed25519. |
| **Sertifikalar ve PKI** | Açık anahtarı ada bağlar; güven zinciri, tarih, ad, iptal, şeffaflık. |
| **TLS** | Anahtar payı, HKDF, CertificateVerify, Finished; TLS 1.3. |
| **Sık hatalar** | Kodlama şifreleme değil; `secrets`; koda sır yazılmaz; ayarlar denetlenir. |

## Bir mesajın yolu

Bir uygulama, bir parolayla korunan bir mesajı saklayıp sonra geri
okuyor. Modülün dört bölümü birbirine bağlanıyor:

<figure class="fig">
<div class="flow">
<span class="node">Parola + tuz</span>
<span class="arrow">→</span>
<span class="node acc">PBKDF2: ana anahtar</span>
<span class="arrow">→</span>
<span class="node acc">Ayrı enc ve mac anahtarı</span>
<span class="arrow">→</span>
<span class="node">Şifrele, sonra MAC</span>
<span class="arrow">→</span>
<span class="node ok">Önce doğrula, sonra çöz</span>
</div>
<figcaption>Anahtar Türetme, Simetrik Şifreleme, HMAC ve Doğrulanmış Şifreleme bölümleri tek bir akışta.</figcaption>
</figure>

```python
import hashlib
import hmac

password = b"correct horse battery staple"
salt = bytes.fromhex("a1b2c3d4e5f60718293a4b5c6d7e8f90")
master = hashlib.pbkdf2_hmac("sha256", password, salt, 100_000, dklen=32)
enc_key = hmac.new(master, b"encryption" + bytes([1]), hashlib.sha256).digest()
mac_key = hmac.new(master, b"mac" + bytes([1]), hashlib.sha256).digest()


def keystream(key, nonce, length):
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def seal(nonce, message):
    stream = keystream(enc_key, nonce, len(message))
    cipher = bytes(m ^ s for m, s in zip(message, stream))
    tag = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    return nonce + cipher + tag


def open_box(box):
    nonce, cipher, tag = box[:8], box[8:-32], box[-32:]
    expected = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        return None
    stream = keystream(enc_key, nonce, len(cipher))
    return bytes(c ^ s for c, s in zip(cipher, stream))


box = seal(b"nonce-01", b"meet at noon")
print(len(box))
print(open_box(box))
broken = box[:9] + bytes([box[9] ^ 1]) + box[10:]
print(open_box(broken))
print(enc_key != mac_key)
```

```text
52
b'meet at noon'
None
True
```

Paket 8 baytlık nonce, 12 baytlık şifreli metin ve 32 baytlık etiketten
oluştu. Tek bir bit değişince paket hiç çözülmeden reddedildi. Şifreleme
ve MAC anahtarı aynı ana anahtardan ama farklı etiketlerle türedi (HKDF'nin
tek bloklu genişletmesi). Gerçek bir programda bu akışın tamamı tek bir
AEAD çağrısıdır; parçaları burada yalnızca görmek için açtık.

## Sık karışan çiftler

| İkisi | Fark |
|---|---|
| Kodlama / şifreleme | Kodlamanın anahtarı yoktur; herkes geri çevirir |
| Özet / şifreleme | Özet geri döndürülemez; şifre anahtarla çözülür |
| HMAC / imza | HMAC'te tek paylaşılan anahtar; imzada özel imzalar, açık doğrular |
| Nonce / tuz | Nonce şifrelemede mesaj başına benzersiz; tuz KDF'de kayıt başına |
| IV (CBC) / nonce (CTR, GCM) | IV tahmin edilemez olmalı; nonce yalnızca benzersiz |
| PBKDF2 / HKDF | PBKDF2 zayıf girdiyi (parola) yavaşlatır; HKDF güçlü sırdan hızlı türetir |
| RSA şifreleme / RSA imza | Şifrelemede açık anahtar kilitler; imzada özel anahtar imzalar |
| Diffie-Hellman / RSA anahtar taşıma | DH'de anahtar hiç gönderilmez, ileri gizlilik var |
| Sertifika / özel anahtar | Sertifika açık; özel anahtar gizli |

## Özet

- Güvenlik algoritmanın gizliliğinden değil **anahtardan** gelir; anahtar
  yeterince uzun ve gerçekten rastgele olmalı.
- **Gizlilik** (şifreleme) ile **bütünlük** (HMAC, imza) ayrı işlerdir;
  ikisi birlikte AEAD.
- Paroladan anahtar **yavaş ve tuzlu** KDF ile; güçlü sırdan ayrı
  anahtarlar **HKDF** ile.
- Açık anahtarlı kriptografi **tek yönlü** matematik işlemlerine dayanır;
  açık anahtarın sahibini **sertifika** söyler.
- TLS bunların hepsini birleştirir; doğru kullanımın kuralları tek bir
  katalogda (Sık Kriptografi Hataları).
