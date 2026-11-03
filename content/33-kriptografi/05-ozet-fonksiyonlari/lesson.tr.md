# Özet (Hash) Fonksiyonları

Kriptografi Nedir? bölümünde özeti kısaca tanıdık: her uzunluktaki veriden
sabit uzunlukta, geri döndürülemez bir parmak izi. Parolaları Saklamak
bölümünde parolaları saklarken, Kimlik Yönetimi ve Tek Oturum bölümünde
jetonu imzalarken kullandık. Bu bölüm özet fonksiyonlarının hangi
özellikleri sağladığını, nerede kullanıldığını ve en çok nerede yanlış
kullanıldığını anlatıyor.

Bir **kriptografik özet fonksiyonu** (cryptographic hash function) bir
baytı ya da gigabaytı alır, sabit uzunlukta bir **özet** (digest, hash)
üretir ve dört özelliği sağlar:

- **Belirlenimci** (deterministic): aynı girdi her zaman aynı özeti verir.
- **Hızlı:** büyük veriyi hızla özetler.
- **Tek yönlü** (one-way, preimage resistance): özetten girdiyi geri
  bulmak pratikte imkânsız.
- **Çakışmaya dayanıklı** (collision resistance): aynı özeti veren iki
  farklı girdi bulmak pratikte imkânsız.

## Belirlenimci ve sabit uzunlukta

```python
import hashlib

for text in ["meet at noon", "meet at noon", "a much longer message than before"]:
    digest = hashlib.sha256(text.encode()).hexdigest()
    print(len(digest), digest[:16])
```

```text
64 50a8d1d0939b05a7
64 50a8d1d0939b05a7
64 3b10a42186bbb87c
```

İlk iki satır birebir aynı: aynı girdi aynı özeti verdi. Üçüncü girdi çok
daha uzun ama özeti yine 64 onaltılık hane (256 bit). Özetin uzunluğu
girdiye bağlı değildir.

## Çığ etkisi

İyi bir özet fonksiyonunda girdinin **tek bir biti** değişince özetin
yaklaşık **yarısı** değişir. Buna **çığ etkisi** (avalanche effect) denir;
Klasik Şifreleri Kırmak bölümünde modern şifreden beklediğimiz yayılmanın
özetteki karşılığıdır. İki mesajın özetleri arasında kaç bitin farklı
olduğunu sayalım:

```python
import hashlib


def bit_diff(a, b):
    x = int.from_bytes(a, "big") ^ int.from_bytes(b, "big")
    return bin(x).count("1")


h1 = hashlib.sha256(b"message 1").digest()
h2 = hashlib.sha256(b"message 2").digest()
print("total bits:", len(h1) * 8)
print("differing bits:", bit_diff(h1, h2))
```

```text
total bits: 256
differing bits: 117
```

Tek bir karakter değişti (`1` → `2`), ama 256 bitin yaklaşık yarısı
değişti. İki özete bakan biri girdilerin "yakın" olduğunu anlayamaz; özet
girdiyle ilgili hiçbir kalıp sızdırmaz.

## Algoritmalar: hangisi, kaç bit?

```python
import hashlib

for name in ["md5", "sha1", "sha256", "sha512", "sha3_256", "blake2b"]:
    size = hashlib.new(name).digest_size * 8
    print(f"{name:<9} {size} bits")
```

```text
md5       128 bits
sha1      160 bits
sha256    256 bits
sha512    512 bits
sha3_256  256 bits
blake2b   512 bits
```

Hepsi standart kütüphanede. Ama hepsi güvenli değil:

| Algoritma | Durum |
|---|---|
| **MD5** | Kırık: çakışma üretmek kolay. Yeni tasarımda kullanma. |
| **SHA-1** | Kırık: 2017'de gerçek bir çakışma gösterildi. Kullanma. |
| **SHA-256 / SHA-512** | Güvenli; en yaygın seçim (SHA-2 ailesi). |
| **SHA-3** | Güvenli; farklı bir iç tasarım (yedek aile). |
| **BLAKE2** | Güvenli ve hızlı. |

