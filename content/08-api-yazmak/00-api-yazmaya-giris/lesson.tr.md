# API Yazmaya Giriş

API 1'de masanın bir tarafındaydın: **istemci**. Bir adrese istek atıyor,
gelen JSON'u okuyor, durum koduna bakıyordun. Bu modülde masanın öbür
tarafına geçiyorsun: isteği **karşılayan** ve cevabı **üreten** programı,
yani **sunucuyu** yazacaksın.

İyi haber: API 1'de öğrendiğin her kavram burada da geçerli. Yöntem (`GET`,
`POST`), adres, durum kodu, JSON, başlık... Yalnızca bu sefer onları sen
okumuyorsun, sen veriyorsun.

## Sunucunun işi

Bir istek geldiğinde sunucu dört şey yapar:

<figure class="fig">
  <div class="flow">
    <span class="node">İstek<br><small>GET /books</small></span><span class="arrow">→</span>
    <span class="node">Dinle<br><small>uvicorn, port 8000</small></span><span class="arrow">→</span>
    <span class="node acc">Yönlendir<br><small>FastAPI: hangi işlev?</small></span><span class="arrow">→</span>
    <span class="node">Çalıştır<br><small>senin işlevin</small></span><span class="arrow">→</span>
    <span class="node ok">Cevapla<br><small>200 + JSON</small></span>
  </div>
  <figcaption>Bir isteğin sunucudaki yolu. Senin yazdığın yalnızca "Çalıştır" adımı; gerisini uvicorn ve FastAPI yapıyor.</figcaption>
</figure>

1. **Dinlemek:** bilgisayarın bir portunda (ör. 8000) gelen bağlantıları
   beklemek.
2. **Yönlendirmek:** isteğin yöntemine ve adresine bakıp hangi kodun
   çalışacağına karar vermek (`GET /books` → kitapları listeleyen kod).
3. **Çalıştırmak:** o kodu çalıştırmak; gerekiyorsa gelen veriyi okumak ve
   denetlemek.
4. **Cevaplamak:** sonucu JSON'a çevirip durum koduyla geri göndermek.

Bunların hepsini elle yazmak mümkün ama uzun ve hataya açık: gelen baytları
ayrıştırmak, adresi parçalara bölmek, JSON'u çözmek, hatalı veriye uygun
cevap vermek... API 1'de alıştırma sunucusu tam olarak bunu yapıyordu ve
her uç noktası için `if request.path == "/books" and request.method ==
"GET":` gibi satırlar gerekiyordu.

Bu tekrarlanan işleri üstlenen hazır kütüphaneye **çatı** (framework)
denir. Sen yalnızca "bu adrese bu istek gelince şunu döndür" diyorsun;
gerisini çatı yapıyor.

## FastAPI ve uvicorn: iki parça

Bu modülde iki araç kullanacağız:

| Araç | Ne yapar? |
|---|---|
| **FastAPI** | Uygulamayı tanımladığın çatı: hangi adres hangi işleve gidecek, gelen veri nasıl denetlenecek. |
| **uvicorn** | Uygulamayı çalıştıran sunucu programı: portu dinler, istekleri FastAPI'ye verir, cevapları geri yollar. |

Bir benzetme: FastAPI bir restoranın **menüsü ve mutfağı** (hangi sipariş
nasıl hazırlanır), uvicorn kapıdaki **garson** (siparişi alır, mutfağa
iletir, tabağı müşteriye götürür). İkisi de gerekli, ama işleri ayrı.

FastAPI'nin seçilme sebebi: Python'un **tip belirtimlerini** (`year: int`)
kullanıyor. Bir parametrenin tipini yazdığında FastAPI hem gelen veriyi
o tipe göre denetliyor hem de API'nin belgesini kendiliğinden yazıyor.
Python patikasında öğrendiğin tip belirtimleri burada iş görmeye başlıyor.

## İlk uygulama

