# HTTP ve HTTPS

DNS adı adrese çevirdi, TCP bağlantısı kuruldu; şimdi tarayıcı ile sunucu
konuşmaya başlıyor. Web'in dili **HTTP**'dir (HyperText Transfer
Protocol). Modülün geri kalanındaki web saldırılarının hepsi (oturum
çalma, SQL enjeksiyonu, XSS, CSRF) HTTP mesajlarının içinde taşınır; bu
yüzden önce bir HTTP mesajını okumayı öğreniyoruz. Sonra aynı mesajı
yolda koruyan **HTTPS**'e geçiyoruz. Bütün mesajlar Python'da metin
olarak duruyor; hiçbir istek gönderilmiyor.

## Bir HTTP isteği

HTTP metin tabanlı bir protokoldür: istek, satırlardan oluşan düz bir
metindir. İlk satır **istek satırıdır** (yöntem, yol, sürüm); ardından
**başlıklar** (header) gelir; boş bir satırdan sonra varsa **gövde**
(body). Satırlar `\r\n` ile biter.

```python
raw = (
    "POST /login HTTP/1.1\r\n"
    "Host: shop.example.com\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Cookie: session=abc123\r\n"
    "\r\n"
    "user=ada&password=s3cret"
)

head, body = raw.split("\r\n\r\n", 1)
lines = head.split("\r\n")
method, path, version = lines[0].split(" ")
headers = dict(line.split(": ", 1) for line in lines[1:])
print(method, path, version)
for name, value in headers.items():
    print(f"{name}: {value}")
print("body:", body)
```

```text
POST /login HTTP/1.1
Host: shop.example.com
Content-Type: application/x-www-form-urlencoded
Cookie: session=abc123
body: user=ada&password=s3cret
```

Dört şeyi not et:

- **Yöntem** (method) ne yapılmak istendiğini söyler. `GET` bir şeyi
  okur, `POST` gönderir ya da oluşturur, `PUT`/`PATCH` değiştirir,
  `DELETE` siler. `GET` **güvenli** (safe) kabul edilir: sunucuda bir şey
  değiştirmemelidir. Bir şeyi silen `GET` isteği, CSRF bölümünde
  göreceğimiz gibi kolayca kötüye kullanılır.
- **`Host`** başlığı aynı sunucuda duran birçok siteden hangisinin
  istendiğini söyler.
- **`Cookie`** başlığı tarayıcının o site için sakladığı çerezleri taşır;
  oturum kimliği burada (Oturum ve Çerez bölümü).
- **Gövde** formdaki parola gibi verileri taşır. Bu istek şifresiz giderse
  hepsi yolda okunur (Ağ Saldırıları bölümündeki dinleme).

Her şey kullanıcının elindedir: yöntem, yol, başlıklar ve gövde tarayıcı
olmadan da istenildiği gibi yazılabilir. **Sunucu, istekteki hiçbir şeye
"tarayıcı böyle gönderdi" diye güvenemez.** Bu cümle web güvenliğinin
temelidir; Girdi Doğrulama bölümünde ona döneceğiz.

## Cevap ve durum kodları

Sunucunun cevabı da aynı biçimdedir; ilk satırında bir **durum kodu**
(status code) vardır. Kodun yüzler basamağı sınıfını söyler:

```python
def status_class(code):
    classes = {1: "info", 2: "success", 3: "redirect",
               4: "client error", 5: "server error"}
    return classes.get(code // 100, "invalid")


for code in [200, 301, 401, 403, 404, 500]:
    print(code, status_class(code))
```

```text
200 success
301 redirect
401 client error
403 client error
404 client error
500 server error
```

Güvenlikle ilgili üç kod sık karışır:

- **401 Unauthorized:** "Kim olduğunu bilmiyorum." Kimlik doğrulama yok ya
  da geçersiz.
- **403 Forbidden:** "Kim olduğunu biliyorum ama buna yetkin yok."
- **404 Not Found:** "Böyle bir şey yok."

Bir kaynağın var olduğunu bile gizlemek gerektiğinde (başkasının
faturası gibi) 403 yerine 404 döndürülür; yoksa saldırgan hangi
numaraların var olduğunu öğrenir. **500** ise sunucu hatasıdır ve cevapta
yığın dökümü, dosya yolu ya da sürüm bilgisi gibi iç ayrıntılar
**gösterilmez**; bunlar saldırgana harita verir.

## Adresi doğru okumak

Bir URL'nin parçaları **şema** (`https`), **ana bilgisayar** (host),
isteğe bağlı **port**, **yol** ve **sorgudur**. Python'ın `urllib.parse`
modülü adresi parçalara ayırır (yalnızca metni işler, ağa çıkmaz):

```python
from urllib.parse import urlsplit

for url in ["https://shop.example.com/cart?id=7",
            "http://shop.example.com:8080/login",
            "https://shop.example.com@203.0.113.66/login"]:
    parts = urlsplit(url)
    print(parts.scheme, parts.hostname, parts.port, parts.path)
```

```text
https shop.example.com None /cart
http shop.example.com 8080 /login
https 203.0.113.66 None /login
```

Üçüncü adrese dikkat: göze `shop.example.com` gibi görünüyor ama gerçek ana
bilgisayar `203.0.113.66`. URL'de `@` işaretinin solundaki kısım bir
kullanıcı adı olarak okunur ve adres orada bitmez. Oltalama bağlantıları
bu tür görünüş farklarından yararlanır. Bir adrese karar veren kod (izin
listesi, yönlendirme denetimi) adresi **göz kararı ya da metin aramasıyla
değil**, bir ayrıştırıcıyla parçalayıp `hostname`'e bakar. SSRF bölümünde
bunun önemi yeniden çıkacak.

