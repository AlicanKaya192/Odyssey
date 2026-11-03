# Mesaj Doğrulama: HMAC

Özet Fonksiyonları bölümü bir uyarıyla bitti: düz bir özet, veriyi
**kazara** bozulmaya karşı korur ama **kasıtlı** değişikliğe karşı
korumaz. Saldırgan veriyi değiştirip özeti de yeniden hesaplar. XOR ve Tek
Kullanımlık Şifre bölümünde de şifrelemenin bütünlük sağlamadığını, şifreli
metnin bit bit değiştirilebildiğini gördük. Bu bölüm iki soruyu birden
cevaplayan aracı anlatıyor: **mesaj değişti mi** ve **bunu anahtarı bilen
biri mi gönderdi**.

## Mesaj doğrulama kodu (MAC)

Çözüm, özete bir **gizli anahtar** katmaktır. Gönderen ile alıcı aynı
anahtarı paylaşır. Gönderen mesajın yanına anahtarla hesaplanmış bir
**etiket** (tag) ekler; alıcı aynı anahtarla etiketi yeniden hesaplar ve
karşılaştırır. Anahtarı bilmeyen geçerli bir etiket üretemez. Bu etikete
**mesaj doğrulama kodu** (message authentication code, MAC) denir.

En yaygın MAC, bir özet fonksiyonunu anahtarla saran **HMAC**'tir. Python'ın
standart kütüphanesinde hazır gelir:

```python
import hashlib
import hmac

key = b"shared-secret-key"
message = b"transfer 100 to bob"
tag = hmac.new(key, message, hashlib.sha256).hexdigest()
print(tag[:32])
print(len(tag))
```

```text
c3e2b5cb52e9b0f62c7efef90eb5b2c7
64
```

Etiket, mesajın ve anahtarın birlikte parmak izidir; SHA-256 tabanlı
olduğu için 64 onaltılık hanedir. Kimlik Yönetimi ve Tek Oturum
bölümündeki oyuncak jetonu tam olarak böyle imzalamıştık.

## Doğrulama

Alıcı mesajı ve etiketi alır, etiketi kendi anahtarıyla yeniden hesaplar.
Mesaj ya da etiket değiştiyse yeni etiket tutmaz:

```python
import hashlib
import hmac


def verify(key, message, tag):
    expected = hmac.new(key, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, tag)


key = b"shared-secret-key"
message = b"transfer 100 to bob"
tag = hmac.new(key, message, hashlib.sha256).hexdigest()

print(verify(key, message, tag))
print(verify(key, b"transfer 900 to eve", tag))
print(verify(b"wrong-key", message, tag))
```

```text
True
False
False
```

- Birinci satır `True`: mesaj ve etiket değişmedi.
- İkinci satır `False`: mesaj değişti, saldırgan anahtarı bilmediği için
  yeni mesaja uygun etiketi üretemedi. XOR bölümündeki `PAY BOB 100` →
  `PAY BOB 900` saldırısı artık yakalanıyor.
- Üçüncü satır `False`: anahtar yanlış.

## Neden `sha256(key + message)` değil?

Akla ilk gelen "anahtarı mesajın başına ekleyip özetini al" olur. Ama
yaygın özet fonksiyonlarının iç yapısı buna **uzatma saldırısı**
(length-extension) denen bir açık bırakır: saldırgan anahtarı bilmeden,
geçerli bir etiketi olan mesajın **sonuna** ekleme yapıp yeni mesaj için de
geçerli bir etiket üretebilir. Ayrıntısına girmiyoruz; önemli olan şu:
HMAC bu sorunu olmayan özel bir yapıyla (anahtarı iki kez, farklı
dolgularla karıştırarak) kurulmuştur. **Kendin `sha256(key + message)`
yazma; `hmac` modülünü kullan.** Güvenlik İlkeleri bölümündeki "kendi
kriptonu yazma" kuralının küçük ama tipik bir örneği.

## Karşılaştırma neden `==` ile değil?

