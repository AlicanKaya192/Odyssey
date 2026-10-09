# API Araçları: Tarayıcı, curl, Postman, Swagger

Şimdiye kadar her isteği Python koduyla gönderdin. Ama bir API'yi tanırken
çoğu zaman kod yazmadan önce **denersin**: "bu adres ne döndürüyor?", "bu
başlığı vermezsem ne olur?". Bunun için yapılmış araçlar var ve iş hayatında
neredeyse her gün kullanılıyor.

Bu bölümde araçları tanıyacağız. Hepsinin işi aynı: HTTP isteği kurmak,
göndermek, yanıtı göstermek. Değişen, ne kadar kolay ve nerede
kullanıldıkları.

> Not: Alıştırma sunucusu (`api.odyssey.test`) yalnızca Odyssey'in alıştırma
> çalıştırıcısının içinde var; dış araçlar ona ulaşamaz. Araçları gerçek ve
> açık API'lerle denersin; bu bölümün alıştırmaları araçların ürettiği
> metinleri (curl komutu, OpenAPI belgesi, Postman koleksiyonu) Python'la
> okuyup çalıştırmayı öğretiyor.

## Tarayıcı: en hızlı GET

Bir `GET` adresini tarayıcının adres çubuğuna yazmak, bir API'yi denemenin
en hızlı yolu. Açık bir API'nin JSON yanıtı ekranda görünür; çoğu tarayıcı
JSON'u okunur biçimde gösterir.

Sınırları belli: tarayıcı adres çubuğundan yalnızca `GET` gönderir, başlık
ekleyemez. Kimlik isteyen ya da veri gönderen istekler için başka bir araç
gerekir.

### Geliştirici Araçları: Ağ sekmesi

Tarayıcıda **F12** ile açılan Geliştirici Araçları'nın **Ağ** (Network)
sekmesi, bir web sayfasının arka planda attığı bütün istekleri listeler.
Bir isteğe tıklayınca adresini, yöntemini, başlıklarını, durum kodunu ve
yanıtını görürsün.

Bu, veri bilimcisi için çok değerli bir alışkanlık: bir sitede gördüğün
verinin **hangi API'den geldiğini** buradan bulabilirsin. Çoğu modern sayfa
verisini zaten bir JSON API'sinden çekiyor. (O API'yi kendi programında
kullanmadan önce sitenin kullanım koşullarına bak.)

## curl: komut satırında istek

**curl**, komut satırından HTTP isteği gönderen küçük bir program.
Windows 10 ve 11'de hazır geliyor; Linux ve macOS'ta da var. Belgelerin
neredeyse hepsinde örnekler curl ile verilir, bu yüzden okumayı bilmek şart.

```text
curl https://api.example.com/books
curl -i https://api.example.com/books/1
curl --json @book.json -H "Authorization: Bearer abc" https://api.example.com/books
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>curl</code></span><span>Program</span></div>
    <div class="anat-row"><span><code>-X POST</code></span><span>Yöntem (verilmezse <code>GET</code>)</span></div>
    <div class="anat-row"><span><code>https://api.../books</code></span><span>Adres</span></div>
    <div class="anat-row"><span><code>-H "Ad: değer"</code></span><span>Bir başlık; birden çok kez yazılabilir</span></div>
    <div class="anat-row"><span><code>-d '...'</code> / <code>--json '...'</code></span><span>Gövde</span></div>
    <div class="anat-row"><span><code>-i</code></span><span>Yanıtın başlıklarını da göster</span></div>
  </div>
  <figcaption>Bir curl komutu, Bölüm 02'de parça parça gördüğün isteğin komut satırı hâli.</figcaption>
</figure>

Windows'ta PowerShell `curl` adını başka bir komuta ayırabiliyor; emin olmak
için `curl.exe` yaz.

### curl'den requests'e

Belgede gördüğün bir curl komutunu Python'a çevirmek çok sık yapılan bir iş.
Parçalar birebir eşleşiyor:

| curl | requests |
|---|---|
| `curl URL` | `requests.get(URL)` |
| `-X POST` | `requests.post(...)` ya da `requests.request("POST", ...)` |
| `-H "Ad: değer"` | `headers={"Ad": "değer"}` |
| `-d '{"a": 1}'` + JSON başlığı | `json={"a": 1}` |
| `-u kullanici:sifre` | `auth=("kullanici", "sifre")` |
| `-i` | `r.status_code`, `r.headers` |

Python'un hazır `shlex` modülü bir komutu, tırnakları doğru anlayarak
parçalarına ayırıyor:

```python
import shlex

cmd = 'curl -X POST "http://api.odyssey.test/books" -H "Authorization: Bearer letmein"'
print(shlex.split(cmd))
# ['curl', '-X', 'POST', 'http://api.odyssey.test/books',
#  '-H', 'Authorization: Bearer letmein']
```

Alıştırmada bu parçalardan bir istek kuracaksın.

## Swagger UI ve OpenAPI

Birçok API'nin belgesi **makine okunur** bir dosya olarak da yayımlanıyor:
**OpenAPI** belirtimi (eski adıyla Swagger). Bu JSON (ya da YAML) dosyası her
uç noktayı, parametrelerini, kimlik gereksinimini ve yanıtlarını anlatıyor:

```json
{"openapi": "3.1.0",
 "paths": {"/books": {"get": {"summary": "List books"},
                      "post": {"summary": "Add a book", "security": [{"bearer": []}]}}}}
