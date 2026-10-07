# REST'i Okumak

Patikanın başından beri REST'in kurallarına göre tasarlanmış bir API
kullanıyorsun; çoğunu farkında olmadan öğrendin. Bu bölümde parçaları bir
araya getirip REST'i adıyla okuyacağız. Amaç iki yönlü:

- Yeni bir API'nin belgesini açtığında **tahmin edebilmek**: "kitapları
  silmek büyük olasılıkla `DELETE /books/<id>`".
- İyi ve kötü tasarımı **ayırt edebilmek**: API 2'de kendi API'ni yazarken
  doğru kararları vermek.

## REST nedir?

REST (Representational State Transfer), 2000 yılında bir doktora tezinde
tarif edilen bir **tasarım tarzı**. Bir kütüphane ya da protokol değil; HTTP'yi
nasıl kullanacağına dair bir dizi ilke. Bu ilkelere uyan API'ye "REST API"
ya da "RESTful" deniyor.

İlkelerin günlük hayattaki karşılığı beş fikre iniyor.

## 1. Her şey bir kaynak, her kaynağın bir adresi var

**Kaynak** (resource), API'nin üzerinde konuştuğu şey: bir kitap, bir yazar,
bir sipariş. Kaynakların iki biçimi var:

<figure class="fig">
  <div class="flow">
    <span class="node">/books<br><small>koleksiyon</small></span><span class="arrow">→</span>
    <span class="node acc">/books/42<br><small>öğe</small></span>
    <span class="arrow">·</span>
    <span class="node">/authors/6<br><small>öğe</small></span><span class="arrow">→</span>
    <span class="node">/authors/6/books<br><small>ilişkili koleksiyon</small></span>
  </div>
  <figcaption>Koleksiyonun adı çoğul; öğe koleksiyonun adresine kimlik eklenerek yazılır; ilişkiler iç içe.</figcaption>
</figure>

- **Koleksiyon** (collection): aynı türden kaynakların listesi. Adı çoğul:
  `/books`, `/authors`.
- **Öğe** (item): tek bir kaynak. Koleksiyonun adresi + kimlik:
  `/books/42`.

İlişkili kaynaklar **iç içe** yazılabilir: `/authors/6/books` "6 numaralı
yazarın kitapları".

```python
r = requests.get(BASE + "/authors/6/books")
print([b["title"] for b in r.json()["data"]])
# ['The Dispossessed', 'The Left Hand of Darkness',
#  'A Wizard of Earthsea', 'The Lathe of Heaven']
```

## 2. Adres isimdir, eylem yöntemdedir

REST'in en kolay tanınan kuralı: **adreste fiil olmaz.** Ne yapılacağını HTTP
yöntemi söyler.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Eylem adreste</h4><pre><code class="language-text">GET  /getBooks
POST /createBook
POST /books/42/delete
POST /updateBookPrice</code></pre></div>
    <div class="ok"><h4>Eylem yöntemde</h4><pre><code class="language-text">GET    /books
POST   /books
DELETE /books/42
PATCH  /books/42</code></pre></div>
  </div>
  <figcaption>Sağdaki dört istek iki adres kullanıyor; işi yöntem belirliyor.</figcaption>
</figure>

`/getBooks`, `/createBook`, `/books/42/delete` gibi adresler REST'e uymaz:
eylem adresin içine sızmış. REST'te aynı adres (`/books/42`) yöntemle farklı
işler yapar.

## 3. Yöntemler ve kodlar sözleşmedir

REST API'de her yöntemin anlamı ve başarı kodu bellidir; patika boyunca
gördüğün tablo aslında REST'in sözleşmesi:

| İstek | Anlam | Başarı |
|---|---|---|
| `GET /books` | Listele | `200` + liste |
| `GET /books/42` | Getir | `200` + kayıt; yoksa `404` |
| `POST /books` | Oluştur | `201` + `Location` |
| `PUT /books/42` | Tamamen değiştir | `200` (ya da `204`) |
| `PATCH /books/42` | Kısmen değiştir | `200` |
| `DELETE /books/42` | Sil | `204` |

Desteklenmeyen bir yöntem `405` alır ve `Allow` başlığı geçerli olanları
söyler:

```python
r = requests.put(BASE + "/books")
print(r.status_code, r.headers["Allow"])   # 405 GET, POST
```

Koleksiyon `GET` ve `POST` kabul ediyor; `PUT` öğe içindir.