Doğrularken `expected == tag` yazmak sonucu doğru verir ama bir yan kanal
açar. Python'ın `==` işleci iki diziyi karşılaştırırken **ilk farklı
baytta durur**; doğru etikete yakın bir tahmin, uzak bir tahminden azıcık
daha uzun sürer. Bu süre farkını ölçen bir saldırgan etiketi bayt bayt
bulabilir. `hmac.compare_digest` farkı nerede olursa olsun **aynı sürede**
karşılaştırır (sabit süreli karşılaştırma):

```python
import hmac

a = "a" * 64
b = "a" * 63 + "b"
print(a == a, hmac.compare_digest(a, a))
print(a == b, hmac.compare_digest(a, b))
```

```text
True True
False False
```

Sonuçlar aynı (`True`/`False`), ama `compare_digest` zamanlamayı ele
vermez. Etiket, parola özeti ya da jeton karşılaştıran her yerde bu
kullanılır. Parolaları Saklamak bölümünde parola özetlerini de bununla
karşılaştırmıştık.

## MAC mi, imza mı?

<figure class="fig"><div class="versus">
  <div><h4>HMAC (simetrik)</h4>Gönderen ve alıcı <b>aynı</b> gizli anahtarı paylaşır. Hızlıdır. Ama etiketi iki taraf da üretebildiği için, bir tarafın "bunu öteki gönderdi" diye <b>üçüncü bir kişiye kanıtlaması</b> mümkün değildir.</div>
  <div><h4>Dijital imza (asimetrik)</h4>Gönderen <b>özel</b> anahtarıyla imzalar, herkes <b>açık</b> anahtarla doğrular. Yavaştır. Yalnızca özel anahtarın sahibi üretebildiği için üçüncü kişiye kanıt (<b>inkâr edilemezlik</b>) sağlar.</div>
</div><figcaption>İki taraf arasında bütünlük için HMAC; üçüncü kişiye kanıt için imza (Dijital İmza bölümü).</figcaption></figure>

Güvenlik Nedir? CIA Üçlüsü bölümündeki tabloyu hatırla: HMAC bütünlük ve
kimlik doğruluğu sağlar; inkâr edilemezlik için dijital imza gerekir.

## Önce doğrula, sonra kullan

Doğrulanmış bir mesajı işlerken sıra önemlidir: **önce etiketi denetle,
tutmazsa mesajı hiç açma.** Kimlik Yönetimi bölümündeki jetonda da aynı
kuralı görmüştük: önce imza, sonra içerik.

```python
import hashlib
import hmac

KEY = b"shared-secret-key"


def handle(message, tag):
    expected = hmac.new(KEY, message, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, tag):
        return "rejected"
    return "accepted: " + message.decode()


msg = b"ok"
good = hmac.new(KEY, msg, hashlib.sha256).hexdigest()
print(handle(msg, good))
print(handle(b"tampered", good))
```

```text
accepted: ok
rejected
```

Etiketi tutmayan mesaj hiç açılmadan reddedildi. Bu, Doğrulanmış Şifreleme
bölümünün temelini kuruyor: orada şifreleme ile MAC bir arada çalışıp hem
gizlilik hem bütünlük sağlayacak.

## Özet

- **MAC** mesajın değişmediğini **ve** anahtarı bilen birinden geldiğini
  kanıtlar; düz özetin yapamadığı budur.
- **HMAC** bir özet fonksiyonunu anahtarla sarar; `hmac.new(key, message,
  hashlib.sha256)`.
- **`sha256(key + message)` yazma:** uzatma saldırısına açık. `hmac`
  modülünü kullan.
- Etiketleri **`hmac.compare_digest`** ile karşılaştır: sabit süreli,
  zamanlamayı ele vermez.
- **HMAC simetriktir** (ortak anahtar, inkâr edilemezlik yok); üçüncü
  kişiye kanıt için **dijital imza** gerekir.
- Doğrulanmış mesajda **önce etiketi denetle, sonra içeriği kullan.**
