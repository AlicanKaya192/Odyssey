# requests ile İlk İstek

Şimdiye kadar istekleri ve yanıtları kâğıt üstünde, metin olarak inceledin.
Bu bölümde ilk kez **gerçek bir istek** gönderiyorsun: Python kodun bir
sunucuya bağlanacak, HTTP isteğini yazacak, yanıtı bekleyip okuyacak.

Bunun için Python dünyasının en çok kullanılan kütüphanesini kullanacağız:
**requests**. Adının anlamı "istekler"; tek işi HTTP isteği göndermek ve
bunu olabildiğince kolay yapmak.

## Alıştırma sunucusu

Gerçek bir API'ye istek atmak internet, bazen hesap, bazen ücret ister ve
sonuç her gün değişir. Bu yüzden bu patikanın alıştırmaları Odyssey'in
**içinde çalışan bir alıştırma sunucusuna** istek atıyor:

```text
http://api.odyssey.test
```

Bu bir kütüphane API'si: kitaplar, yazarlar, süzme, sayfalama, kimlik
doğrulama... Gerçek bir sunucu gibi davranıyor; isteğin gerçekten bir
soketten gidiyor, durum kodları gerçekten geliyor. Tek farkı, isteğin
**bilgisayarından hiç çıkmaması**. `.test` uzantısı dünyada hiçbir siteye ait
değil; Odyssey bu adı kendi içindeki sunucuya yönlendiriyor.

Alıştırmayı çalıştırdığında terminalde sunucuya giden istekleri de
görürsün:

```text
Alıştırma sunucusuna giden istekler (1):
  → GET /books/1  200
```

## requests kurulumu

requests Python'la birlikte gelmiyor; ayrı bir paket. Kendi bilgisayarında
bir projede kullanmak için:

```text
python -m pip install requests
```

Odyssey'in alıştırma ortamında kurulu geliyor; burada bir şey yapman
gerekmiyor. Paket kurmayı Python patikasının "Paketler ve Ortamlar"
bölümünde görmüştün.

## İlk istek: `requests.get`

```python
import requests

response = requests.get("http://api.odyssey.test/books/1")
print(response.status_code)   # 200
```

Bu iki satırda olanlar, önceki bölümlerde parça parça öğrendiğin her şey:

<figure class="fig">
  <div class="flow">
    <span class="node">requests.get(...)</span><span class="arrow">→</span>
    <span class="node">HTTP isteği<br><small>GET /books/1</small></span><span class="arrow">→</span>
    <span class="node acc">Sunucu</span><span class="arrow">→</span>
    <span class="node">HTTP yanıtı<br><small>200 + JSON</small></span><span class="arrow">→</span>
    <span class="node">Response nesnesi</span>
  </div>
  <figcaption>İstek satırını, başlıkları ve yanıtın ayrıştırılmasını requests yapıyor; sana yalnızca adres ve sonuç kalıyor.</figcaption>
</figure>

`requests.get` bir `GET` isteği gönderiyor ve yanıt gelene kadar bekliyor.
Dönen değer bir **yanıt nesnesi** (`Response`): sunucunun söylediği her şey
onun içinde.

## Yanıt nesnesinin parçaları

```python
print(response.status_code)               # 200
print(response.ok)                        # True
print(response.headers["Content-Type"])   # application/json; charset=utf-8
print(response.url)                       # http://api.odyssey.test/books/1
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>status_code</code></span><span>Durum kodu: <code>200</code>, <code>404</code>...</span></div>
    <div class="anat-row"><span><code>ok</code></span><span>Kod 400'den küçükse <code>True</code></span></div>
    <div class="anat-row"><span><code>headers</code></span><span>Yanıt başlıkları; adlarda büyük/küçük harf fark etmez</span></div>
    <div class="anat-row"><span><code>text</code></span><span>Gövde, metin olarak</span></div>
    <div class="anat-row"><span><code>json()</code></span><span>Gövde, Python nesnesi olarak</span></div>
    <div class="anat-row"><span><code>url</code></span><span>İsteğin gittiği son adres</span></div>
    <div class="anat-row"><span><code>request</code></span><span>Bu yanıtı doğuran istek (yöntem, adres, başlıklar)</span></div>
  </div>
  <figcaption>Bölüm 03'te parça parça okuduğun yanıt, requests'te bir nesnenin alanları.</figcaption>
</figure>

`response.ok`, durum kodu 400'den küçükse `True`. Hızlı bir "sorun var mı?"
sorusu için kullanışlı, ama hangi sorun olduğunu söylemiyor; ayrıntı için
`status_code`'a bakarsın.

`response.headers` bir sözlük gibi çalışıyor ve Bölüm 02'de öğrendiğin gibi
**adlarda büyük/küçük harf fark etmiyor**: `response.headers["content-type"]`
de aynı değeri verir.

## Gövdeyi okumak: `text` ve `json()`

Gövdeyi iki biçimde alabilirsin:

- `response.text`: gövdenin **metin** hâli. Bir JSON metni de olabilir, düz
  bir yazı da.
- `response.json()`: gövdeyi JSON olarak ayrıştırıp **Python nesnesi**
  döndürür. Bölüm 04'teki `json.loads(response.text)` ile aynı iş.

```python
book = response.json()
print(book["title"], book["author"]["name"])   # Emma Austen
```

`json()` bir metot (sonunda parantez var), `text` bir özellik (parantez
yok). Karıştırmak sık yapılan bir hata.

Gövde JSON değilse `json()` hata verir:

```python
r = requests.get("http://api.odyssey.test/status")
print(r.headers["Content-Type"])   # text/plain; charset=utf-8
print(r.text)                      # ok
r.json()   # requests.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