## 4. Her istek kendi başına anlaşılır (durumsuz)

REST'te sunucu, istekler arasında **seni hatırlamaz**. Her istek, anlaşılması
için gereken her şeyi taşır: kimlik (jeton), parametreler, gövde. Bu yüzden
jetonu **her** istekte gönderiyorsun; "bir kez giriş yaptım, artık tanıyor"
diye bir şey yok. Buna **durumsuzluk** (statelessness) deniyor.

Faydası: herhangi bir istek, herhangi bir sunucu kopyasına gidebilir. API
büyüdükçe sunucu sayısını artırmak kolaylaşıyor.

## 5. Yanıtlar yol gösterebilir (bağlantılar)

İyi bir REST API yanıtlarında **bağlantılar** verir: bir sonraki sayfa, ilgili
kaynak, yapılabilecek işler. Alıştırma sunucusunun kök adresi:

```python
print(requests.get(BASE + "/").json())
# {'links': {'books': '/books', 'authors': '/authors', 'stats': '/stats'}}
```

İstemci adresleri ezberlemek yerine bağlantıları izleyebilir. Sayfalamadaki
`links.next` (Bölüm 10) bunun en yaygın örneği. Bu fikrin uzun bir adı var:
HATEOAS ("uygulama durumunun motoru olarak hipermedya"). Adını bilmen yeter;
pratikte "bağlantıları izle" demek.

## Sorgu parametreleri ve sürüm

Kalan iki alışkanlık önceki bölümlerden tanıdık:

- **Süzme, sıralama, sayfalama sorgu dizesinde:** `/books?author=Austen&sort=-year&page=2`
  (Bölüm 07, 10). Yeni bir adres açmazsın (`/books/by-author/Austen` değil).
- **Sürüm adreste ya da başlıkta:** `/v1/books`, `/v2/books`. Eski istemciler
  bozulmasın diye değişiklik yeni sürümde yapılır (Bölüm 01).

## İyi tasarım, kötü tasarım

| Kötü | Neden | REST karşılığı |
|---|---|---|
| `GET /getAllBooks` | Adreste fiil | `GET /books` |
| `POST /books/42/delete` | Eylem adreste, yöntem yanlış | `DELETE /books/42` |
| `GET /book?id=42` | Tekil ad, kimlik sorguda | `GET /books/42` |
| `POST /updatePrice` | Fiil + kaynak belirsiz | `PATCH /books/42` |
| `GET /books/delete/42` | `GET` bir şey siliyor! | `DELETE /books/42` |
| Hata için `200` + `{"error": ...}` | Kod yanlış bilgi veriyor | `404`, `422`... |

Sonuncu en sinsisi: hata olduğu hâlde `200` dönen bir API, durum koduna bakan
bütün istemcileri yanıltır. `GET` ile bir şeyi silmek ise daha tehlikeli:
tarayıcılar ve araçlar `GET`'i güvenli sayıp kendiliğinden tekrarlayabilir.

## REST her şey değil

REST en yaygın tarz ama tek değil. Adını duyacağın birkaç tanesi:

- **GraphQL:** tek bir adres; istemci hangi alanları istediğini bir sorgu
  diliyle yazar.
- **gRPC:** programlar arası hızlı iletişim için; JSON yerine ikili biçim.
- **Webhook:** tersine çalışır: sunucu bir şey olunca **senin** adresine
  istek atar.

Bu patikada ve API 2'de REST ile çalışıyoruz; ötekileri tanıman yeterli.

## Özet

- REST, HTTP'yi kullanmanın bir tasarım tarzı. Beş fikir: **kaynaklar ve
  adresleri**, **adreste isim / yöntemde eylem**, **yöntem ve kod sözleşmesi**,
  **durumsuzluk**, **bağlantılar**.
- Koleksiyon çoğul (`/books`), öğe koleksiyon + kimlik (`/books/42`), ilişki
  iç içe (`/authors/6/books`).
- Adreste fiil olmaz; aynı adres yöntemle farklı iş yapar. Desteklenmeyen
  yöntem `405` + `Allow`.
- Her istek kendi başına anlaşılır: jeton her istekte gider.
- Süzme ve sayfalama sorguda; sürüm adreste.
- Hata için `200` dönmek ve `GET` ile değişiklik yapmak REST'in en tehlikeli
  ihlalleri.
