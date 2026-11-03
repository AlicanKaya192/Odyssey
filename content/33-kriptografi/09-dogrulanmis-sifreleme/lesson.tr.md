# Doğrulanmış Şifreleme

Simetrik Şifreleme ve Blok Şifre Kipleri bölümleri aynı uyarıyla bitti:
şifreleme mesajı **gizler** ama değiştirilmesini **engellemez**. Mesaj
Doğrulama: HMAC bölümünde de değişikliği yakalayan etiketi gördük. Bu bölüm
ikisini birleştiriyor: hem gizleyen hem doğrulayan **doğrulanmış
şifreleme** (authenticated encryption).

## Tek başına şifreleme neden yetmez

XOR ve Tek Kullanımlık Şifre bölümünde akış şifresinde bir biti çevirmenin
düz metinde aynı biti çevirdiğini görmüştük. Bunu kendi oyuncak
şifremizde bir kez daha görelim; amaç, alıcının **hiçbir şey fark
etmediğini** göstermek.

```python
import hashlib


def keystream(key, nonce, length):
    out, counter = b"", 0
    while len(out) < length:
        out += hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        counter += 1
    return out[:length]


def toy_cipher(key, nonce, data):
    return bytes(d ^ s for d, s in zip(data, keystream(key, nonce, len(data))))


enc_key = b"enc-key-0123456789abcdef"
nonce = b"nonce-001"
cipher = toy_cipher(enc_key, nonce, b"pay 100 to ada")
changed = bytearray(cipher)
changed[4] ^= ord("1") ^ ord("9")
print(toy_cipher(enc_key, nonce, bytes(changed)))
```

```text
b'pay 900 to ada'
```

Şifreli metinde tek bir bayt değişti ve çözülen mesaj `100` yerine `900`
dedi. Çözme işlemi hata vermedi: şifre, mesajın değişip değişmediğini
bilmez. Gizlilik var, **bütünlük** yok (Güvenlik Nedir? CIA Üçlüsü
bölümündeki ikinci harf).

## Önce şifrele, sonra MAC

Çözüm, şifreli metne bir HMAC etiketi eklemek. Doğru sıra **önce şifrele,
sonra MAC** (encrypt-then-MAC): etiket, **nonce ile şifreli metnin**
üzerinden hesaplanır. Şifreleme ve MAC için **iki ayrı anahtar**
kullanılır.

```python
import hmac

mac_key = b"mac-key-fedcba9876543210"


def seal(enc_key, mac_key, nonce, message):
    cipher = toy_cipher(enc_key, nonce, message)
    tag = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    return nonce + cipher + tag


def open_box(enc_key, mac_key, box):
    nonce, cipher, tag = box[:9], box[9:-32], box[-32:]
    expected = hmac.new(mac_key, nonce + cipher, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        return None
    return toy_cipher(enc_key, nonce, cipher)


box = seal(enc_key, mac_key, nonce, b"pay 100 to ada")
print(len(box))
print(open_box(enc_key, mac_key, box))
```

```text
55
b'pay 100 to ada'
```

Paket üç parçadan oluşuyor: 9 baytlık nonce, 14 baytlık şifreli metin ve
32 baytlık etiket. `open_box` önce etiketi doğruluyor, **ancak etiket
tutarsa** çözüyor. HMAC bölümündeki "önce doğrula, sonra kullan" kuralı
burada "önce doğrula, sonra çöz" oldu.

## Değiştirilen paket reddedilir

Aynı bayt değişikliğini şimdi korumalı pakette yapalım:

```python
broken = bytearray(box)
broken[13] ^= ord("1") ^ ord("9")
print(open_box(enc_key, mac_key, bytes(broken)))
```

```text
None
```

Etiket tutmadı ve `open_box` hiç çözmeden `None` döndürdü. Alıcı değişmiş
mesajı görmüyor bile; bu, değiştirilmiş veriyle hiçbir işlem
yapılmamasını sağlar (Güvenlik İlkeleri bölümündeki **güvenli
başarısızlık**).

## Sıralama neden önemli

Şifreleme ile MAC'i birleştirmenin üç yolu var ve yalnızca biri her
durumda güvenli kabul edilir:

| Yol | Etiket neyin üzerinden? | Sonuç |
|---|---|---|
| Önce şifrele, sonra MAC | Şifreli metin | **Önerilen**: çözmeden reddedilir |
| Önce MAC, sonra şifrele | Düz metin (ikisi birlikte şifrelenir) | Doğrulamak için önce çözmek gerekir |
| Şifrele ve MAC | Düz metin (etiket açıkta) | Etiket düz metin hakkında bilgi sızdırabilir |

Önce şifrele, sonra MAC'te alıcı değiştirilmiş veriyi **hiç çözmez**.
Öteki iki yolda doğrulama için çözmek gerekir ve değiştirilmiş veriyi
işleyen kod, hatalarıyla bilgi sızdırabilir.

## Ek doğrulanmış veri (AAD)

Bazen bir bilginin **gizlenmesi gerekmez ama değiştirilmemesi gerekir**:
mesajın alıcısı, sürüm numarası, paketin başlığı. Bu bilgiye **ek
doğrulanmış veri** (additional authenticated data, **AAD**) denir: açık
kalır ama etikete girer.

```python
def seal_aad(enc_key, mac_key, nonce, header, message):
    cipher = toy_cipher(enc_key, nonce, message)
    data = len(header).to_bytes(4, "big") + header + nonce + cipher
    tag = hmac.new(mac_key, data, hashlib.sha256).digest()
    return cipher, tag


def check_aad(mac_key, nonce, header, cipher, tag):
    data = len(header).to_bytes(4, "big") + header + nonce + cipher
    expected = hmac.new(mac_key, data, hashlib.sha256).digest()
    return hmac.compare_digest(tag, expected)


cipher, tag = seal_aad(enc_key, mac_key, nonce, b"to:ada", b"pay 100")
print(check_aad(mac_key, nonce, b"to:ada", cipher, tag))
print(check_aad(mac_key, nonce, b"to:bob", cipher, tag))
```

```text
True
False
```

Başlık şifrelenmedi, herkes `to:ada` yazdığını görebilir; ama `to:bob`
yapılınca etiket tutmadı. Başlığın önüne **uzunluğu** yazılıyor: yoksa
başlığın sonu ile nonce'un başı arasındaki sınır belirsiz kalır ve iki
farklı (başlık, veri) çifti aynı baytları verebilir.

## Gerçek sistemlerde: AEAD

Gerçek uygulamalar bu parçaları elle birleştirmez. Şifrelemeyi, etiketi ve
AAD'yi tek işlemde yapan **AEAD** (Authenticated Encryption with
Associated Data) algoritmaları kullanılır:

<figure class="fig">
<div class="versus">
<div>
<h4>AES-GCM</h4>
CTR kipinde AES + etiket. 12 baytlık nonce, 16 baytlık etiket. AES için
donanım desteği olan işlemcilerde çok hızlı.
</div>
<div>
<h4>ChaCha20-Poly1305</h4>
ChaCha20 akış şifresi + Poly1305 etiketi. 32 baytlık anahtar, 12 baytlık
nonce, 16 baytlık etiket. Donanım desteği olmadan da hızlı.
</div>
</div>
<figcaption>İki yaygın AEAD algoritması. İkisi de standart kütüphanede yok; denenmiş bir kütüphaneden kullanılır.</figcaption>
</figure>

İkisinde de iki kural aynı: **nonce aynı anahtarla asla tekrarlanmaz**
(GCM'de tekrar edilen nonce hem gizliliği hem doğrulamayı bozar) ve etiket
tutmazsa çıktı **hiç kullanılmaz**. Kütüphane etiket tutmadığında hata
verir; o hatayı yakalayıp yine de veriyi kullanmaya çalışmak, bütün
korumayı boşa çıkarır.

## Özet

- Şifreleme tek başına **gizlilik** verir; değiştirilmiş şifreli metin
  hatasız çözülür.
- **Önce şifrele, sonra MAC:** etiket nonce + şifreli metnin üzerinden,
  şifreleme ve MAC için ayrı anahtar.
- Alıcı **önce etiketi doğrular**, tutmazsa hiç çözmez.
- **AAD**, gizlenmeyen ama değiştirilmemesi gereken veridir; etikete
  girer.
- Gerçekte **AEAD** kullanılır: AES-GCM ya da ChaCha20-Poly1305; nonce
  tekrarlanmaz.
