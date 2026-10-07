# Başlıklar ve Kimlik Doğrulama

Şimdiye kadar istediğin her şeyi aldın, çünkü sorduğun kapılar herkese
açıktı. Gerçek API'lerin çoğu ise kapıda **kim olduğunu** sorar: Bir
hava durumu servisi kaç istek attığını saymak, bir şirket API'si yalnızca
çalışanlara veri vermek, bir ödeme servisi işlemi kimin yaptığını bilmek
ister.

Bu bölümde iki şeyi öğreneceksin: isteğe **başlık** eklemek ve başlıklarla
**kimliğini kanıtlamak**. Bir de hayati bir alışkanlık: anahtarı **koda
yazmamak**.

## İki kelime: kimlik doğrulama ve yetki

Karıştırılan iki kavram:

- **Kimlik doğrulama** (authentication): "Sen kimsin?" Anahtarın, jetonun ya
  da şifren bunu kanıtlıyor.
- **Yetki** (authorization): "Bunu yapmaya iznin var mı?" Kim olduğun
  bilindikten sonra sorulan soru.

Bölüm 03'teki iki kod tam olarak bunlara karşılık geliyor:

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>401 Unauthorized</h4><p><b>Kimlik doğrulama</b> başarısız: "Seni tanımıyorum."<br>Anahtar yok, yanlış ya da süresi dolmuş.<br>Yapılacak: anahtarına ve başlığına bak.</p></div>
    <div class="dim"><h4>403 Forbidden</h4><p><b>Yetki</b> yok: "Seni tanıyorum ama buna iznin yok."<br>Anahtar geçerli, kapı kapalı.<br>Yapılacak: başka bir yetki gerekiyor.</p></div>
  </div>
  <figcaption>Adları yanıltıcı: 401'in adında "Unauthorized" (yetkisiz) geçiyor ama aslında "tanınmıyorsun" demek.</figcaption>
</figure>

## İsteğe başlık eklemek: `headers=`

requests'e başlıkları da bir sözlükle veriyorsun:

```python
import requests

BASE = "http://api.odyssey.test"
r = requests.get(BASE + "/books/1", headers={"Accept": "application/json"})
```

requests kendi başlıklarını (`User-Agent`, `Accept-Encoding`...) yine ekliyor;
senin verdiklerin onlara katılıyor ya da aynı adlıysa onların yerine geçiyor.

## Yöntem 1: API anahtarı

En basit kimlik: API'yi kaydolurken aldığın uzun bir metin, **API anahtarı**
(API key). Çoğu zaman özel bir başlıkta gönderilir. Alıştırma sunucusunun
`/stats` uç noktası `X-API-Key` başlığında anahtar istiyor:

```python
r = requests.get(BASE + "/stats")
print(r.status_code, r.json())
# 401 {'error': 'missing or invalid api key'}

r = requests.get(BASE + "/stats", headers={"X-API-Key": "demo-key-123"})
print(r.status_code, r.json())
# 200 {'books': 23, 'authors': 8, 'oldest': 1811, 'newest': 1986}
```

Anahtarsız istek `401` aldı: sunucu seni tanımıyor. Başlığı ekleyince `200`.

Başlığın adı API'den API'ye değişir: `X-API-Key`, `X-Api-Token`, `apikey`...
Bazı API'ler anahtarı sorgu parametresinde ister (`?api_key=...`). Hangisi
olduğunu belge söyler. Mümkünse başlık tercih edilir: adres sunucu
kayıtlarına, tarayıcı geçmişine yazılır; anahtar orada görünmesin.

## Yetki: anahtar geçerli ama yetmez

Aynı anahtarla yönetici raporunu isteyelim:

```python
r = requests.get(BASE + "/admin/report", headers={"X-API-Key": "demo-key-123"})
print(r.status_code, r.json())
# 403 {'error': 'this key cannot read admin reports'}
```

Bu kez `403`: sunucu seni tanıyor ama bu kapı sana kapalı. `401`'de
anahtarına bakarsın, `403`'te başka bir **yetki** gerekiyor; aynı isteği
tekrar göndermek bir şey değiştirmez.

## Yöntem 2: Bearer jeton

Çok yaygın ikinci yol, `Authorization` başlığında bir **jeton** (token)
göndermek:

```python
r = requests.get(BASE + "/me", headers={"Authorization": "Bearer letmein"})
print(r.status_code, r.json())
# 200 {'user': 'ada', 'role': 'editor'}
```

Başlığın değeri iki parça: `Bearer` kelimesi, bir boşluk ve jeton. "Bearer"
"taşıyıcı" demek: **bu jetonu taşıyan kişi yetkilidir**. Bu yüzden jeton bir
anahtar gibi saklanmalı; ele geçiren, senin yerine istek atabilir.

