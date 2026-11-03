# Oturum ve Çerez

HTTP **durumsuzdur** (stateless): her istek öncekinden bağımsızdır, sunucu
bir isteğin az önce giriş yapan kişiden gelip gelmediğini kendiliğinden
bilmez. Her sayfada yeniden parola sormamak için **oturum** (session)
kullanılır: giriş başarılı olunca sunucu kişiye bir **oturum kimliği**
verir, tarayıcı bunu bir **çerezde** (cookie) saklayıp her istekte geri
gönderir. Bu kimlik artık parolanın yerini tutar; onu ele geçiren kişi,
parolayı bilmeden hesaba girer. Bu bölüm oturum kimliğinin nasıl
üretileceğini, çerezin nasıl korunacağını ve oturumun ne zaman
bitirileceğini anlatıyor.

## Oturum kimliği

Sunucu, kimliği bir sözlükte (gerçekte bir veritabanında) kişiyle eşler.
Kimlik **tahmin edilemez** olmalıdır; Kriptografi modülünün Rastgelelik
bölümündeki `secrets` modülü bunun içindir:

```python
import secrets

sessions = {}


def login(user):
    sid = secrets.token_urlsafe(32)
    sessions[sid] = {"user": user}
    return sid


sid = login("ada")
print(len(sid))
print(sessions[sid]["user"])
```

```text
43
ada
```

`token_urlsafe(32)` 32 rastgele bayttan (256 bit) URL'de güvenle
kullanılabilen 43 karakterlik bir metin üretir. Tahmin etmek
olanaksızdır. Kimliği sayaçla üretmek ise ciddi bir hatadır:

```python
counter = 1000


def weak_login(user):
    global counter
    counter += 1
    return f"s{counter}"


print(weak_login("ada"), weak_login("bob"))
```

```text
s1001 s1002
```

Kendi kimliği `s1001` olan biri, bir sonraki kullanıcının `s1002`
alacağını bilir; çerezini değiştirip onun oturumuna girer. Zaman damgası,
kullanıcı adı ya da `random` modülüyle üretilen kimlikler de aynı nedenle
tahmin edilebilir.

## Çerez ve öznitelikleri

Sunucu çerezi bir cevap başlığıyla koyar: `Set-Cookie: session=...`.
Başlığın sonuna eklenen **öznitelikler** çerezin nasıl korunacağını
söyler:

<figure class="fig anat">
  <div class="anat-row"><span><b>Secure</b></span><span>Çerez yalnızca HTTPS ile gönderilir; düz HTTP'de yolda okunmaz.</span></div>
  <div class="anat-row"><span><b>HttpOnly</b></span><span>Sayfadaki JavaScript çereze erişemez; XSS ile çalınması zorlaşır (XSS bölümü).</span></div>
  <div class="anat-row"><span><b>SameSite</b></span><span>Başka bir siteden başlatılan isteklerde çerezin gönderilip gönderilmeyeceği: <code>Strict</code>, <code>Lax</code>, <code>None</code>. CSRF'e karşı (CSRF bölümü).</span></div>
  <div class="anat-row"><span><b>Max-Age / Expires</b></span><span>Çerezin ne kadar yaşayacağı. Yoksa tarayıcı kapanınca silinir.</span></div>
  <div class="anat-row"><span><b>Path / Domain</b></span><span>Çerezin hangi yollara ve alan adlarına gönderileceği. <code>Domain</code> genişletildikçe daha çok alt alan çerezi görür.</span></div>
  <figcaption>Oturum çerezinde Secure, HttpOnly ve SameSite neredeyse her zaman açık olur.</figcaption>
</figure>

Bir `Set-Cookie` başlığını parçalayıp eksik öznitelikleri bulalım:

```python
def cookie_flags(header):
    parts = [p.strip() for p in header.split(";")]
    name = parts[0].partition("=")[0]
    flags = {}
    for p in parts[1:]:
        key, _, value = p.partition("=")
        flags[key.lower()] = value
    return name, flags


for header in ["session=abc123; Path=/",
               "session=abc123; Path=/; Secure; HttpOnly; SameSite=Lax"]:
    name, flags = cookie_flags(header)
    missing = [f for f in ["secure", "httponly", "samesite"] if f not in flags]
    print(name, "missing:", missing)
```

```text
session missing: ['secure', 'httponly', 'samesite']
session missing: []
```

İlk çerez üç korumanın üçünden de yoksun: düz HTTP sayfasında yolda
okunur, sayfaya sızan bir betik onu okuyabilir ve başka sitelerden
başlatılan isteklere eklenir. İkincisi doğru kurulmuş.

## Oturum sabitleme