Bütün bir API, beş satır kod:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, API"}
```

Satır satır:

- `from fastapi import FastAPI`: çatıyı içe aktar.
- `app = FastAPI()`: **uygulama nesnesini** oluştur. Bütün uç noktalar
  bunun üzerine kurulacak. Adı genellikle `app`; uvicorn da onu bu adla
  arayacak.
- `@app.get("/")`: hemen altındaki işlevi **`GET /`** isteğine bağla.
  Başındaki `@` işaretine **dekoratör** (süsleyici) denir: işlevin
  tanımının üstüne konan bir etiket gibi düşün. İşlevi değiştirmiyor,
  FastAPI'ye "bu adres gelince bu işlevi çağır" diye kaydediyor.
- `def home():`: o istek gelince çalışacak sıradan bir Python işlevi.
  Adının bir önemi yok (`home`, `root`, `index` olabilir); ama ne yaptığını
  anlatan bir ad seç, belgede de bu ad görünecek.
- `return {"message": "Hello, API"}`: bir sözlük döndür. FastAPI onu
  **kendiliğinden JSON'a** çevirip `200 OK` ile gönderiyor.

Başka bir adres eklemek için aynı kalıbı tekrarlarsın:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

## Çalıştırmak

Kendi bilgisayarında denemek için önce iki paketi kurarsın (Odyssey'de
ikisi de hazır):

```text
python -m pip install fastapi uvicorn
```

Sonra dosyanın (`main.py`) bulunduğu klasörde uvicorn'u başlatırsın:

```text
uvicorn main:app --reload
```

`main:app` "`main.py` dosyasındaki `app` nesnesi" demek. `--reload` dosyayı
her kaydettiğinde sunucuyu yeniden başlatıyor; geliştirirken çok
kullanışlı. Ekranda şunlar çıkıyor (ölçtük, kısalttık):

```text
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [23324]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Artık tarayıcıda `http://127.0.0.1:8000` adresini açabilir ya da API 1'deki
gibi `curl` ile istek atabilirsin:

```text
curl -i http://127.0.0.1:8000/
HTTP/1.1 200 OK
server: uvicorn
content-length: 24
content-type: application/json

{"message":"Hello, API"}
```

Durum kodunu, `content-type` başlığını ve JSON gövdesini **sen yazmadın**:
FastAPI, döndürdüğün sözlükten hepsini üretti. Olmayan bir adres
istendiğinde de kendiliğinden `404` veriyor:

```text
curl http://127.0.0.1:8000/nothing
{"detail":"Not Found"}
```

uvicorn her isteği kendi ekranına da yazıyor; API'nin ne aldığını oradan
izleyebilirsin:

```text
INFO:     127.0.0.1:57893 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:57895 - "GET /nothing HTTP/1.1" 404 Not Found
```

Durdurmak için terminalde `Ctrl+C`.

## `/docs`: hazır belge

API 1'de bir API'yi tanımak için belgesini okumuştun. FastAPI belgeyi senin
yerine yazıyor. Sunucu açıkken `http://127.0.0.1:8000/docs` adresine git:
**Swagger UI** sayfası, uç noktalarının listesini gösterir; her birini
"Try it out" düğmesiyle tarayıcıdan deneyebilirsin.

Sayfanın arkasında `/openapi.json` var: API'nin makinenin okuyacağı
tarifi. Tek uç noktalı uygulamamızda (kısalttık):

```json
{"openapi": "3.1.0",
 "info": {"title": "FastAPI", "version": "0.1.0"},
 "paths": {"/": {"get": {"summary": "Home", ...}}}}
```

İşlevin adı `home` olduğu için özet "Home" oldu. Postman gibi araçlar bu
dosyayı içe aktarıp bütün uç noktaları hazır hâle getirebiliyor.

## Odyssey'de nasıl çalışacağız?

Alıştırmalarda kodunu `main.py`'ye yazıyorsun. Üç yol var:

1. **Çalıştır** (Ctrl+Enter): Odyssey uygulamanı **sunucu açmadan**
   çağırıyor, alıştırmanın istediği istekleri sırayla atıyor ve cevapları
   denetliyor. Terminalde her isteği görürsün: `→ GET /  200`.
2. **İstek** sekmesi (sol panelde): kendi isteğini yazıp gönder (yöntem,
   adres, gövde), cevabı ve durum kodunu gör. Kaydedilmez, deneme sayılmaz.
3. **Sunucuyu başlat**: uygulaman bu bilgisayarda gerçekten açılır ve
   tarayıcıda `/docs` sayfası gelir. Kodu değiştirince durdurup yeniden
   başlatırsın.

Dosyanın sonuna `uvicorn.run(app)` yazarsan Odyssey onu çalıştırmaz
(denetim beklemeden geçer); kendi bilgisayarında ise o satır sunucuyu
açar:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)
```

## Özet

- İstemci istek atar, **sunucu** dinler, yönlendirir, çalıştırır, cevaplar.
- **FastAPI** uygulamayı tanımlar (`app = FastAPI()`), **uvicorn** onu
  çalıştırır (`uvicorn main:app --reload`).
- `@app.get("/yol")` altındaki işlevi o adrese bağlar; döndürülen sözlük
  JSON olur, durum kodu `200`.
- Olmayan adres `404`; belge `/docs` ve `/openapi.json` kendiliğinden hazır.
