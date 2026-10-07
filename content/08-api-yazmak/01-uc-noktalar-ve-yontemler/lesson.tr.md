# Uç Noktalar ve Yöntemler

İlk bölümde tek bir `GET` uç noktası yazdın. Gerçek bir API'de aynı adrese
farklı yöntemlerle gelinir: `GET /counter` sayacı **okur**, `POST /counter`
sayacı **artırır**. Bu bölümde yöntemleri, uygulamanın hafızasını ve
FastAPI'nin döndürdüğün değerleri nasıl JSON'a çevirdiğini görüyorsun.

## Yöntem başına bir dekoratör

API 1'de öğrendiğin her HTTP yönteminin FastAPI'de bir dekoratörü var:

| Yöntem | Dekoratör | Genellikle ne için? |
|---|---|---|
| `GET` | `@app.get("/yol")` | Okumak |
| `POST` | `@app.post("/yol")` | Yeni bir şey oluşturmak, bir işlem başlatmak |
| `PUT` | `@app.put("/yol")` | Bir kaydın tamamını değiştirmek |
| `PATCH` | `@app.patch("/yol")` | Bir kaydın bir kısmını değiştirmek |
| `DELETE` | `@app.delete("/yol")` | Silmek |

Aynı adrese farklı yöntemlerle ayrı işlevler bağlanabilir. FastAPI isteğin
**yöntemine ve adresine birlikte** bakıp doğru işlevi seçer:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>GET /counter</span><span><code>read_counter()</code> → sayacı okur</span></div>
    <div class="anat-row"><span>POST /counter</span><span><code>increase()</code> → sayacı artırır</span></div>
    <div class="anat-row"><span>DELETE /counter</span><span>işlev yok → <code>405 Method Not Allowed</code></span></div>
    <div class="anat-row"><span>GET /sayac</span><span>adres yok → <code>404 Not Found</code></span></div>
  </div>
  <figcaption>FastAPI yöntem ile adresi birlikte eşleştirir. Aynı adres, farklı yöntem: farklı işlev.</figcaption>
</figure>

## Uygulamanın hafızası

Bir sayaç yazalım: okunabilsin ve artırılabilsin.

```python
from fastapi import FastAPI

app = FastAPI()
state = {"count": 0}


@app.get("/counter")
def read_counter():
    return state


@app.post("/counter")
def increase():
    state["count"] += 1
    return state
```

`state` işlevlerin **dışında**, dosyanın en üstünde tanımlı: sunucu açık
olduğu sürece bellekte duruyor ve her istek aynı sözlüğü görüyor. İşlevin
içinde tanımlasaydık her istekte baştan `0` olurdu.

Sözlüğün içini değiştirmek (`state["count"] += 1`) işlevin içinden
doğrudan yapılabiliyor. Bu yüzden sayıyı düz bir değişken (`count = 0`)
yerine sözlükte tutuyoruz; düz değişkeni işlevin içinden değiştirmek ek
bir kural (`global`) istiyor.

Sırayla atılan istekler ve cevapları (ölçtük):

```text
GET  /counter   200  {"count":0}
POST /counter   200  {"count":1}
POST /counter   200  {"count":2}
GET  /counter   200  {"count":2}
```

**Dikkat:** bu hafıza geçici. Sunucu durunca (ya da `--reload` yeniden
başlatınca) sayaç `0`'a döner. Kalıcı veri için bir veritabanı gerekiyor;
onu Veritabanı bölümünde yapacağız.

## Yanlış yöntem: 405

Sayaç için bir `DELETE` yazmadık. Biri yine de gönderirse:

```text
DELETE /counter   405  {"detail":"Method Not Allowed"}
```

`404` değil `405`: adres **var**, ama bu yöntem izinli değil. API 1'de
istemci olarak bu iki kodu ayırt etmeyi öğrenmiştin; şimdi FastAPI onları
senin yerine doğru veriyor.

## Ne döndürürsen JSON olur

Uç nokta sözlük ya da liste dışında da değer döndürebilir; FastAPI hepsini
JSON'a çevirir (ölçtük):

| İşlevin döndürdüğü | Gelen gövde |
|---|---|
| `{"count": 2}` | `{"count":2}` |
| `["red", "green"]` | `["red","green"]` |
| `3.14159` | `3.14159` |
| `"Odyssey"` | `"Odyssey"` (tırnaklı: bir JSON metni) |
| `None` | `null` |

Hepsinde `content-type: application/json` ve `200`. Durum kodunu
değiştirmeyi Yanıt Modelleri ve Durum Kodları bölümünde göreceğiz.

## Sondaki eğik çizgi

`@app.get("/books")` yazdın ama istemci `/books/` istedi. FastAPI
`307 Temporary Redirect` ile istemciyi `/books` adresine yönlendiriyor
(ölçtük); tarayıcı ve `requests` yönlendirmeyi kendiliğinden izliyor. Yine
de adresleri tutarlı yaz: sonda eğik çizgi **olmadan** (`/books`,
`/books/42`).

## İyi adres, iyi yöntem

API 1'deki REST kuralları burada senin sorumluluğunda:

- Adres bir **şeyi** (kaynağı) anlatsın, yöntem **ne yapılacağını**:
  `POST /counter`, `POST /increase-counter` değil.
- Adreslerde küçük harf ve çoğul ad: `/books`, `/users`.
- `GET` hiçbir şeyi değiştirmesin. Tarayıcı ya da bir önbellek `GET`'i
  istediği kadar tekrar edebilir; sayacı `GET` ile artırsaydık sayfayı her
  yenileyen sayacı artırırdı.

## Özet

- Her yöntemin dekoratörü var: `get`, `post`, `put`, `patch`, `delete`.
  Aynı adrese farklı yöntemlerle farklı işlevler bağlanır.
- İşlevlerin dışında tanımlanan veri sunucu açık kaldıkça yaşar; sunucu
  durunca kaybolur.
- Adres var ama yöntem yoksa `405`, adres yoksa `404`.
- Döndürülen her değer JSON olur: sözlük, liste, sayı, metin, `None` →
  `null`.
- `GET` yalnızca okur; değiştiren işler başka yöntemlerle.