Saldırgan kendi seçtiği bir oturum kimliğini kurbanın tarayıcısına
yerleştirebilirse (örneğin bir alt alandan çerez koyarak) ve sunucu girişten
sonra **aynı kimliği** kullanmaya devam ederse, kurban giriş yaptığı anda
saldırganın bildiği kimlik yetkili bir oturuma dönüşür. Buna **oturum
sabitleme** (session fixation) denir. Savunması basittir: **girişte kimlik
yenilenir.**

```python
import secrets

sessions = {}


def login_keep(sid, user):
    sessions[sid] = user
    return sid


def login_rotate(sid, user):
    sessions.pop(sid, None)
    new_sid = secrets.token_urlsafe(32)
    sessions[new_sid] = user
    return new_sid


planted = "attacker-chosen-id"
print(login_keep(planted, "ada") == planted)
print(login_rotate(planted, "ada") == planted, planted in sessions)
```

```text
True
False False
```

İlk yöntemde girişten sonra da saldırganın kimliği geçerli. İkincisinde
eski kimlik silindi, yerine kimsenin bilmediği yeni bir kimlik geldi.
Aynı kural yetki değiştiğinde de uygulanır: kişi yönetici olunca ya da
parolasını değiştirince kimlik yenilenir.

## Oturumun sonu

Bir oturum sonsuza kadar geçerli kalmamalı. Çalınan bir kimlik ne kadar
kısa yaşarsa zararı o kadar az olur. İki süre kullanılır:

- **Boşta kalma süresi** (idle timeout): son istekten bu yana belli bir
  süre geçtiyse oturum biter (masada açık bırakılan bilgisayar).
- **Mutlak süre** (absolute timeout): kişi sürekli çalışsa bile, girişten
  bu yana belli bir süre geçtiyse yeniden giriş istenir.

```python
IDLE, ABSOLUTE = 15 * 60, 8 * 3600


def still_valid(created, last_seen, now):
    return now - last_seen < IDLE and now - created < ABSOLUTE


print(still_valid(0, 0, 600))
print(still_valid(0, 0, 1200))
print(still_valid(0, 28700, 28900))
```

```text
True
False
False
```

10 dakika sonra oturum geçerli, 20 dakika boşta kaldıktan sonra değil.
Üçüncü durumda kişi 200 saniye önce işlem yapmış ama girişin üstünden 8
saatten fazla geçmiş; oturum bitti.

**Çıkış** (logout) yalnızca tarayıcıdaki çerezi silmek değildir: sunucu
oturum kaydını da siler. Yoksa çerezin bir kopyasını almış biri çıkıştan
sonra da devam eder.

## Durumu çerezde tutmak: imzalı çerez

Bazı uygulamalar oturum bilgisini sunucuda değil çerezin **kendisinde**
tutar (`user=ada;role=user`). Kullanıcı çerezi istediği gibi
değiştirebildiği için bu bilgi **imzalanmak** zorundadır. HMAC bölümündeki
etiket tam bunu yapar:

```python
import hashlib
import hmac

KEY = b"server-only-secret"


def sign(value):
    tag = hmac.new(KEY, value.encode(), hashlib.sha256).hexdigest()
    return value + "." + tag


def read(cookie):
    value, _, tag = cookie.rpartition(".")
    expected = hmac.new(KEY, value.encode(), hashlib.sha256).hexdigest()
    return value if hmac.compare_digest(tag, expected) else None


cookie = sign("user=ada;role=user")
print(read(cookie))
print(read(cookie.replace("role=user", "role=admin")))
```

```text
user=ada;role=user
None
```

Kullanıcı rolünü `admin` yapınca etiket tutmadı ve çerez reddedildi
(`None`). İmza bilgiyi **gizlemez**, yalnızca değiştirilmesini önler;
çerezdeki her şey okunabilir. Gizli bir şey çereze yazılmaz. İmzalı
çerezin bir zayıflığı da sunucunun onu tek başına geçersiz kılamamasıdır:
süresi dolana kadar geçerlidir. Bu yüzden içine bir son geçerlilik zamanı
konur.

## Özet

- HTTP durumsuzdur; **oturum kimliği** girişten sonra parolanın yerini
  tutar. Onu çalan hesaba girer.
- Kimlik `secrets` ile üretilir (`token_urlsafe(32)`, 256 bit); sayaç,
  zaman ya da `random` ile üretilen kimlik tahmin edilir.
- Oturum çerezinde **Secure**, **HttpOnly** ve **SameSite** açık olur.
- **Oturum sabitleme**ye karşı girişte (ve yetki değişince) kimlik
  yenilenir.
- Oturum **boşta kalma** ve **mutlak** süreyle biter; çıkışta sunucudaki
  kayıt da silinir.
- Çerezde durum tutulacaksa **imzalanır** (HMAC); imza gizlemez, gizli
  bilgi çereze yazılmaz.
