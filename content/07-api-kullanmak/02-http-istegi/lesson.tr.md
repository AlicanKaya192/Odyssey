# HTTP İsteği

Adresi kurmayı öğrendin. Ama adres tek başına bir istek değil; bir zarfın
üstündeki adres gibi. Zarfın içinde ne olduğu, nasıl açılacağı, kimden
geldiği de yazılmalı.

İstemci ile sunucu bu bilgileri **HTTP** (HyperText Transfer Protocol) adlı
ortak bir kurala göre yazıyor. **Protokol**, iki tarafın konuşurken uyduğu
kurallar demek: kim önce konuşur, ne sırayla ne söylenir. Tarayıcın da,
Python kodun da, bir sunucu da aynı HTTP kurallarıyla konuşuyor; bu yüzden
birbirlerini anlıyorlar.

Bu bölümde bir HTTP isteğinin içini açıp her parçasına bakacağız.

## Bir istek aslında düz bir metin

Bir hava durumu isteği yolda şöyle bir metin olarak gidiyor:

```text
GET /v1/weather?city=Istanbul HTTP/1.1
Host: api.example.com
Accept: application/json
User-Agent: odyssey-client/1.0

```

Gözünü korkutmasın; dört parçası var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>İstek satırı</span><span><code>GET /v1/weather?city=Istanbul HTTP/1.1</code>: yöntem, hedef, sürüm</span></div>
    <div class="anat-row"><span>Başlıklar</span><span><code>Host: ...</code>, <code>Accept: ...</code>: istek hakkında bilgiler, satır başına bir tane</span></div>
    <div class="anat-row"><span>Boş satır</span><span>Başlıkların bittiğini söyler</span></div>
    <div class="anat-row"><span>Gövde</span><span>Gönderilen veri; <code>GET</code> isteğinde yok</span></div>
  </div>
  <figcaption>Her HTTP isteği bu dört parçadan oluşur. Bu örnekte gövde boş: hava durumunu okumak için bir şey göndermek gerekmiyor.</figcaption>
</figure>

Şimdi parçalara tek tek bakalım.

## İstek satırı

İlk satır üç şey söylüyor, aralarında birer boşluk var:

```text
GET  /v1/weather?city=Istanbul  HTTP/1.1
│    │                          │
│    hedef: yol + sorgu dizesi  HTTP sürümü
yöntem
```

- **Yöntem** (method): ne yapılmak istendiği. Burada `GET`, "getir".
- **Hedef** (target): URL'nin yol ve sorgu kısmı. Şema ve ana makine burada
  yok; ana makine birazdan `Host` başlığında geliyor.
- **Sürüm:** `HTTP/1.1`. HTTP'nin 2 ve 3 sürümleri de var; yolda daha
  verimli gidiyorlar ama anlattıkları şey aynı. Bu patikada fark etmez.

## Yöntemler: ne yapmak istiyorsun?

HTTP'nin birkaç **yöntemi** var. Her biri sunucuya farklı bir iş söylüyor:

| Yöntem | Ne demek | Örnek | Gövde taşır mı? |
|---|---|---|---|
| `GET` | Getir, oku | `GET /books/42` | Hayır |
| `POST` | Yeni bir şey oluştur | `POST /books` | Evet |
| `PUT` | Tamamen değiştir | `PUT /books/42` | Evet |
| `PATCH` | Bir kısmını değiştir | `PATCH /books/42` | Evet |
| `DELETE` | Sil | `DELETE /books/42` | Genellikle hayır |

Aynı adres farklı yöntemle bambaşka bir iş yapıyor: `GET /books/42` kitabı
getirir, `DELETE /books/42` siler. **Adres neye dokunulacağını, yöntem ne
yapılacağını söylüyor.**

`PUT` ile `PATCH` farkı: kitabın yalnızca fiyatını değiştirmek
istiyorsan `PATCH` ile yalnızca fiyatı gönderirsin. `PUT` ise kaydın
**tamamını** yenisiyle değiştirir; göndermediğin alanlar silinmiş sayılabilir.

İki yöntemi daha adıyla tanı, yeter: `HEAD` (yalnızca başlıkları getir,
gövdeyi değil) ve `OPTIONS` (bu adreste hangi yöntemler kullanılabilir?).

## Güvenli ve tekrarlanabilir yöntemler

Yöntemlerin iki özelliği, ileride hata yönetiminde çok işine yarayacak:

- **Güvenli** (safe): sunucuda hiçbir şeyi değiştirmez. `GET`, `HEAD`,
  `OPTIONS`. İstediğin kadar gönderebilirsin.
- **Tekrarlanabilir** (idempotent): bir kez göndermekle on kez göndermek
  aynı sonucu bırakır. Güvenlilere ek olarak `PUT` ve `DELETE`. Kitabı on
  kez silmek, bir kez silmekle aynı: kitap yok.

`POST` ikisi de değil. "Yeni sipariş oluştur" isteğini iki kez gönderirsen
**iki sipariş** oluşur. Bu yüzden bağlantı koptuğunda `GET` isteğini
gönül rahatlığıyla yeniden gönderirsin; `POST`'u yeniden göndermeden önce
düşünürsün. Bunu Bölüm 11'de kullanacağız.

## Başlıklar: zarfın üstündeki bilgiler

İstek satırından sonraki satırlar **başlıklar** (headers). Her biri
`Ad: değer` biçiminde, bir satırda bir başlık:

