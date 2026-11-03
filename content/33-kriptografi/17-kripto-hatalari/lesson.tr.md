# Sık Kriptografi Hataları

Kriptografi açıkları çoğu zaman algoritmanın kırılmasından değil, doğru
algoritmanın **yanlış kullanılmasından** çıkar. Bu bölüm, modül boyunca
tek tek gördüğümüz hataları bir arada topluyor ve onları kodda ya da
ayarda **bulmanın** yollarını gösteriyor. Hepsinin ortak dersi aynı:
kriptografi kendi yazılmaz, denenmiş bir kütüphaneyle ve doğru ayarlarla
kullanılır.

## Kodlama şifreleme değildir

Base64, onaltılık ya da URL kodlaması veriyi **başka bir yazıma** çevirir;
anahtar yoktur, herkes geri çevirebilir.

```python
import base64

token = base64.b64encode(b"user=ada;role=admin")
print(token)
print(base64.b64decode(token))
```

```text
b'dXNlcj1hZGE7cm9sZT1hZG1pbg=='
b'user=ada;role=admin'
```

"Okunmuyor" görünmesi gizli olduğu anlamına gelmez. Gizlilik gerekiyorsa
doğrulanmış şifreleme, değiştirilmemesi gerekiyorsa HMAC ya da imza
kullanılır.

## Gizli değer için doğru rastgelelik

Anahtar, nonce, tuz, oturum jetonu ya da parola sıfırlama kodu gibi
**tahmin edilmemesi gereken** her değer `secrets` modülüyle üretilir.
`random` modülü benzetim ve oyun gibi işler için yapılmıştır; gizli değer
için kullanılmaz.

```python
import secrets

print(len(secrets.token_bytes(32)))
print(len(secrets.token_hex(16)))
print(len(secrets.token_urlsafe(16)) >= 16)
```

```text
32
32
True
```

## Koda gömülü sırlar

Kaynak koddaki bir anahtar, depoya erişen herkesin anahtarıdır ve git
geçmişinden kolay kolay silinmez. Kodda sır **adı** geçebilir ama değeri
ortam değişkeninden ya da sır kasasından gelmelidir. Basit bir tarayıcı
yazıp örnek bir dosyada arayalım:

```python
import re

source = """API_URL = "https://api.example.test"
SECRET_KEY = "s3cr3t-value"
password = os.environ["DB_PASSWORD"]
timeout = 30"""
pattern = re.compile(r'(key|secret|password|token)\w*\s*=\s*["\']', re.IGNORECASE)
for number, line in enumerate(source.splitlines(), 1):
    if pattern.search(line):
        print(number, line.split("=")[0].strip())
```

```text
2 SECRET_KEY
```

Tarayıcı yalnızca **değeri tırnak içinde yazılmış** sırrı yakaladı; ortam
değişkeninden okunan parola sorun değil. Gerçek projelerde bu iş için
hazır sır tarayıcıları, commit öncesi denetimlerde çalıştırılır. Sızan bir
sır bulunursa silmek yetmez: **değiştirilir** (döndürülür), çünkü
geçmişte kalmış olabilir.

## Hata kataloğu

| Hata | Neden yanlış | Doğrusu | Bölüm |
|---|---|---|---|
| Kodlamayı şifreleme sanmak | Anahtarı yok | AEAD | Bu bölüm |
| Gizli değer için `random` | Tahmin edilebilir | `secrets` | Bu bölüm |
| Koda gömülü anahtar | Depoyu gören herkes bilir | Ortam değişkeni, sır kasası | Bu bölüm |
| Parolayı hızlı özetle saklamak | Tahmin denemesi çok hızlı | Tuzlu, yavaş KDF | Anahtar Türetme |
| MD5 / SHA-1 ile bütünlük | Çakışma üretilebilir | SHA-256 ve üstü | Özet (Hash) Fonksiyonları |
| Etiketi `==` ile karşılaştırmak | Süre bilgi sızdırabilir | `hmac.compare_digest` | Mesaj Doğrulama: HMAC |
| ECB kipi | Kalıp sızar | GCM | Blok Şifre Kipleri ve IV |
| Nonce / IV tekrarı | Anahtar dizisi tekrarlanır | Her mesajda benzersiz | Simetrik Şifreleme |
| Doğrulamasız şifreleme | Değişiklik fark edilmez | AEAD, önce doğrula | Doğrulanmış Şifreleme |
| Tek anahtarı her işe kullanmak | İşlemler birbirini zayıflatır | HKDF ile ayrı anahtarlar | Anahtar Türetme |
| Dolgusuz RSA | Belirleyici | OAEP, PSS | RSA |
| Kısa anahtar | Kaba kuvvete açık | AES-128+, RSA-2048+, eğri 256 | Kriptografi Nedir? |
| Sertifika doğrulamasını kapatmak | Kiminle konuşulduğu bilinmez | Her zaman açık | Sertifikalar ve PKI |
| Eski TLS sürümü | Bilinen zayıflıklar | TLS 1.3 / güçlü TLS 1.2 | TLS El Sıkışması |
| Kendi algoritmasını yazmak | Gözden kaçan zayıflık | Denenmiş kütüphane | Kriptografi Nedir? |

## Ayarları denetlemek

Hataların çoğu bir ayar dosyasında görünür. Bir yapılandırmayı satır satır
denetleyen küçük bir **denetçi** yazmak, yanlış ayarın üretime çıkmasını
engeller. Alıştırmalarda bunu adım adım kuracaksın: zayıf özet adı, kısa
anahtar, koda gömülü sır, ECB, sabit nonce, kapalı TLS doğrulaması.

## Özet

- Kodlama (Base64) şifreleme değildir.
- Gizli değerler `secrets` ile üretilir; `random` ile değil.
- Sırlar koda yazılmaz; sızan sır değiştirilir.
- Modüldeki her doğru kullanım kuralı tek bir katalogda: kip, nonce,
  doğrulama, KDF, anahtar boyu, dolgu, sertifika, TLS sürümü.
- Kriptografi kendi yazılmaz; doğru ayarlarla denenmiş kütüphane.
