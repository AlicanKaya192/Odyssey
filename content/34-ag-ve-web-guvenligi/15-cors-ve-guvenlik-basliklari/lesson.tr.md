# CORS ve Güvenlik Başlıkları

Tarayıcı, bir sitenin sayfasında çalışan betiğin başka bir siteden veri
okumasını varsayılan olarak engeller. Bu kurala **aynı köken politikası**
(same-origin policy) denir ve web güvenliğinin temel taşıdır: yoksa açık
duran herhangi bir sekme, bankanızın sayfasındaki bilgileri okuyabilirdi.
Bazen bu kuralı bilerek gevşetmek gerekir (sitenin kendi API'si ayrı bir
adreste duruyorsa); bunun yolu **CORS**'tur. Bu bölüm CORS'un nasıl
çalıştığını, en sık yapılan yapılandırma hatalarını ve sunucunun
tarayıcıya gönderdiği **güvenlik başlıklarını** küçük Python
fonksiyonlarıyla gösteriyor.

## Köken nedir?

**Köken** (origin) üç parçadır: şema, alan adı ve port. Üçü de aynıysa iki
adres aynı kökendendir; yol önemli değildir:

```python
from urllib.parse import urlsplit

DEFAULT_PORTS = {"http": 80, "https": 443}


def origin(url):
    parts = urlsplit(url)
    port = parts.port or DEFAULT_PORTS[parts.scheme]
    return parts.scheme, parts.hostname, port


base = "https://shop.example/cart"
for other in [
    "https://shop.example:443/account",
    "http://shop.example/cart",
    "https://api.shop.example/cart",
    "https://shop.example:8443/cart",
]:
    print(origin(base) == origin(other), other)
```

```text
True https://shop.example:443/account
False http://shop.example/cart
False https://api.shop.example/cart
False https://shop.example:8443/cart
```

Port yazılmadığında HTTPS için 443 sayılır; bu yüzden ilk adres aynı
köken. Şema (`http`), alt alan adı (`api.`) ya da port (`8443`) değişince
köken değişir. Alt alan adı da ayrı bir kökendir: `api.shop.example`,
`shop.example`'ın sayfalarını okuyamaz.

Aynı köken politikası **okumayı** engeller, **göndermeyi** değil: başka
bir sitenin formu sizin sitenize istek gönderebilir. CSRF bölümünde bu
yüzden jeton ve `SameSite` gerekti.

## CORS: izni sunucu verir

Tarayıcı başka bir kökene istek gönderirken isteğe `Origin` başlığını
koyar. Sunucu cevabında `Access-Control-Allow-Origin` ile bu kökene
okuma izni verirse, tarayıcı cevabı betiğe teslim eder; vermezse betik
cevabı göremez. Kararı **sunucu** verir, uygulayan **tarayıcıdır**.

En tehlikeli hata, gelen `Origin`'i olduğu gibi geri yazmaktır, özellikle
çerezlerle birlikte:

```python
def cors_leaky(origin):
    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
    }


ALLOWED_ORIGINS = {"https://shop.example", "https://admin.shop.example"}


def cors_safe(origin):
    headers = {"Vary": "Origin"}
    if origin in ALLOWED_ORIGINS:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return headers


for origin in ["https://shop.example", "https://other.example"]:
    print(origin)
    print("  leaky:", cors_leaky(origin)["Access-Control-Allow-Origin"])
    print("  safe: ", cors_safe(origin).get("Access-Control-Allow-Origin"))
```

```text
https://shop.example
  leaky: https://shop.example
  safe:  https://shop.example
https://other.example
  leaky: https://other.example
  safe:  None
```

`cors_leaky` her siteye "çerezlerle birlikte oku" izni verdi: kullanıcı
herhangi bir sayfayı açtığında, o sayfanın betiği kullanıcının oturumuyla
API'nizden veri okuyabilir. Aynı köken politikası tamamen ortadan kalkmış
olur. `cors_safe` yalnızca **izin listesindeki** kökenlere izin veriyor.

`Vary: Origin` başlığı, aradaki önbelleğe cevabın `Origin`'e göre
değiştiğini söyler; yoksa bir kökene verilen cevap önbellekten başka bir
kökene de dönebilir. Tarayıcı `Access-Control-Allow-Origin: *` ile
çerezli isteği zaten kabul etmez; `*` yalnızca herkese açık, kimlik
istemeyen veriler için uygundur.

## İzin listesini metinle denetlemek

İzin listesi yerine "sonu bizim alan adımızla bitiyorsa" demek cazip
görünür, ama sonu aynı biten **başka** bir alan adını da kabul eder:

```python
def allowed_suffix(origin):
    return origin.endswith("shop.example")


def allowed_exact(origin):
    return origin in ALLOWED_ORIGINS


ALLOWED_ORIGINS = {"https://shop.example", "https://admin.shop.example"}
for origin in ["https://admin.shop.example", "https://notshop.example"]:
    print(f"{origin:<27} {allowed_suffix(origin)!s:<5} {allowed_exact(origin)}")
```

```text
https://admin.shop.example  True  True
https://notshop.example     True  False
```

`notshop.example` bizim alan adımız değil, ama `shop.example` ile bitiyor.
Kökenler **tam eşitlikle** ve bir kümeyle denetlenir; desen gerekiyorsa
nokta dahil (`.shop.example`) ve şema ile birlikte, `re.fullmatch` ile.
`Origin: null` değeri de izin listesine konmaz: dosyadan açılan sayfalar ve
bazı yönlendirmeler bu değeri gönderir.

