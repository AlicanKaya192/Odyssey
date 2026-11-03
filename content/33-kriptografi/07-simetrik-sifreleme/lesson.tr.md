# Simetrik Şifreleme

Kriptografi Nedir? bölümünde iki aileyi tanıttık: **simetrik** (şifreleyen
ve çözen aynı anahtarı kullanır) ve asimetrik. XOR ve Tek Kullanımlık Şifre
bölümünde simetrik şifrelemenin en saf hâlini gördük: mesajı rastgele bir
anahtarla XOR'lamak. Tek sorunu, anahtarın mesaj kadar uzun olması ve bir
kez kullanılmasıydı. Bu bölüm o fikri pratik hâle getiren modern simetrik
şifrelemeyi anlatıyor: kısa bir anahtardan uzun bir anahtar dizisi üretmek.

## İki tür: akış ve blok

- **Akış şifresi** (stream cipher): anahtardan mesaj kadar uzun, rastgele
  görünen bir **anahtar dizisi** (keystream) üretir ve mesajla XOR'lar.
  Tek kullanımlık şifrenin pratik hâli.
- **Blok şifresi** (block cipher): mesajı sabit boyutlu bloklara böler ve
  her bloğu anahtarla karıştırır. En yaygın örnek **AES**.

## Oyuncak akış şifresi

Tek kullanımlık şifrede anahtar mesaj kadar uzundu. Akış şifresinde kısa
bir anahtardan uzun bir dizi **üretiriz**. Burada bunu bir özet
fonksiyonuyla yapan zararsız bir oyuncak kuruyoruz: her blok için
`özet(anahtar + nonce + sayaç)` bir parça anahtar dizisi verir, parçalar
birleşip mesajla XOR'lanır. **Nonce** (number used once) her mesajda
değişen, tekrarlanmayan bir sayıdır.

```python
import hashlib


def keystream(key, nonce, length):
    out = b""
    counter = 0
    while len(out) < length:
        block = hashlib.sha256(key + nonce + counter.to_bytes(4, "big")).digest()
        out += block
        counter += 1
    return out[:length]


def toy_cipher(key, nonce, data):
    stream = keystream(key, nonce, len(data))
    return bytes(d ^ s for d, s in zip(data, stream))


key = b"a 16-byte key!!!"
nonce = b"nonce-1234"
message = b"the treasure is buried under the old oak"
cipher = toy_cipher(key, nonce, message)
print(cipher.hex()[:32])
print(toy_cipher(key, nonce, cipher))
```

```text
52f20fb9990a1ce25094870ed53e0a67
b'the treasure is buried under the old oak'
```

Şifreleme ve çözme aynı işlemdir (XOR), tıpkı tek kullanımlık şifredeki
gibi. Ama anahtar yalnızca 16 bayt; uzun diziyi özet fonksiyonu üretti.
**Bu oyuncak gerçek bir sistemde kullanılmaz** (gerçek akış şifreleri
ChaCha20 gibi özel tasarımlardır); burada yalnızca fikri görüyoruz.

## Nonce neden gerekir?

XOR bölümünde anahtarı iki mesajda tekrar kullanmanın felaket olduğunu
gördük: `c1 ^ c2 = m1 ^ m2`. Akış şifresinde aynı anahtarı birçok mesajda
kullanmak isteriz; nonce bunu güvenli kılar. **Aynı anahtar ama farklı
nonce** her mesaj için farklı bir anahtar dizisi üretir:

```python
m = b"attack at dawn"
c1 = toy_cipher(key, b"nonce-0001", m)
c2 = toy_cipher(key, b"nonce-0002", m)
print(c1.hex()[:20])
print(c2.hex()[:20])
print(c1 == c2)
```

```text
b1e25dad0364bc6e3b29
1d913ab6ef1249fcdeed
False
```

Aynı mesaj, aynı anahtar, ama iki farklı şifreli metin. Böylece saldırgan
"bu iki mesaj aynı" bilgisini bile edinemez (Klasik Şifreleri Kırmak
bölümündeki "aynı mesaj, farklı şifreli metin" beklentisi). **Kural:
nonce asla aynı anahtarla iki kez kullanılmaz;** kullanılırsa akış
şifresi tek kullanımlık şifrenin tekrar-anahtar hatasına düşer. Nonce'un
gizli olması gerekmez, yalnızca **benzersiz** olması gerekir; şifreli
metnin yanında açıkça gönderilir.