## HTTPS: HTTP'nin TLS içinde taşınması

**HTTPS**, aynı HTTP mesajlarının **TLS** ile kurulmuş şifreli bir
bağlantı içinde taşınmasıdır (Kriptografi modülünün TLS El Sıkışması
bölümü). TLS üç şey sağlar:

<figure class="fig anat">
  <div class="anat-row"><span><b>Gizlilik</b></span><span>Yol, başlıklar, çerezler ve gövde yolda okunamaz.</span></div>
  <div class="anat-row"><span><b>Bütünlük</b></span><span>Mesaj yolda fark edilmeden değiştirilemez.</span></div>
  <div class="anat-row"><span><b>Sunucu kimliği</b></span><span>Sertifika, karşındakinin gerçekten o alan adının sahibi olduğunu gösterir; ortadaki adama karşı koruma budur.</span></div>
  <figcaption>HTTPS'in getirdikleri. Üçü de HTTP'nin kendisinde yoktur.</figcaption>
</figure>

HTTPS'in **getirmedikleri** de var ve sık karıştırılır:

<figure class="fig"><div class="versus">
  <div class="ok"><h4>HTTPS söyler</h4>"Bu bağlantı şifreli ve karşındaki sunucu, adres çubuğundaki alan adının sahibi."</div>
  <div class="no"><h4>HTTPS söylemez</h4>"Bu site güvenilir." Oltalama sitesi de kendi alan adı için sertifika alabilir. Sitenin kendi açıklarını (SQL enjeksiyonu, XSS) da kapatmaz. Gidilen alan adı (DNS ve TLS el sıkışmasında) yine görünür.</div>
</div><figcaption>Kilit simgesi bağlantıyı anlatır, sitenin niyetini değil.</figcaption></figure>

## HTTP'den HTTPS'e geçiş ve HSTS

Kullanıcı adres çubuğuna yalnızca `shop.example.com` yazarsa tarayıcı çoğu
zaman önce düz `http://` ile gider; sunucu `301` ile `https://`'e
yönlendirir. Ama o **ilk istek** şifresizdir: yoldaki bir saldırgan
yönlendirmeyi engelleyip kullanıcıyla düz HTTP üzerinden konuşmaya devam
edebilir. Buna **SSL soyma** (SSL stripping) denir.

Çözüm **HSTS**'dir (HTTP Strict Transport Security). Sunucu HTTPS
cevabına bir başlık ekler; tarayıcı bunu gördükten sonra o site için,
belirtilen süre boyunca, **düz HTTP'yi hiç denemez**:

```python
def parse_hsts(value):
    directives = {}
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        name, _, arg = part.partition("=")
        directives[name.strip().lower()] = arg.strip()
    return directives


h = parse_hsts("max-age=31536000; includeSubDomains")
print(h)
print(int(h["max-age"]) // 86400, "days")
```

```text
{'max-age': '31536000', 'includesubdomains': ''}
365 days
```

- **`max-age`** saniye cinsinden süredir; 31536000 saniye bir yıldır.
  Kısa süre (birkaç dakika) korumayı neredeyse işe yaramaz kılar.
- **`includeSubDomains`** kuralı bütün alt alanlara yayar.
- Tarayıcı başlığı ilk HTTPS ziyaretinde öğrenir; o ilk ziyaretten
  önceki açığı kapatmak için siteler tarayıcıların içine gömülü **önceden
  yükleme** (preload) listelerine de eklenir.

Yönlendirmenin kendisi de basit bir dönüşümdür; şema dışında her şey
korunur:

```python
from urllib.parse import urlsplit


def to_https(url):
    parts = urlsplit(url)
    if parts.scheme == "https":
        return url
    query = "?" + parts.query if parts.query else ""
    return "https://" + parts.netloc + parts.path + query


print(to_https("http://shop.example.com/cart?id=7"))
print(to_https("https://shop.example.com/"))
```

```text
https://shop.example.com/cart?id=7
https://shop.example.com/
```

## Karışık içerik ve fazla bilgi

- **Karışık içerik** (mixed content): HTTPS bir sayfa betiği ya da resmi
  düz `http://` ile yüklerse o parça yolda değiştirilebilir. Tarayıcılar
  betiklerde bunu engeller; sayfadaki her kaynak `https://` olmalıdır.
- **Fazla bilgi veren başlıklar:** `Server: ExampleServer/2.4.1` gibi tam
  sürüm bildiren başlıklar saldırgana hangi bilinen açığı deneyeceğini
  söyler. Gerekmeyen bilgi gönderilmez.

## Özet

- HTTP metin tabanlıdır: **istek satırı** (yöntem, yol, sürüm),
  **başlıklar**, boş satır, **gövde**.
- `GET` sunucuda bir şey değiştirmemelidir; durum değiştiren işler `POST`
  ve benzerleriyle yapılır.
- İsteğin her parçası kullanıcının elindedir; **sunucu istekteki hiçbir
  şeye körü körüne güvenmez.**
- **401** kimlik yok, **403** yetki yok, **404** yok; varlığı gizlemek için
  404. Hata cevabı iç ayrıntı göstermez.
- Adres kararları **ayrıştırıcıyla** verilir; `@` işaretinin solundaki
  kısım ana bilgisayar değildir.
- **HTTPS** = HTTP + TLS: gizlilik, bütünlük, sunucu kimliği. Sitenin
  güvenilir olduğunu söylemez.
- **HSTS** tarayıcıya düz HTTP'yi hiç denememesini söyler; `max-age` en az
  bir yıl, gerekirse `includeSubDomains` ve preload.