## Ön kontrol isteği

Bazı istekler tarayıcı tarafından önce bir **ön kontrol** (preflight)
isteğiyle sorulur: `OPTIONS` yöntemiyle "bu kökenden, bu yöntemle, bu
başlıklarla istek gönderebilir miyim?" Basit istekler (`GET`, `HEAD`,
`POST` ve formların gönderebildiği üç içerik türü) sorulmadan gider:

```python
SIMPLE_METHODS = {"GET", "HEAD", "POST"}
SIMPLE_TYPES = {
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
}


def needs_preflight(method, content_type):
    return method not in SIMPLE_METHODS or content_type not in SIMPLE_TYPES


print(needs_preflight("POST", "text/plain"))
print(needs_preflight("POST", "application/json"))
print(needs_preflight("DELETE", "text/plain"))
```

```text
False
True
True
```

JSON gönderen `POST` ve `DELETE` önce sorulur. Bu ayrıntı CSRF için
önemlidir: bir form başka bir siteden `application/json` gönderemez,
ama `text/plain` ile `POST` gönderebilir. Sunucu yalnızca
`Content-Type: application/json` isteklerini kabul ederse, ön kontrolü
geçemeyen başka kökenlerin isteklerini de dolaylı olarak dışarıda bırakır.
Bu yine de CSRF jetonunun yerini tutmaz; ek bir katmandır.

<figure class="fig">
<div class="flow">
<span class="node">betik: fetch(api)</span>
<span class="arrow">→</span>
<span class="node">OPTIONS + Origin</span>
<span class="arrow">→</span>
<span class="node acc">sunucu izin verdi mi?</span>
<span class="arrow">→</span>
<span class="node ok">asıl istek</span>
</div>
<figcaption>Ön kontrol gereken istekte tarayıcı önce izin sorar; izin yoksa asıl istek hiç gönderilmez.</figcaption>
</figure>

## Güvenlik başlıkları

Sunucu her cevapla tarayıcıya "bu sayfayı nasıl koruyayım?" talimatları
da gönderebilir. Bir cevaptaki başlıkları denetleyen küçük bir fonksiyon:

```python
REQUIRED = [
    "content-security-policy",
    "strict-transport-security",
    "x-content-type-options",
    "referrer-policy",
    "x-frame-options",
]

response = {
    "Content-Type": "text/html; charset=utf-8",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
}

present = {name.lower() for name in response}
for name in REQUIRED:
    if name not in present:
        print("missing:", name)
```

```text
missing: content-security-policy
missing: referrer-policy
missing: x-frame-options
```

Beş başlıktan üçü eksik. Başlık adları büyük/küçük harfe duyarsızdır; bu
yüzden karşılaştırma küçük harfle yapıldı. Başlıkların ne yaptığı:

<figure class="fig">
<div class="anat">
<div class="anat-row"><span>Content-Security-Policy</span><span>Hangi kaynaklardan betik, stil ve resim yüklenebileceği (XSS bölümü).</span></div>
<div class="anat-row"><span>Strict-Transport-Security</span><span>Tarayıcı bu siteye bir süre yalnızca HTTPS ile bağlanır (HTTP ve HTTPS bölümü).</span></div>
<div class="anat-row"><span>X-Content-Type-Options: nosniff</span><span>Tarayıcı bildirilen türe uyar, içeriğe bakıp tür tahmin etmez.</span></div>
<div class="anat-row"><span>Referrer-Policy</span><span>Başka siteye geçerken adresin ne kadarının gönderileceği.</span></div>
<div class="anat-row"><span>X-Frame-Options / frame-ancestors</span><span>Sayfanın başka bir sitenin içinde çerçeveyle gösterilmesini engeller.</span></div>
</div>
<figcaption>Beş yaygın güvenlik başlığı ve görevleri.</figcaption>
</figure>

Çerçeve engeli **tıklama kaçırmaya** (clickjacking) karşıdır: saldırgan
sizin sayfanızı görünmez bir çerçevede kendi sayfasının üstüne koyar ve
kullanıcıyı bilmeden sizin düğmenize tıklatır. Bugün aynı iş CSP'nin
`frame-ancestors 'none'` yönergesiyle de yapılır; ikisini birlikte
göndermek eski tarayıcıları da kapsar.

Başlıklar uygulamanın kendi hatalarını düzeltmez: CSP, kaçışlama yapılmamış
bir şablonun yerini tutmaz; HSTS, HTTP'de açık kalan bir girişin. Hepsi
**ikinci katmandır**.

## Özet

- Köken = şema + alan adı + port; aynı köken politikası başka kökenden
  **okumayı** engeller.
- CORS ile izni sunucu verir; gelen `Origin`'i geri yazmak, özellikle
  `Allow-Credentials: true` ile, politikayı ortadan kaldırır.
- Kökenler tam eşitlikle bir izin listesinde denetlenir; `endswith` ve
  `null` tuzaktır. `Vary: Origin` unutulmaz.
- JSON gönderen ve basit olmayan istekler önce ön kontrolle sorulur.
- CSP, HSTS, `nosniff`, `Referrer-Policy` ve çerçeve engeli tarayıcıya
  ikinci bir savunma katmanı kurdurur.