```text
Host: api.example.com
Accept: application/json
User-Agent: odyssey-client/1.0
```

Başlıklar isteğin kendisi değil, istek **hakkında** bilgi. Sık göreceklerin:

| Başlık | Ne söyler |
|---|---|
| `Host` | Hangi ana makineye gidildiği (zorunlu) |
| `Accept` | Yanıtı hangi biçimde istediğin: `application/json` |
| `Content-Type` | Gönderdiğin gövdenin biçimi: `application/json` |
| `Content-Length` | Gövdenin kaç bayt olduğu |
| `Authorization` | Kimliğin: anahtar ya da jeton (Bölüm 08) |
| `User-Agent` | İsteği hangi programın gönderdiği |

İki kural:

- **Başlık adlarında büyük/küçük harf fark etmez.** `Content-Type`,
  `content-type` ve `CONTENT-TYPE` aynı başlık. Bu yüzden program içinde
  başlık adlarını küçük harfe çevirip öyle karşılaştırmak iyi bir
  alışkanlık.
- Başlığın **adı ile değeri** ilk `: ` (iki nokta ve boşluk) ile ayrılır.
  Değerin içinde de iki nokta olabilir (`Host: localhost:8000`); bu yüzden
  yalnızca **ilk** iki noktadan bölünür.

## Boş satır ve gövde

Başlıklar bir **boş satırla** biter. Boş satırdan sonra gelen her şey
**gövde** (body): sunucuya gönderdiğin veri.

`GET` isteğinde gövde yoktur; istediğin her şey adreste. Yeni bir kitap
eklerken (`POST`) ise kitabın bilgileri gövdede gider:

```text
POST /v1/books HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 37

{"title": "Emma", "author": "Austen"}
```

Burada iki başlık gövdeyi anlatıyor: `Content-Type` "gövde JSON biçiminde",
`Content-Length` "gövde 37 bayt" diyor. Sunucu bu sayıya bakarak gövdenin
nerede bittiğini anlıyor. (Sayıyı elle saymazsın; istek kütüphanesi senin
için hesaplar.)

`Content-Length` **bayt** sayar, harf değil. İngilizce harfler birer bayt,
ama `ş` ya da `ö` gibi harfler UTF-8 ile ikişer bayt tutar. Python'da bayt
sayısı `len(text.encode("utf-8"))` ile bulunur.

## Python'da bir isteği okumak

Gerçek işte isteği metin olarak elle yazmayacaksın; `requests` gibi bir
kütüphane senin için yazacak. Ama metnin nasıl kurulduğunu bilmek, hata
aldığında neyin yanlış gittiğini görmeni sağlıyor. Bir isteği parçalarına
ayırmak birkaç satır:

```python
raw = """GET /v1/weather?city=Istanbul HTTP/1.1
Host: api.example.com
Accept: application/json"""

lines = raw.split("\n")
method, target, version = lines[0].split(" ")

headers = {}
for line in lines[1:]:
    name, value = line.split(": ", 1)
    headers[name.lower()] = value

print(method)           # GET
print(target)           # /v1/weather?city=Istanbul
print(headers["host"])  # api.example.com
```

`split(": ", 1)` sondaki `1` sayesinde yalnızca **ilk** ayraçtan bölüyor;
değerin içindeki iki noktaya dokunmuyor. `name.lower()` başlık adlarını
küçük harfe çevirdiği için `headers["host"]` her yazılışta çalışıyor.

## Doğru yöntemi seçmek

Bir API belgesi her uç noktanın yöntemini söyler. Ama yöntemlerin anlamını
bilirsen belgeyi okumadan çoğunu tahmin edebilirsin:

| Yapmak istediğin | İstek |
|---|---|
| Bütün kitapları listelemek | `GET /books` |
| 42 numaralı kitabı görmek | `GET /books/42` |
| Yeni kitap eklemek | `POST /books` (gövdede kitap) |
| Kitabın fiyatını değiştirmek | `PATCH /books/42` (gövdede fiyat) |
| Kitabı bütünüyle yenilemek | `PUT /books/42` (gövdede bütün kitap) |
| Kitabı silmek | `DELETE /books/42` |

Dikkat et: yeni kitap eklerken adres `/books`, yani **liste**. Kitabın
numarasını henüz bilmiyorsun; sunucu yeni kayda numarayı kendisi verecek.

## Özet

- HTTP, istemci ile sunucunun ortak konuşma kuralı (protokol).
- Bir istek dört parça: **istek satırı** (yöntem, hedef, sürüm),
  **başlıklar**, **boş satır**, **gövde**.
- Yöntemler: `GET` getir, `POST` oluştur, `PUT` tamamen değiştir, `PATCH`
  kısmen değiştir, `DELETE` sil. Adres neye, yöntem ne yapılacağına karar
  verir.
- **Güvenli** yöntem hiçbir şeyi değiştirmez (`GET`). **Tekrarlanabilir**
  yöntemi tekrar göndermek sonucu değiştirmez (`GET`, `PUT`, `DELETE`).
  `POST` ikisi de değil.
- Başlıklar `Ad: değer`; adlarda büyük/küçük harf fark etmez.
  `Content-Type` gövdenin biçimini, `Content-Length` bayt sayısını söyler.
- `GET` isteğinde gövde yok; gönderilen veri `POST`/`PUT`/`PATCH` gövdesinde.