## Blok şifresi ve dolgu

Blok şifreleri mesajı sabit boyutlu bloklara böler (AES'te 16 bayt). Mesaj
blok boyutunun katı değilse, son blok **dolgu** (padding) ile tamamlanır.
En yaygın yöntem **PKCS#7**: kaç bayt eksikse, o sayıda ve her biri o
sayıya eşit bayt eklenir. Çözerken son bayt kaç dolgu eklendiğini söyler:

```python
def pad(data, block=16):
    need = block - (len(data) % block)
    return data + bytes([need]) * need


def unpad(data):
    return data[:-data[-1]]


for text in [b"short", b"exactly 16 bytes"]:
    padded = pad(text)
    print(len(text), "->", len(padded), "last:", padded[-1])
    print(unpad(padded) == text)
```

```text
5 -> 16 last: 11
True
16 -> 32 last: 16
True
```

Tam 16 baytlık mesaja bile **yeni bir tam blok** (16 bayt, hepsi 16)
eklendiğine dikkat et: yoksa çözerken gerçek veriyle dolguyu ayırt etmek
mümkün olmazdı. Akış şifreleri dolgu istemez (mesaj kadar anahtar dizisi
üretirler); dolgu blok şifrelerine özgüdür.

## AES: standart simetrik şifre

**AES** (Advanced Encryption Standard) bugünün simetrik şifreleme
standardıdır. 128 bitlik bloklarla çalışır ve üç anahtar boyu vardır:

```python
for bits in [128, 192, 256]:
    print(f"AES-{bits}: key {bits // 8} bytes, block 16 bytes")
```

```text
AES-128: key 16 bytes, block 16 bytes
AES-192: key 24 bytes, block 16 bytes
AES-256: key 32 bytes, block 16 bytes
```

AES'in içi, Klasik Şifreler bölümündeki iki temel hareketi (yer değiştirme
ve yer karıştırma) birçok tur boyunca üst üste uygular; sonuç, şifreli
metnin rastgeleden ayırt edilemez olmasıdır. **AES Python'ın standart
kütüphanesinde yoktur**; gerçek bir uygulamada ayrı bir kütüphanenin
yüksek düzeyli işleviyle (örneğin doğrulanmış AES-GCM) kullanılır. Bu
yüzden derste AES'i çalıştırmıyor, fikrini anlatıyoruz. Blok şifresinin
blokları nasıl zincirlediği (kipler) ve nonce/IV'nin oradaki rolü bir
sonraki bölümün, Blok Şifre Kipleri ve IV'nin konusu.

## Kendi şifreni yazma

Yukarıdaki oyuncak akış şifresi fikri göstermek içindir. Gerçekte **kendi
simetrik şifreni yazmazsın**: denenmiş bir kütüphanenin, hem gizlilik hem
bütünlük sağlayan **doğrulanmış şifreleme** işlevini kullanırsın
(Doğrulanmış Şifreleme bölümü). Çünkü tek başına şifreleme, XOR bölümünde
gördüğümüz gibi, mesajın değiştirilmesini engellemez; yanına bir MAC gerekir.

## Özet

- **Simetrik şifreleme** tek anahtar kullanır; iki tür: **akış** (anahtar
  dizisiyle XOR) ve **blok** (AES gibi, sabit bloklar).
- Akış şifresi, tek kullanımlık şifrenin fikrini kısa bir anahtardan **uzun
  anahtar dizisi** üreterek pratik kılar.
- **Nonce** aynı anahtarın birçok mesajda güvenle kullanılmasını sağlar;
  benzersiz olmalı, gizli olması gerekmez, **asla tekrarlanmaz.**
- **Blok şifreleri dolgu ister** (PKCS#7); akış şifreleri istemez.
- **AES** standarttır (128/192/256 bit anahtar, 128 bit blok) ama standart
  kütüphanede yoktur; gerçekte kütüphaneyle, doğrulanmış kipte kullanılır.
- Kendi simetrik şifreni yazma; doğrulanmış şifreleme kullan.