En sık hata `Bearer ` önekini unutmak:

```python
r = requests.get(BASE + "/me", headers={"Authorization": "letmein"})
print(r.status_code)   # 401
```

Jetonlar genellikle bir giriş isteğiyle alınır ve bir süre sonra **geçerliliğini
yitirir** (expire). Süresi dolan jetonla `401` alırsın; yeni bir jeton almak
gerekir. Bu akışın ayrıntısı (OAuth gibi) API'den API'ye değişir ve belgede
anlatılır.

## Yöntem 3: kullanıcı adı ve şifre (Basic)

Eski ama hâlâ görülen yol **Basic** kimlik doğrulama: kullanıcı adı ve şifre.
requests bunun için `auth=` parametresini sunuyor:

```python
r = requests.get(BASE + "/basic", auth=("reader", "pass123"))
print(r.status_code, r.json())             # 200 {'user': 'reader'}
print(r.request.headers["Authorization"])  # Basic cmVhZGVyOnBhc3MxMjM=
```

requests `reader:pass123` metnini **base64** ile kodlayıp `Authorization`
başlığına koyuyor. Base64 bir şifreleme **değil**; herkes geri çözebilir. Bu
yüzden Basic yalnızca `https` ile kullanılır.

## Anahtarı koda yazma

Şu satır bir gün sorun çıkarır:

```python
API_KEY = "sk_live_8f2a..."   # yapma
```

Kod GitHub'a, bir arkadaşına, bir ekran görüntüsüne gider; anahtar da onunla
gider. Sızan bir anahtarla başkası senin adına istek atar, faturan kabarır
ya da verin açığa çıkar. Ve bir kez commit'lenen anahtar, silsen bile geçmişte
kalır.

Doğru yol anahtarı **ortam değişkeninde** (environment variable) tutmak.
Ortam değişkeni, işletim sisteminin programa verdiği ad-değer çiftleri;
koddan ayrı duruyor:

```python
import os

key = os.environ.get("LIBRARY_KEY", "demo-key-123")
r = requests.get(BASE + "/stats", headers={"X-API-Key": key})
```

`os.environ.get(ad, varsayılan)` değişkeni okur; tanımlı değilse varsayılanı
verir. Alıştırmalarda varsayılan olarak alıştırma sunucusunun herkese açık
anahtarını kullanıyoruz; gerçek bir projede varsayılan **koymazsın**, anahtar
yoksa program açıkça durmalı.

Ortam değişkenini Windows'ta komut satırından tanımlamak:

```text
set LIBRARY_KEY=gercek-anahtarin
python program.py
```

Projelerde anahtarlar çoğu zaman `.env` adlı bir dosyada tutulur ve bu dosya
**asla** git'e eklenmez (`.gitignore`).

## Her istekte aynı başlık: `Session`

Her istekte aynı anahtarı yazmak hem uzun hem hataya açık. `requests.Session`
bir **oturum** açar: ona verdiğin başlıklar oturumdaki her isteğe eklenir.

```python
session = requests.Session()
session.headers.update({
    "Authorization": "Bearer letmein",
    "User-Agent": "odyssey-notes/1.0",
})

print(session.get(BASE + "/me").json())   # {'user': 'ada', 'role': 'editor'}
print(session.get(BASE + "/books/1").request.headers["User-Agent"])   # odyssey-notes/1.0
```

Oturumun bir faydası daha var: aynı sunucuya giden istekler aynı bağlantıyı
yeniden kullanıyor, bu da çok sayıda istekte işi hızlandırıyor.

## `User-Agent`: kendini tanıt

requests her isteğe `User-Agent: python-requests/2.34.2` gibi bir başlık
ekliyor. Bazı API'ler kimin istek attığını görmek için kendi adını
yazmanı ister: `User-Agent: odyssey-notes/1.0 (ada@example.com)`. Sorun
olduğunda sana ulaşabilsinler diye. Kibar bir alışkanlık.

## Özet

- **Kimlik doğrulama** "kimsin", **yetki** "iznin var mı". `401` tanınmıyorsun,
  `403` izin yok.
- Başlıklar `headers={...}` ile eklenir.
- **API anahtarı** genellikle bir başlıkta (`X-API-Key`); **Bearer jeton**
  `Authorization: Bearer <jeton>`; **Basic** `auth=(ad, şifre)`.
- Jetonu ve anahtarı taşıyan yetkilidir; onları sakla. Basic yalnızca
  `https` ile.
- Anahtarı koda yazma: `os.environ.get(...)` ile ortam değişkeninden oku,
  `.env` dosyasını git'e ekleme.
- `requests.Session()` başlıkları her isteğe ekler ve bağlantıyı yeniden
  kullanır.