Bu yüzden emin değilsen önce `Content-Type`'a bak: `application/json` ile
başlıyorsa `json()`, değilse `text`.

## Önce durum kodu, sonra gövde

Var olmayan bir kitabı isteyelim:

```python
r = requests.get("http://api.odyssey.test/books/99")
print(r.status_code, r.ok)   # 404 False
print(r.json())              # {'error': 'book not found', 'id': 99}
```

**requests, 404 geldi diye hata vermiyor.** Yanıt geldi; ne dediğine bakmak
sana kalmış. Durum koduna bakmadan `r.json()["title"]` yazan kod burada
`KeyError` ile düşer, ya da daha kötüsü hata mesajını veri sanıp devam
eder. Bölüm 03'ün kuralı burada da geçerli: **önce kod.**

```python
r = requests.get("http://api.odyssey.test/books/99")
if r.status_code == 200:
    print(r.json()["title"])
else:
    print("error", r.status_code)
```

## `raise_for_status`: hatayı hataya çevirmek

Her istekten sonra `if` yazmak yerine, requests'e "kod hata ise bir istisna
fırlat" diyebilirsin:

```python
r = requests.get("http://api.odyssey.test/books/99")
try:
    r.raise_for_status()
except requests.HTTPError as error:
    print("HTTPError:", error)
# HTTPError: 404 Client Error: Not Found for url: http://api.odyssey.test/books/99
```

`raise_for_status()` kod 400 ya da üstündeyse `requests.HTTPError` fırlatır,
değilse hiçbir şey yapmaz. Birçok programda isteğin hemen ardından
çağrılır: bir şey ters gittiyse program orada durur ve nedeni söyler.

## İsteğin kendisi de bir nesne

Hata ayıklarken "ben aslında ne gönderdim?" sorusu çok işe yarar. Yanıt,
onu doğuran isteği de taşıyor:

```python
print(response.request.method)    # GET
print(response.request.url)       # http://api.odyssey.test/books/1
print(response.request.headers)   # requests'in eklediği başlıklar
```

requests `User-Agent`, `Accept` gibi başlıkları kendisi ekliyor; Bölüm
02'de elle yazdığın isteğin tamamını senin yerine kuruyor.

## Sık yapılan hatalar

- **Şemayı unutmak.** `requests.get("api.odyssey.test/books")` hata verir:
  `MissingSchema`. Adres `http://` ya da `https://` ile başlamalı.
- **`json` ile `json()` karışıklığı.** `response.json` (parantezsiz) bir
  metodun kendisi; veriyi almak için `response.json()`.
- **Durum koduna bakmamak.** 404 ve 500 de "yanıt"; requests onları hata
  saymaz.
- **Gövdeyi iki kez ayrıştırmak.** `json.loads(response.json())` hata
  verir; `json()` zaten Python nesnesi döndürüyor.

## Özet

- `requests.get(adres)` bir `GET` isteği gönderir ve bir `Response` döndürür.
- Yanıtın parçaları: `status_code`, `ok`, `headers`, `text`, `json()`, `url`,
  `request`.
- `text` gövdenin metni, `json()` ayrıştırılmış Python nesnesi. JSON değilse
  `json()` hata verir; önce `Content-Type`'a bak.
- requests 4xx/5xx yanıtlarda hata vermez; ya durum koduna bakarsın ya da
  `raise_for_status()` ile hataya çevirirsin.
- Alıştırmalar `http://api.odyssey.test` adresindeki alıştırma sunucusuna
  gidiyor; istek bilgisayarından çıkmıyor.