"Kırık" demek, çakışmaya dayanıklılığın artık geçerli olmaması demektir:
aynı özeti veren iki farklı girdi üretilebiliyor. MD5 ve SHA-1 hâlâ
parmak izi gibi **güvenlik gerektirmeyen** işlerde görülür, ama imza ya da
bütünlük denetimi gibi güvenlik işlerinde kullanılmaz.

## Ne için kullanılır?

Özetin en yaygın işi **bütünlük denetimi**: bir dosyanın beklenen özeti
bilinirse, dosya değişmiş mi diye özet yeniden hesaplanıp karşılaştırılır.
İndirilen bir dosyanın yanında yayımlanan SHA-256 değeri tam olarak budur.

```python
import hashlib

KNOWN = {
    "report.pdf": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
}


def verify(name, data):
    digest = hashlib.sha256(data).hexdigest()
    return digest == KNOWN.get(name)


print(verify("report.pdf", b""))
print(verify("report.pdf", b"tampered"))
```

```text
True
False
```

İlk satır `True`: boş içeriğin özeti kayıttaki değere uydu (bu değer boş
baytın SHA-256'sıdır). İkinci satırda tek bir bayt bile değişince özet
tutmadı. Aynı fikir ağda dosya doğrulama, kopya tespiti (deduplication) ve
sürüm kontrolünde (Git'in nesne kimlikleri) kullanılır.

## İki yaygın hata

**1. Parolayı düz özetle saklamak.** Özet hızlıdır; bu, bütünlük için iyi
ama parola için kötüdür. Saldırgan saniyede milyarlarca parola deneyebilir.
Parolalar bu yüzden **yavaş, tuzlu** parola özetiyle saklanır (Parolaları
Saklamak bölümü), düz SHA-256 ile değil.

**2. Özeti bütünlük kanıtı sanmak.** Düz bir özet, veriyi **kazara**
bozulmaya karşı korur ama **kasıtlı** değişikliğe karşı korumaz: saldırgan
veriyi değiştirip özeti de yeniden hesaplayabilir. Gönderenin kimliğini de
kanıtlayan bir bütünlük için anahtarlı bir yapı gerekir: HMAC (Mesaj
Doğrulama: HMAC bölümü).

## Çakışma neden kaçınılmazdır ama güvenli algoritmada bulunamaz?

Girdi sayısı sonsuz, özet sayısı sonludur (256 bitlik özette `2²⁵⁶`); bu
yüzden aynı özeti veren girdiler **vardır**. Önemli olan onları
**bulabilmek**tir. Rastgele denemeyle çakışma bulmak için gereken deneme
sayısı, özet uzunluğunun yarısının üssüyle (`2^(n/2)`) orantılıdır; buna
**doğum günü sınırı** (birthday bound) denir. Hesaplayalım:

```python
for bits in [64, 128, 256]:
    tries = 2 ** (bits / 2)
    print(f"{bits:>3} bits: ~2^{bits // 2} = {tries:.2e} tries")
```

```text
 64 bits: ~2^32 = 4.29e+09 tries
128 bits: ~2^64 = 1.84e+19 tries
256 bits: ~2^128 = 3.40e+38 tries
```

64 bitlik bir özet için yaklaşık dört milyar deneme yeter (bu yüzden
güvenlik için kısa özet kullanılmaz); 256 bit için gereken sayı evrenin
atom sayısıyla kıyaslanır. Bu yüzden bugünkü özetler en az 256 bittir ve
"kırık" MD5/SHA-1'in sorunu, matematiksel sınırdan çok daha azıyla çakışma
bulunabilmesidir.

## Özet

- Kriptografik özet **belirlenimci**, **tek yönlü** ve **çakışmaya
  dayanıklı**dır; çıktısı sabit uzunlukludur.
- **Çığ etkisi:** bir bit değişince özetin yaklaşık yarısı değişir.
- **MD5 ve SHA-1 kırık**; bugün SHA-256, SHA-3 ya da BLAKE2 kullanılır.
- Özet **bütünlük denetimi** için; parola için yavaş-tuzlu özet, gönderen
  kanıtı için HMAC gerekir.
- **Doğum günü sınırı:** çakışma `2^(n/2)` denemeyle bulunur; bu yüzden
  özetler en az 256 bittir.
