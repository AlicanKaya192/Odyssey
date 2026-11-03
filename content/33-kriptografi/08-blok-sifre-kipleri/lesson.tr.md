# Blok Şifre Kipleri ve IV

Simetrik Şifreleme bölümünde blok şifresinin mesajı 16 baytlık bloklara
böldüğünü ve son bloğu dolguyla tamamladığını gördük. Ama bir soru açık
kaldı: blok şifresi **tek bir bloğu** şifreler; uzun bir mesajın blokları
birbirine nasıl bağlanır? Bu bağlama yöntemine **kip** (mode of operation)
denir ve yanlış kip seçmek, güçlü bir şifreyi bile işe yaramaz hâle
getirir.

## Oyuncak blok şifresi

AES standart kütüphanede yok. Kipleri görebilmek için 16 baytlık bloklarla
çalışan küçük bir **oyuncak** blok şifresi kuruyoruz. Yapısı, gerçek blok
şifrelerinin de kullandığı **Feistel ağı**: blok iki yarıya ayrılır, her
turda bir yarı, öteki yarının anahtarlı özetiyle XOR'lanır ve yarılar yer
değiştirir. Turlar tersten uygulanınca blok geri gelir.

```python
import hashlib


def round_fn(key, i, half):
    return hashlib.sha256(key + bytes([i]) + half).digest()[:8]


def encrypt_block(key, block):
    left, right = block[:8], block[8:]
    for i in range(4):
        mixed = bytes(a ^ b for a, b in zip(left, round_fn(key, i, right)))
        left, right = right, mixed
    return left + right


def decrypt_block(key, block):
    left, right = block[:8], block[8:]
    for i in reversed(range(4)):
        mixed = bytes(a ^ b for a, b in zip(right, round_fn(key, i, left)))
        left, right = mixed, left
    return left + right


key = b"toy-block-key-16"
cipher = encrypt_block(key, b"exactly16bytes!!")
print(cipher.hex()[:16])
print(decrypt_block(key, cipher))
```

```text
6fcb9dd4b0ccbb92
b'exactly16bytes!!'
```

Bu oyuncak yalnızca kipleri göstermek için; gerçek bir sistemde AES
kullanılır.

## ECB: her blok tek başına

En basit kip **ECB** (Electronic Codebook): her blok ayrı ayrı, aynı
anahtarla şifrelenir. Sorunu şu: **aynı düz metin bloğu her zaman aynı
şifreli bloğa** dönüşür.

```python
def ecb_encrypt(key, data):
    out = b""
    for i in range(0, len(data), 16):
        out += encrypt_block(key, data[i:i + 16])
    return out


message = b"YELLOW SUBMARINE" * 2 + b"another block 16"
cipher = ecb_encrypt(key, message)
blocks = [cipher[i:i + 16].hex()[:8] for i in range(0, len(cipher), 16)]
print(blocks)
print(blocks[0] == blocks[1])
```

```text
['48fd288d', '48fd288d', '88cf223f']
True
```

İlk iki şifreli blok birebir aynı: anahtarı bilmeyen biri bile "mesajın ilk
iki bloğu aynı" bilgisini okur. Klasik Şifreleri Kırmak bölümündeki
yerine koyma şifresinin sorununun blok düzeyindeki hâli bu: tekrar eden
düz metin, şifreli metinde tekrar olarak görünür. Bir resmi ECB ile
şifrelemek, resmin ana hatlarını görünür bırakır. **ECB kullanılmaz.**

## CBC: blokları zincirlemek

**CBC** (Cipher Block Chaining) her düz metin bloğunu şifrelemeden önce
**bir önceki şifreli blokla** XOR'lar. İlk blok için önceki blok yoktur;
onun yerine rastgele bir **başlangıç vektörü** (initialization vector,
**IV**) kullanılır.

```python
def cbc_encrypt(key, iv, data):
    prev, out = iv, b""
    for i in range(0, len(data), 16):
        block = bytes(a ^ b for a, b in zip(data[i:i + 16], prev))
        prev = encrypt_block(key, block)
        out += prev
    return out


iv1 = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
iv2 = bytes.fromhex("f0e0d0c0b0a090807060504030201000")
c1 = cbc_encrypt(key, iv1, message)
c2 = cbc_encrypt(key, iv2, message)
print(c1[:16] == c1[16:32])
print(c1 == c2)
```

```text
False
False
```

Artık aynı iki düz metin bloğu farklı şifreli bloklara dönüştü (zincir
her bloğu bir öncekine bağladı) ve aynı mesaj farklı IV ile bambaşka bir
şifreli metin verdi. IV'nin **gizli olması gerekmez**, şifreli metnin
başına eklenip gönderilir; ama CBC'de **tahmin edilemez** (rastgele)
olmalıdır. CBC dolgu ister ve tek başına bütünlük sağlamaz.

## CTR: blok şifresinden akış şifresi

**CTR** (Counter) kipi blok şifresini bir akış şifresine çevirir: düz
metni değil, **nonce + sayaç** bloğunu şifreler ve çıkanı anahtar dizisi
olarak mesajla XOR'lar. Simetrik Şifreleme bölümündeki oyuncak akış
şifresinin, özet yerine blok şifresiyle yapılmış hâli.

```python
def ctr_crypt(key, nonce, data):
    out = b""
    for n, i in enumerate(range(0, len(data), 16)):
        stream = encrypt_block(key, nonce + n.to_bytes(8, "big"))
        out += bytes(a ^ b for a, b in zip(data[i:i + 16], stream))
    return out


nonce = bytes(8)
secret = ctr_crypt(key, nonce, b"no padding needed here")
print(len(secret))
print(ctr_crypt(key, nonce, secret))
```

```text
22
b'no padding needed here'
```

22 baytlık mesaj 22 baytlık şifreli metin verdi: **dolgu gerekmedi**.
Şifreleme ve çözme aynı işlem ve şifre çözmek için `decrypt_block` hiç
kullanılmadı. Ama akış şifrelerinin kuralı burada da geçerli: **aynı
anahtarla nonce asla tekrarlanmaz** (XOR ve Tek Kullanımlık Şifre bölümü).

## Kiplerin karşılaştırması

| Kip | Aynı blok → aynı çıktı? | IV / nonce | Dolgu | Bütünlük |
|---|---|---|---|---|
| ECB | **Evet** (sızdırır) | Yok | Gerekir | Yok |
| CBC | Hayır | Rastgele IV | Gerekir | Yok |
| CTR | Hayır | Benzersiz nonce | Gerekmez | Yok |
| GCM | Hayır | Benzersiz nonce | Gerekmez | **Var** |

Son sütuna dikkat: ECB, CBC ve CTR'nin hiçbiri tek başına mesajın
değiştirilmesini engellemez. Bu yüzden bugünkü öneri, şifrelemeyle
doğrulamayı birlikte yapan **GCM** gibi bir kiptir. Bir sonraki bölüm,
Doğrulanmış Şifreleme, bunu anlatıyor.

## Özet

- **Kip**, blok şifresinin uzun bir mesajın bloklarını nasıl bağladığıdır.
- **ECB** aynı bloğu aynı çıktıya çevirir ve düz metnin kalıbını sızdırır;
  kullanılmaz.
- **CBC** her bloğu öncekiyle zincirler; rastgele, tahmin edilemez **IV**
  ister, dolgu ister.
- **CTR** blok şifresini akış şifresine çevirir; dolgu istemez, nonce asla
  tekrarlanmaz.
- Hiçbiri tek başına bütünlük sağlamaz; bugün **doğrulanmış kip** (GCM)
  kullanılır.
