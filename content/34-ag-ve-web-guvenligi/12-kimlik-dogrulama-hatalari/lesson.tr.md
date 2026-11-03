# Kimlik Doğrulama Hataları

Güvenlik Temelleri modülünde kimlik doğrulamanın kavramlarını (bilinen,
sahip olunan, olunan; MFA) ve parolaların nasıl saklanacağını gördük.
Oturum ve Çerez bölümü girişten **sonrasını** işledi. Bu bölüm girişin
**kendisindeki** hatalara bakıyor: kullanıcı adlarını ele veren mesajlar,
sınırsız deneme, parola sıfırlama akışı ve zayıf parola kuralları. OWASP
Top 10'daki A07 kategorisi bunların toplamıdır. Örneklerin hepsi küçük
Python fonksiyonları; hiçbir gerçek sisteme giriş denenmiyor.

## Kullanıcı adını ele vermek

Giriş başarısız olduğunda **neden** başarısız olduğunu söylemek kullanıcıya
yardım gibi görünür, ama saldırgana da yardım eder:

```python
USERS = {"ada", "bob"}


def login_leaky(user, password_ok):
    if user not in USERS:
        return "no such user"
    if not password_ok:
        return "wrong password"
    return "welcome"


def login_safe(user, password_ok):
    if user in USERS and password_ok:
        return "welcome"
    return "invalid user name or password"


for user in ["ada", "zeynep"]:
    print(f"{user:<7} {login_leaky(user, False):<15} {login_safe(user, False)}")
```

```text
ada     wrong password  invalid user name or password
zeynep  no such user    invalid user name or password
```

İlk fonksiyon `zeynep` diye bir kullanıcı olmadığını, `ada`'nın ise var
olduğunu söyledi. Buna **kullanıcı adı numaralandırma** (user enumeration)
denir: saldırgan önce hangi hesapların var olduğunu öğrenir, sonra
yalnızca onlara yüklenir. Doğrusu, iki durumda da **aynı** mesajı
vermektir. Aynı ilke kayıt ve parola sıfırlama sayfalarında da geçerli:
"bu e-postaya bağlantı gönderdik" mesajı, adres kayıtlı olsun olmasın aynı
olur.

Mesaj kadar **süre** de ele verebilir. Bilinmeyen kullanıcı için parola
özeti hiç hesaplanmazsa cevap daha hızlı döner. Güvenlik Temelleri'nin
Genel Tekrar bölümündeki programda bu yüzden bilinmeyen kullanıcı için de
özet hesaplanıyordu.

## Sınırsız deneme

Hiçbir sınır yoksa saldırgan bir hesap için binlerce parola dener (**kaba
kuvvet**), ya da başka sitelerden sızmış kullanıcı adı–parola çiftlerini
sırayla dener; insanlar aynı parolayı birçok yerde kullandığı için bu
çiftlerin bir kısmı tutar. Buna **kimlik bilgisi doldurma** (credential
stuffing) denir.

Hesabı birkaç hatadan sonra tamamen kilitlemek ilk akla gelen çözümdür,
ama saldırgana başka bir silah verir: herkesin hesabını bilerek kilitleyip
kullanılamaz hâle getirmek (Ağ Saldırıları bölümündeki hizmet engelleme).
Daha dengeli yol **artan bekleme süresidir**: birkaç hatadan sonra her yeni
hatada bekleme ikiye katlanır, bir üst sınırla:

```python
def delay_after(failures):
    if failures < 3:
        return 0
    return min(2 ** (failures - 3), 300)


print([delay_after(n) for n in range(1, 12)])
```

```text
[0, 0, 1, 2, 4, 8, 16, 32, 64, 128, 256]
```

Parolasını iki kez yanlış yazan kişi hiç beklemez; onuncu hatada iki
dakikadan fazla beklenir. Saniyede binlerce deneme yapmak isteyen bir
saldırgan için bu, denemenin pratikte durması demektir. Sınır **hem hesap
başına hem kaynak başına** tutulur: kimlik bilgisi doldurmada saldırgan
her hesabı bir kez dener ama bunu tek bir kaynaktan çok sayıda hesap için
yapar, ve bu kayıtlarda görünür:

```python
from collections import defaultdict

log = [("198.51.100.9", f"user{i}", False) for i in range(25)] + [
    ("192.168.1.10", "ada", False), ("192.168.1.10", "ada", True)]

failed_users = defaultdict(set)
for src, user, ok in log:
    if not ok:
        failed_users[src].add(user)
for src, users in sorted(failed_users.items()):
    print(src, len(users), "SUSPECT" if len(users) >= 10 else "ok")
```

```text
192.168.1.10 1 ok
198.51.100.9 25 SUSPECT
```

Tek bir kaynaktan 25 farklı hesaba başarısız giriş, kimlik bilgisi
doldurmanın tipik izidir. En güçlü savunma ise **çok faktörlü kimlik
doğrulamadır**: sızan parola tek başına yetmez.

## Parola sıfırlama

