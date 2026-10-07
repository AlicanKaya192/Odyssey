# Sayfalama

Kütüphanede 23 kitap var ama `GET /books` yalnızca 5 tanesini döndürüyor.
Bu bir hata değil: API'lerin çoğu uzun listeleri **sayfalara** bölerek
gönderir. Bir arama motorunun sonuçları on on gösterdiği gibi.

Neden? Bir listede milyonlarca kayıt olabilir. Hepsini tek yanıtta göndermek
sunucuyu yorar, yanıtı dakikalarca sürdürür, belleği doldurur. Sayfalama
(pagination) bu yükü küçük, düzenli parçalara böler. Senin işin, ihtiyacın
olan bütün sayfaları sırayla istemek.

## Bir sayfanın içi

```python
import requests

BASE = "http://api.odyssey.test"
body = requests.get(BASE + "/books").json()
print(body["meta"])
# {'page': 1, 'per_page': 5, 'total': 23, 'pages': 5}
print(body["links"])
# {'next': '/books?page=2', 'prev': None}
```

Zarf (Bölüm 05) şimdi tam anlamını kazanıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>data</code></span><span>Bu sayfadaki kayıtlar (en fazla <code>per_page</code> tane)</span></div>
    <div class="anat-row"><span><code>meta.page</code></span><span>Şu anki sayfa: <code>1</code></span></div>
    <div class="anat-row"><span><code>meta.per_page</code></span><span>Sayfa başına kayıt: <code>5</code></span></div>
    <div class="anat-row"><span><code>meta.total</code></span><span>Bütün kayıtlar: <code>23</code></span></div>
    <div class="anat-row"><span><code>meta.pages</code></span><span>Sayfa sayısı: <code>5</code> (23 ÷ 5, yukarı yuvarlanmış)</span></div>
    <div class="anat-row"><span><code>links.next</code></span><span>Sonraki sayfanın adresi; son sayfada <code>None</code></span></div>
  </div>
  <figcaption>Her sayfa hem veriyi hem de "neredesin, nereye gidebilirsin" bilgisini taşıyor.</figcaption>
</figure>

- `page`: şu anki sayfa; `per_page`: sayfa başına kayıt.
- `total`: bütün kayıtların sayısı; `pages`: kaç sayfa olduğu.
- `links.next`: bir sonraki sayfanın adresi; son sayfadaysan `None`.

## Sayfalamanın dört biçimi

API'ler sayfalamayı dört yaygın biçimde yapar. Hepsinin fikri aynı: "nerede
kaldım?" bilgisini her istekte göndermek.

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Sayfa numarası</span><span><code>?page=2&amp;per_page=5</code>: "2. sayfayı ver"</span></div>
    <div class="anat-row"><span>Sonraki bağlantısı</span><span>Yanıttaki <code>next</code> adresine git: "sunucu söylesin"</span></div>
    <div class="anat-row"><span>Ofset + sınır</span><span><code>?offset=10&amp;limit=10</code>: "10 kayıt atla, 10 ver"</span></div>
    <div class="anat-row"><span>İmleç</span><span><code>?cursor=c4</code>: "kaldığım yerden devam et"</span></div>
  </div>
  <figcaption>Hangisini kullanacağını API seçer; belgede yazar. Dördünde de döngü aynı: iste, ekle, devam mı dur mu karar ver.</figcaption>
</figure>

## 1. Sayfa numarasıyla

En kolayı: `page=1`, `page=2`, ... `pages` kadar sayfa iste.

```python
books = []
page = 1
while True:
    body = requests.get(BASE + "/books", params={"page": page}).json()
    books.extend(body["data"])
    if page >= body["meta"]["pages"]:
        break
    page += 1

print(len(books), page)   # 23 5
```

`while True` + `break` kalıbı: sayfa sayısını ilk yanıtı almadan bilmediğin
için döngü kendi durma koşulunu içeride denetliyor. `extend`, bir listenin
öğelerini ötekinin sonuna ekliyor (`append` listeyi tek öğe olarak eklerdi).

Var olmayan bir sayfayı istersen hata değil, boş liste gelir:

```python
print(requests.get(BASE + "/books", params={"page": 9}).json()["data"])   # []
```

Bu yüzden `pages` bilgisini vermeyen API'lerde döngü **boş sayfa gelince**
durur: `if not body["data"]: break`.

## 2. "Sonraki" bağlantısıyla

