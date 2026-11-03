# CSRF: Siteler Arası İstek Sahteciliği

Oturum ve Çerez bölümünde tarayıcının oturum çerezini **her istekte** geri
gönderdiğini gördük. Bu kolaylığın bir bedeli var: tarayıcı çerezi
isteğin **nereden başlatıldığına bakmadan** ekler. Kullanıcı bankasına
giriş yapmışken başka bir sitedeki bir sayfa, tarayıcısına bankaya bir
istek gönderttirebilir; çerez otomatik eklendiği için banka isteği
kullanıcıdan gelmiş sanır. Buna **CSRF** (cross-site request forgery,
siteler arası istek sahteciliği) denir. Bu bölüm açığı bir tarayıcı
taklidiyle gösteriyor, sonra savunmalarını kuruyor: CSRF jetonu,
`SameSite` çerezi, köken denetimi ve durumu değiştirmeyen `GET`. Bütün
"siteler" Python sözlükleri; hiçbir istek gönderilmiyor.

## Açık: çerez kendiliğinden gidiyor

Bir tarayıcıyı ve bir banka sunucusunu küçük fonksiyonlarla taklit
edelim. Tarayıcının çerez kutusunda bankanın oturum çerezi var:

```python
jar = {"bank.example": {"session": "s-ada"}}
SESSIONS = {"s-ada": "ada"}
BALANCE = {"ada": 1000}


def server(path, form, cookies):
    user = SESSIONS.get(cookies.get("session"))
    if user is None:
        return "401 login required"
    if path == "/transfer":
        BALANCE[user] -= int(form["amount"])
        return f"200 sent {form['amount']} to {form['to']}"
    return "404"


def browser_send(target, path, form, from_site):
    cookies = jar.get(target, {})
    return server(path, form, cookies)


print(browser_send("bank.example", "/transfer",
                   {"to": "bob", "amount": "50"}, "bank.example"))
print(browser_send("bank.example", "/transfer",
                   {"to": "mallory", "amount": "900"}, "games.example"))
print(BALANCE["ada"])
```

```text
200 sent 50 to bob
200 sent 900 to mallory
50
```

İlk isteği Ada bankanın kendi sayfasından gönderdi. İkincisini Ada'nın o
sırada açtığı bir oyun sitesindeki gizli bir form başlattı; tarayıcı
`from_site` değerine hiç bakmadan bankanın çerezini ekledi ve sunucu iki
isteği ayırt edemedi. Ada'nın bakiyesi 50'ye indi.

Üç şeyi not et:

- Saldırgan Ada'nın **çerezini görmedi**, çalmadı. Yalnızca tarayıcıya bir
  istek gönderttirdi.
- Saldırgan **cevabı da göremez**: tarayıcı, bir sitenin başka bir sitenin
  cevabını okumasını engeller (aynı köken politikası, CORS ve Güvenlik
  Başlıkları bölümü). CSRF bu yüzden veri okumak için değil, **bir işlem
  yaptırmak** için kullanılır: para göndermek, e-posta adresini
  değiştirmek, parola değiştirmek.
- Sunucunun sorduğu tek soru "bu çerez geçerli mi?" idi. Sorması gereken
  soru "bu isteği kullanıcı **bizim sayfamızdan** mı gönderdi?".

## Birinci savunma: CSRF jetonu

Sunucu, işlem formunu sayfaya koyarken içine tahmin edilemeyen bir
**jeton** ekler ve jetonu oturuma bağlar. Form gönderilince jeton
denetlenir. Başka bir site bu jetonu bilemez: bankanın sayfasını
okuyamadığı için içindeki jetonu da göremez.

```python
import hmac
import secrets

csrf_tokens = {}


def new_form(session_id):
    token = secrets.token_urlsafe(32)
    csrf_tokens[session_id] = token
    return token


def check(session_id, form):
    expected = csrf_tokens.get(session_id)
    sent = form.get("csrf", "")
    return expected is not None and hmac.compare_digest(expected, sent)


token = new_form("s-ada")
print(check("s-ada", {"to": "bob", "amount": "50", "csrf": token}))
print(check("s-ada", {"to": "mallory", "amount": "900"}))
print(check("s-ada", {"to": "mallory", "amount": "900", "csrf": "guess"}))
```

```text
True
False
False
```

Bankanın kendi formundan gelen istek geçti; jetonsuz ve yanlış jetonlu
istekler reddedildi. Jeton `secrets` ile üretilir (Oturum ve Çerez
bölümündeki oturum kimliği gibi) ve `hmac.compare_digest` ile
karşılaştırılır. Sunucu tarafında saklamak istemeyen uygulamalar jetonu
bir çerezde de tutup formdakiyle karşılaştırabilir (**çift gönderimli
çerez**, double-submit cookie); fikir aynıdır: başka bir site formdaki
değeri bilemez.

Jeton yalnızca durum değiştiren isteklerde (`POST`, `PUT`, `PATCH`,
`DELETE`) denetlenir; bu yüzden aşağıdaki kural önemlidir.

## İkinci savunma: SameSite çerezi