```

**Swagger UI** bu dosyayı okuyup tarayıcıda etkileşimli bir sayfa çiziyor:
her uç noktanın yanında "Try it out" düğmesi, parametre kutuları, gönder
düğmesi ve yanıt. Belgeyi okurken aynı sayfada deniyorsun. **ReDoc** aynı
dosyadan daha okunaklı (ama denemesiz) bir belge sayfası üretiyor.

API Yazmak modülünde yazacağın FastAPI uygulamaları bu sayfayı **kendiliğinden** üretiyor:
uygulamayı çalıştırıp `/docs` adresine gidince Swagger UI açılıyor. Bu yüzden
Swagger UI'ı iyi tanımak, kendi API'ni denerken de işine yarayacak.

Alıştırma sunucusunun da küçük bir OpenAPI belgesi var: `GET /openapi.json`.

## Postman: kurumların standardı

**Postman**, API'lerle çalışmak için en yaygın masaüstü uygulama; şirketlerin
çoğunda ekipler onu kullanıyor. Temel kavramları:

- **İstek:** yöntem seç, adresi yaz, sekmelerden parametre, başlık, gövde ve
  kimlik ekle, **Send**'e bas. Yanıt kodu, süresi, başlıkları ve gövdesi
  alttaki panelde.
- **Koleksiyon** (collection): ilgili istekleri bir klasörde toplar
  ("Kütüphane API'si" altında listele, ekle, sil...). Ekiple paylaşılabilir.
- **Ortam ve değişkenler** (environment, variables): `{{base_url}}`,
  `{{token}}` gibi yer tutucular. Aynı koleksiyonu test ve canlı sunucuda
  yalnızca ortamı değiştirerek çalıştırırsın; anahtarı isteklerin içine
  yazmazsın.
- **Testler:** yanıt geldikten sonra çalışan küçük betikler ("kod 200 mü?").
- **Kod üretme:** bir isteği curl, Python requests ve başka dillere çeviren
  "Code" düğmesi. Postman'de çalışan isteği koda dökmenin en hızlı yolu.

Postman'in bulut eşitlemesi için hesap gerekiyor. Koleksiyonlar JSON olarak
dışa aktarılabiliyor; alıştırmada böyle bir koleksiyonu Python'la okuyup
çalıştıracaksın.

## Bruno: hesapsız ve çevrimdışı

**Bruno**, Postman'e benzeyen ama **açık kaynak**, hesap istemeyen ve
tamamen çevrimdışı çalışan bir uygulama. En önemli farkı: koleksiyonları düz
metin dosyaları olarak proje klasöründe tutuyor; bu dosyalar kodla birlikte
git'e girebiliyor. Hesap açmadan başlamak ya da isteklerini projeyle birlikte
saklamak istiyorsan iyi bir seçenek.

## Ötekiler: kısa tanıtım

- **Insomnia:** Postman'e benzer masaüstü uygulama.
- **Thunder Client:** VS Code içinde çalışan bir eklenti; editörden çıkmadan
  istek atarsın.
- **HTTPie:** curl'den daha okunaklı bir komut satırı aracı:
  `http GET api.example.com/books author==Austen`.

## Hangisini ne zaman?

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Bir GET'e hızlıca bakmak</span><span>Tarayıcı</span></div>
    <div class="anat-row"><span>Bir sitenin verisi nereden geliyor?</span><span>Geliştirici Araçları → Ağ</span></div>
    <div class="anat-row"><span>Belgedeki örneği denemek, betikte kullanmak</span><span>curl</span></div>
    <div class="anat-row"><span>Bir API'yi belgesinde denemek</span><span>Swagger UI (<code>/docs</code>)</span></div>
    <div class="anat-row"><span>Ekiple düzenli çalışmak, ortamlar, testler</span><span>Postman</span></div>
    <div class="anat-row"><span>Hesapsız, çevrimdışı, istekler git'te</span><span>Bruno</span></div>
    <div class="anat-row"><span>Tekrarlanan iş, veri çekme</span><span>Python + requests</span></div>
  </div>
  <figcaption>Araçlar denemek ve keşfetmek için; tekrarlanan iş için kod. İkisi birbirini tamamlıyor.</figcaption>
</figure>

## Özet

- Tarayıcı en hızlı `GET` denemesi; **F12 → Ağ** bir sayfanın kullandığı
  API'leri gösterir.
- **curl** komut satırının istek aracı; belgelerdeki örneklerin dili.
  `-X` yöntem, `-H` başlık, `-d` gövde, `-i` başlıklarla yanıt.
- **OpenAPI** API'nin makine okunur belgesi; **Swagger UI** ondan denenebilir
  bir sayfa çizer. FastAPI `/docs`'u kendiliğinden üretir.
- **Postman** kurumların standardı: koleksiyonlar, ortam değişkenleri,
  testler, kod üretme. **Bruno** hesapsız, çevrimdışı, git dostu.
- Araçta çalışan isteği koda çevirmek: curl ↔ requests eşleşmesi.