API bir sonraki sayfanın adresini veriyorsa onu izlemek en güvenli yol:
sayfa numaralarını sen hesaplamıyorsun, sunucu söylüyor.

```python
books = []
url = BASE + "/books?per_page=10"
while url:
    body = requests.get(url).json()
    books.extend(body["data"])
    nxt = body["links"]["next"]
    url = BASE + nxt if nxt else None

print(len(books))   # 23
```

`while url:` adres `None` olunca duruyor. Sunucu `next` bağlantısını süzme ve
sıralama parametreleriyle birlikte veriyor (`/books?per_page=10&page=2`);
bunları kaybetmiyorsun.

Bazı API'ler bağlantıyı tam adres olarak verir (`https://api.../books?page=2`),
bazıları burada olduğu gibi yalnızca yol olarak. Tam adresse başına `BASE`
eklemezsin. Bazıları da bağlantıları gövdede değil `Link` başlığında gönderir;
requests onları `r.links` ile okunur hâle getiriyor.

## 3. Ofset ve sınırla

Veritabanı diline yakın bir biçim: "şu kadar kaydı atla, şu kadarını ver".

```python
items = []
offset = 0
while True:
    params = {"offset": offset, "limit": 10}
    body = requests.get(BASE + "/offset/books", params=params).json()
    items.extend(body["items"])
    offset += body["limit"]
    if offset >= body["total"]:
        break

print(len(items))   # 23
```

`offset=0` ilk 10 kayıt, `offset=10` sonraki 10, `offset=20` son 3.

## 4. İmleçle (cursor)

Büyük ve sürekli değişen listelerde (sosyal medya akışı gibi) sayfa
numaraları kayar: sen 2. sayfayı isterken başa yeni kayıt eklenirse bir
kaydı iki kez görürsün. **İmleç** (cursor) bunu önler: sunucu "kaldığın yer"
için opak bir işaret verir, sen onu geri gönderirsin.

```python
results = []
cursor = None
while True:
    params = {"cursor": cursor} if cursor else {}
    body = requests.get(BASE + "/cursor/books", params=params).json()
    results.extend(body["results"])
    cursor = body["next_cursor"]
    if cursor is None:
        break

print(len(results))   # 23
```

İmlecin içeriğini yorumlamaya çalışma (`c4` gibi görünse de); olduğu gibi
geri gönder. "Opak" tam olarak bu demek: içi senin için değil.

## Kaç kayıt isteyeceğin: `per_page`

```python
print(requests.get(BASE + "/books", params={"per_page": 100}).json()["meta"])
# {'page': 1, 'per_page': 20, 'total': 23, 'pages': 2}
```

100 istedin, 20 geldi: sunucunun bir **üst sınırı** var. Neredeyse her API'de
böyle bir sınır vardır ve belgede yazar. Büyük sayfa daha az istek demek,
ama sınırı aşamazsın; sonucu her zaman `meta`'dan oku.

## İyi bir sayfalama döngüsü

- **Bir durma koşulu olsun.** `next` yok, boş sayfa, ya da `pages`'e ulaşıldı.
  Durma koşulu yanlış olan döngü sonsuza kadar istek atar.
- **Bir güvenlik sınırı koy.** Hata durumunda sonsuz döngüye girmemek için:
  `for page in range(1, 1000):` gibi bir üst sınır.
- **Gereğinden fazla isteme.** İlk 10 kitap lazımsa 23'ünü çekme; yeterli
  kayıt toplanınca dur.
- **Süzmeyi sunucuya bırak.** `author=Austen` ile sayfalamak, bütün sayfaları
  çekip Python'da süzmekten çok daha az istek demek.

## Özet

- API'ler uzun listeleri sayfalara böler; hepsini almak için sayfaları sırayla
  istersin.
- `meta` (sayfa, sayfa boyu, toplam, sayfa sayısı) ve `links.next` nerede
  olduğunu söyler.
- Dört biçim: **sayfa numarası** (`page`), **sonraki bağlantısı** (`next`),
  **ofset + sınır** (`offset`, `limit`), **imleç** (`cursor`).
- Döngü `while True` + `break` ya da `while url:` ile kurulur; durma koşulu
  açık olmalı.
- `per_page`'in bir üst sınırı var; gelen sayıyı `meta`'dan oku.
- İmleci yorumlama, olduğu gibi geri gönder.