"Parolamı unuttum" akışı, parolayı hiç bilmeden hesaba girmenin yasal
yoludur; bu yüzden en az giriş kadar dikkat ister. Sıfırlama bağlantısındaki
jeton:

- `secrets` ile üretilir, tahmin edilemez;
- **kısa ömürlüdür** (örneğin 15 dakika);
- **bir kez** kullanılır;
- sunucuda **özeti** saklanır: veritabanı sızarsa jetonlar kullanılamasın
  (parolalar gibi).

```python
import hashlib
import hmac
import secrets

store = {}


def issue(user, now):
    token = secrets.token_urlsafe(32)
    digest = hashlib.sha256(token.encode()).hexdigest()
    store[user] = {"hash": digest, "expires": now + 900, "used": False}
    return token


def redeem(user, token, now):
    record = store.get(user)
    if record is None or record["used"] or now >= record["expires"]:
        return False
    digest = hashlib.sha256(token.encode()).hexdigest()
    if not hmac.compare_digest(record["hash"], digest):
        return False
    record["used"] = True
    return True


token = issue("ada", 0)
print(redeem("ada", "guess", 10))
print(redeem("ada", token, 20))
print(redeem("ada", token, 30))
late = issue("ada", 0)
print(redeem("ada", late, 1000))
```

```text
False
True
False
False
```

Yanlış jeton reddedildi; doğru jeton bir kez çalıştı, ikinci kullanımda
reddedildi; 900 saniyeyi geçen jeton da reddedildi. Parola değiştikten
sonra kişinin **diğer bütün oturumları** kapatılır (Oturum ve Çerez
bölümü): parolayı değiştirme sebebi zaten birinin içeride olması olabilir.

Burada jetonun özeti için hızlı bir özet (SHA-256) yeterlidir: parolanın
aksine jeton 256 bitlik rastgele bir değerdir, tahminle bulunamaz.
Parolalar için yavaş özet gerekmesinin sebebi insanların tahmin edilebilir
parolalar seçmesidir.

## Parola kuralları

Eski kurallar "bir büyük harf, bir rakam, bir işaret, her 90 günde
değiştir" derdi; sonuç `Parola1!` gibi tahmin edilebilir parolalar ve
kâğıda yazılmış notlar oldu. Bugünkü yaklaşım (Parolalar bölümü)
**uzunluğa** ve **bilinen kötü parolaları reddetmeye** dayanır:

```python
COMMON = {"123456", "password", "qwerty", "iloveyou", "admin123"}


def password_problems(password, user):
    problems = []
    if len(password) < 8:
        problems.append("too short")
    if password.lower() in COMMON:
        problems.append("common")
    if user.lower() in password.lower():
        problems.append("contains user name")
    return problems


for pw in ["qwerty", "Ada2026!", "blue-river-under-stone"]:
    print(f"{pw:<24} {password_problems(pw, 'ada')}")
```

```text
qwerty                   ['too short', 'common']
Ada2026!                 ['contains user name']
blue-river-under-stone   []
```

Gerçek sistemler `COMMON` yerine sızıntılarda görülmüş milyonlarca
parolanın listesini kullanır. Uzun ve kullanıcı adını içermeyen parola
geçti. Parola yalnızca bir sızıntı belirtisi olduğunda değiştirilir,
takvime göre değil; parola yöneticisi kullanmak teşvik edilir.

## Başka sık hatalar

- **Varsayılan parolalar:** kurulumla gelen `admin/admin` hesabı yayında
  kalır (OWASP Top 10'daki A02 ile kesişir).
- **Kimlik bilgisini URL'de taşımak:** parola ya da jeton adreste olursa
  kayıtlara ve `Referer`'a gider (HTTP ve HTTPS bölümü).
- **MFA'yı atlanabilir bırakmak:** MFA adımı ayrı bir sayfaysa ve sunucu
  ikinci adımın tamamlandığını denetlemeden oturumu tam yetkili sayıyorsa
  MFA kâğıt üstünde kalır.
- **Giriş denemelerini kaydetmemek:** başarısız ve başarılı girişler, kaynak
  ve zamanla kaydedilir (parola değil).

## Özet

- Başarısız girişte **tek bir mesaj**: "kullanıcı adı ya da parola
  yanlış"; süre de ele vermez.
- **Kaba kuvvet** ve **kimlik bilgisi doldurma**ya karşı hesap ve kaynak
  başına sınır, **artan bekleme** ve en çok **MFA**. Tamamen kilitlemek
  hizmet engellemeye kapı açar.
- **Sıfırlama jetonu** rastgele, kısa ömürlü, tek kullanımlık ve sunucuda
  özetli; parola değişince öteki oturumlar kapanır.
- **Parola kuralı** uzunluk ve bilinen kötü parolaların reddi; zorunlu
  periyodik değişim ve karmaşıklık kuralı değil.
- Varsayılan parolalar kaldırılır, kimlik bilgisi URL'ye konmaz, MFA
  sunucuda denetlenir, girişler kaydedilir.
