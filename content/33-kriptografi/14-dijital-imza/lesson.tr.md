# Dijital İmza

Mesaj Doğrulama: HMAC bölümünde bir etiketin mesajın değişmediğini
gösterdiğini gördük. Ama HMAC'in bir sınırı var: etiketi doğrulamak için
**aynı gizli anahtar** gerekir, yani etiketi doğrulayabilen herkes onu
üretebilir de. **Dijital imza** bu sınırı kaldırır: imzayı yalnızca **özel
anahtarın** sahibi atar, **açık anahtarı** olan herkes doğrular.

## Önce özet, sonra imza

RSA bölümündeki anahtar çiftini ters yönde kullanırız: şifrelemede açık
anahtar kilitliyor, özel anahtar açıyordu; imzada **özel anahtar imzalar,
açık anahtar doğrular**. Mesajın kendisi değil **özeti** imzalanır: özet
kısa ve sabit uzunluktadır, mesaj ne kadar uzun olursa olsun.

```python
import hashlib

p, q = 104723, 104729
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))


def digest(message):
    h = hashlib.sha256(message).digest()
    return int.from_bytes(h, "big") % n


def sign(message):
    return pow(digest(message), d, n)


def verify(message, signature):
    return pow(signature, e, n) == digest(message)


signature = sign(b"release 2.4.1")
print(verify(b"release 2.4.1", signature))
```

```text
True
```

İmza yalnızca `d` ile, doğrulama yalnızca `e` ve `n` ile yapıldı. `e` ve
`n` açık anahtardır: herkes elinde tutabilir ve doğrulayabilir.

## Değiştirilen mesaj, başka anahtar

```python
print(verify(b"release 2.4.2", signature))
print(verify(b"release 2.4.1", signature + 1))
print(verify(b"x" * 100000, sign(b"x" * 100000)))
```

```text
False
False
True
```

Mesajda tek bir karakter değişince imza tutmadı; imzanın kendisi
değişince de tutmadı. 100 000 baytlık bir mesaj da aynı yolla imzalandı,
çünkü imzalanan şey her zaman 32 baytlık özet. (Oyuncak `n` 34 bit
olduğu için burada özeti `n`'e göre küçültüyoruz; gerçek imzada özet
anahtarın içine sığar ve dolguyla imzalanır.)

İmza başka bir anahtar çiftiyle de doğrulanamaz:

```python
p2, q2 = 104717, 104743
n2 = p2 * q2
other = pow(digest(b"release 2.4.1"), pow(e, -1, (p2 - 1) * (q2 - 1)), n2)
print(verify(b"release 2.4.1", other))
```

```text
False
```

Başka bir özel anahtarla atılmış imza bizim açık anahtarımızla tutmuyor.
İmza hem "mesaj değişmedi" hem "bu özel anahtarın sahibi imzaladı" der.

## HMAC ile imza

| | HMAC | Dijital imza |
|---|---|---|
| Anahtar | Tek, paylaşılan gizli anahtar | Özel anahtar imzalar, açık anahtar doğrular |
| Kim doğrular? | Yalnızca anahtarı bilenler | Açık anahtarı olan herkes |
| Kim üretebilir? | Doğrulayabilen herkes | Yalnızca özel anahtarın sahibi |
| İnkâr edilemezlik | Yok | Var |
| Hız | Çok hızlı | Daha yavaş |
| Tipik yer | Sunucu içi jetonlar, API istekleri | Yazılım güncellemeleri, sertifikalar, e-posta |

**İnkâr edilemezlik** (non-repudiation): HMAC'te iki taraf da etiketi
üretebildiği için "bu mesajı ben göndermedim" denebilir; imzada yalnızca
özel anahtarın sahibi imzalayabildiği için denemez (özel anahtar
çalınmadıysa).

## Gerçek imza algoritmaları

| Algoritma | Dayandığı | Not |
|---|---|---|
| RSA-PSS | RSA | Ders kitabı RSA imzası yerine rastgele dolgulu PSS |
| ECDSA | Eliptik eğri | Her imzada **benzersiz, gizli** bir rastgele sayı ister |
| Ed25519 | Eliptik eğri (Edwards) | O sayıyı kendisi, mesajdan belirleyici türetir; hata payı az |

ECDSA'nın kuralı katıdır: imza başına kullanılan gizli sayı tekrar ederse
ya da tahmin edilebilirse **özel anahtar ortaya çıkar**. Bu yüzden yeni
sistemlerde çoğunlukla Ed25519 seçiliyor. Hangisi olursa olsun imza
denenmiş bir kütüphaneyle atılır ve doğrulanır.

## İmza nerede kullanılır

- **Yazılım güncellemeleri:** program yeni sürümü indirir, üreticinin açık
  anahtarıyla imzasını doğrular, tutmazsa kurmaz.
- **Kimlik jetonları:** Kimlik Yönetimi ve Tek Oturum bölümündeki jetonda
  kimlik sağlayıcının imzası; önce imza, sonra iddialar.
- **Sertifikalar:** bir açık anahtarın kime ait olduğunu bir otoritenin
  imzası söyler (sonraki bölüm, Sertifikalar ve PKI).

## Özet

- İmzayı **özel anahtar** atar, **açık anahtar** doğrular; herkes
  doğrulayabilir, yalnızca sahibi imzalayabilir.
- Mesajın kendisi değil **özeti** imzalanır.
- Mesaj ya da imza tek bir bitte değişse doğrulama düşer.
- HMAC'ten farkı: **inkâr edilemezlik** ve açık doğrulama.
- Gerçekte RSA-PSS, ECDSA ya da Ed25519; ECDSA'da imza başına sayı asla
  tekrarlanmaz.