Oturum ve Çerez bölümünde `SameSite` özniteliğini gördük. Tarayıcı, başka
bir siteden başlatılan bir isteğe çerezi ekleyip eklemeyeceğine bu
özniteliğe bakarak karar verir:

```python
def sends_cookie(samesite, cross_site, method, top_level):
    if not cross_site:
        return True
    if samesite == "Strict":
        return False
    if samesite == "Lax":
        return method == "GET" and top_level
    return True


cases = [("Strict", "POST", False), ("Lax", "POST", False),
         ("Lax", "GET", True), ("None", "POST", False)]
for samesite, method, top in cases:
    print(f"{samesite:<6} {method:<4} top={top!s:<5} -> "
          f"{sends_cookie(samesite, True, method, top)}")
```

```text
Strict POST top=False -> False
Lax    POST top=False -> False
Lax    GET  top=True  -> True
None   POST top=False -> True
```

- **`Strict`:** başka siteden başlayan hiçbir isteğe çerez eklenmez. En
  güvenlisi; ama başka bir siteden bağlantıyla gelen kullanıcı ilk sayfada
  giriş yapmamış görünür.
- **`Lax`:** başka siteden yalnızca **üst düzey gezinme** (bağlantıya
  tıklayıp sayfanın değişmesi) ve `GET` ile gelen isteğe çerez eklenir.
  Gizli formla gönderilen `POST` çerezsiz gider. Oturum çerezi için iyi
  bir varsayılandır.
- **`None`:** her isteğe eklenir (yalnızca `Secure` ile birlikte kabul
  edilir). Gerçekten başka sitelerde kullanılması gereken çerezler için.

Bazı tarayıcılar özniteliği olmayan çerezi `Lax` sayar, ama buna
güvenilmez; öznitelik açıkça yazılır. `SameSite` güçlü bir **ikinci
katmandır**, jetonun yerini tutmaz: eski tarayıcılar onu bilmez ve aynı
sitenin bir alt alanı "aynı site" sayılır.

## GET durumu değiştirmez

`Lax` satırına bak: başka siteden gelen üst düzey `GET` isteğinde çerez
gider. Eğer `GET /transfer?to=mallory&amount=900` gibi bir adres para
gönderiyorsa, saldırganın yapması gereken tek şey kullanıcıya o bağlantıyı
tıklatmaktır. HTTP ve HTTPS bölümündeki kural burada hayatidir: **`GET`
sunucuda hiçbir şey değiştirmez.** Durum değiştiren her iş `POST` gibi bir
yöntemle ve jetonla yapılır.

## Üçüncü savunma: köken denetimi

Tarayıcılar başka siteden başlayan `POST` isteklerine isteğin hangi
**kökenden** (şema + ana bilgisayar + port) geldiğini söyleyen bir
`Origin` başlığı ekler; sayfanın kendisi bu başlığı değiştiremez. Sunucu
durum değiştiren isteklerde bu başlığı bir izin listesiyle karşılaştırır:

```python
ALLOWED = {"https://bank.example"}


def origin_ok(headers):
    return headers.get("origin") in ALLOWED


print(origin_ok({"origin": "https://bank.example"}))
print(origin_ok({"origin": "https://games.example"}))
print(origin_ok({}))
```

```text
True
False
False
```

Başlık yoksa ne yapılacağına önceden karar verilir: ya `Referer`
başlığının kökenine bakılır ya da istek reddedilir. Köken denetimi de
jetonun yanında bir katmandır.

## Önemli işlemde yeniden doğrulama

Parola değiştirmek, e-posta adresini değiştirmek, büyük tutarlı ödeme gibi
işlemlerde kullanıcıdan **parolası** ya da bir MFA kodu yeniden istenir.
Başka bir site kullanıcının parolasını bilmediği için bu adımı geçemez.

## CSRF ve XSS

CSRF savunmalarının hepsi "istek **başka bir siteden** geliyor"
varsayımına dayanır. Sitede bir XSS açığı varsa, sızan betik **sitenin
kendi içinde** çalışır: sayfadaki jetonu okur, `Origin` doğru görünür,
`SameSite` engellemez. Bu yüzden XSS açığı CSRF savunmasını da boşa
çıkarır; iki açık birlikte kapatılır.

## Özet

- **CSRF:** tarayıcı çerezi isteğin nereden başladığına bakmadan ekler;
  başka bir site kullanıcı adına **işlem yaptırır** (cevabı okuyamaz).
- **CSRF jetonu:** oturuma bağlı, `secrets` ile üretilmiş, formda giden ve
  `compare_digest` ile denetlenen değer; başka site onu bilemez.
- **SameSite:** `Lax` başka siteden gelen `POST`'a çerez eklemez,
  `Strict` hiçbir isteğe eklemez. Açıkça yazılır; jetonun yerini tutmaz.
- **`GET` durum değiştirmez;** `Lax` üst düzey `GET`'e çerez ekler.
- **Köken denetimi:** `Origin` başlığı izin listesiyle karşılaştırılır.
- Önemli işlemde parola ya da MFA yeniden istenir.
- XSS açığı CSRF savunmalarını boşa çıkarır.
