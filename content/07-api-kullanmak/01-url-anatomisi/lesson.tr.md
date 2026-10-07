# Adresin Anatomisi: URL

Her istek bir **adrese** gidiyor. Tarayıcının üstündeki satıra yazdığın da,
bir programın API'ye gönderdiği de aynı türden bir adres: **URL** (Uniform
Resource Locator, "kaynağın yerini gösteren adres").

URL ilk bakışta tek parça bir metin gibi duruyor. Aslında altı parçası var
ve her parçanın ayrı bir görevi var. Bir API'yi kullanırken en sık yapacağın
iş bu parçaları doğru kurmak; yanlış kurulmuş bir adres, sunucuya hiç
ulaşmayan ya da yanlış şeyi isteyen bir istek demek.

## Bir URL'nin parçaları

Şu adresi parçalarına ayıralım:

```text
https://api.example.com:8443/v1/weather?city=Istanbul&units=metric#today
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Şema</span><span><code>https</code>: konuşmanın kuralı; <b>s</b> şifreli demek</span></div>
    <div class="anat-row"><span>Ana makine</span><span><code>api.example.com</code>: isteğin gittiği bilgisayar</span></div>
    <div class="anat-row"><span>Port</span><span><code>8443</code>: o bilgisayarda hangi programın dinlediği</span></div>
    <div class="anat-row"><span>Yol</span><span><code>/v1/weather</code>: hangi uç nokta</span></div>
    <div class="anat-row"><span>Sorgu dizesi</span><span><code>city=Istanbul&amp;units=metric</code>: ek bilgiler</span></div>
    <div class="anat-row"><span>Parça</span><span><code>today</code>: yalnızca tarayıcı için, sunucuya gitmez</span></div>
  </div>
  <figcaption>Altı parça, altı ayrı görev. Bir API isteğinde en çok yol ve sorgu dizesiyle uğraşırsın.</figcaption>
</figure>

Şimdi her parçaya tek tek bakalım.

## Şema: hangi dille konuşulacak

`https://` kısmı **şema** (scheme). İstemci ile sunucunun hangi kurallarla
konuşacağını söylüyor.

- `http`: düz konuşma. Yolda biri araya girerse her şeyi okuyabilir.
- `https`: aynı konuşma, ama **şifreli**. Sondaki **s** "secure" (güvenli).

API'lerde neredeyse her zaman `https` kullanılır, çünkü isteklerin içinde
çoğu zaman bir şifre ya da anahtar bulunur. Yalnızca kendi bilgisayarında
denediğin bir sunucuya `http` ile bağlanırsın.

## Ana makine: kime soruluyor

`api.example.com` **ana makine** (host): isteğin gideceği bilgisayarın adı.
İnternette her bilgisayarın sayılardan oluşan bir adresi var; bu okunabilir
ad, o sayıya çevriliyor.

Birçok şirket API'sini ayrı bir ada koyar: sitesi `example.com`, API'si
`api.example.com`. Baştaki `api.` bir **alt alan adı** (subdomain).

Özel bir ana makine adını şimdiden bil: **`localhost`** (ya da
`127.0.0.1`) **kendi bilgisayarın** demek. API 2'de yazacağın sunucu ve
bu patikada istek atacağın alıştırma sunucusu orada çalışacak.

## Port: binadaki daire numarası

`:8443` **port**. Ana makine bir apartmansa port daire numarası: aynı
bilgisayarda birden çok program istek bekleyebilir ve her biri kendi
numarasını dinler.

Çoğu adreste port yazılmaz, çünkü **varsayılan** bir değeri var:

- `http` için 80,
- `https` için 443.

Yazılmadığında istemci bu varsayılanı kullanır. Kendi bilgisayarında
denediğin sunucular genellikle `8000` gibi bir numarada çalışır:
`http://localhost:8000`.

## Yol: hangi kapı

`/v1/weather` **yol** (path). API'nin hangi uç noktasına gidildiğini söylüyor;
bir önceki bölümdeki **uç nokta** tam olarak bu.

Yolda sık göreceğin iki şey var:

- **Sürüm:** `/v1/`, `/v2/`. API değişince eski istemciler bozulmasın diye
  yeni sürüm yeni bir yolda açılır; eskisi bir süre daha çalışır.
- **Kimlik:** `/books/42`. Yolun son parçası belli bir kaynağı gösterir:
  42 numaralı kitap. Buna **yol parametresi** (path parameter) denir.

## Sorgu dizesi: ek bilgiler

`?city=Istanbul&units=metric` **sorgu dizesi** (query string). Sunucuya
"neyi, nasıl" istediğini ayrıntılandıran ek bilgiler:

- `?` sorgu dizesinin başladığını gösterir; adreste **bir kez** geçer.
- Her bilgi `ad=değer` biçiminde yazılır. Bunlara **sorgu parametresi**
  (query parameter) denir.
- Parametreler `&` ile birbirinden ayrılır.

Sıraları önemli değil: `?city=Istanbul&units=metric` ile
`?units=metric&city=Istanbul` aynı isteği anlatır. Aynı ad birden fazla kez
gelebilir: `?tag=sea&tag=museum` iki etiket demek.

Yol ile sorgu dizesi arasındaki fark şöyle düşünülebilir: **yol neyi**
istediğini (`/books`), **sorgu dizesi nasıl** istediğini (`?author=Austen&
sort=year`) söyler.

## Parça: yalnızca tarayıcı için

`#today` **parça** (fragment). Tarayıcıya "sayfanın şu kısmına kaydır" der.
**Sunucuya hiç gönderilmez.** API isteklerinde bir işe yaramaz; görürsen
bunu bil, yeter.

## Özel karakterler ve yüzde kodlaması

Sorgu dizesindeki bazı karakterlerin özel anlamı var: `?` başlatır, `&`
ayırır, `=` adı değerden ayırır. Peki değerin kendisinde bu karakterler
geçerse?

```text
?q=fish & chips
```

Sunucu bunu `q=fish ` ve anlamsız bir ` chips` olarak okur. Çözüm **yüzde
kodlaması** (percent-encoding): özel karakter `%` ve iki haneli bir kodla
yazılır.

| Karakter | Kodlanmış hâli |
|---|---|
| boşluk | `%20` (sorgu dizesinde `+` da olur) |
| `&` | `%26` |
| `/` | `%2F` |
| `ı` | `%C4%B1` |
| `ö` | `%C3%B6` |

Türkçe harfler de kodlanır: `Kadıköy` adreste `Kad%C4%B1k%C3%B6y` olarak
gider. Bunu elle yapmazsın; Python senin için yapıyor.

## Python'da URL: `urllib.parse`

Python'un hazır `urllib.parse` modülü URL'leri ayırmak ve kurmak için
gereken her şeyi veriyor. Kurulum gerekmiyor.

### Ayırmak: `urlparse`

```python
from urllib.parse import urlparse

url = "https://api.example.com:8443/v1/weather?city=Istanbul&units=metric#today"
parts = urlparse(url)
print(parts.scheme)    # https
print(parts.hostname)  # api.example.com
print(parts.port)      # 8443
print(parts.path)      # /v1/weather
print(parts.query)     # city=Istanbul&units=metric
print(parts.fragment)  # today
```

Adreste port yazılmamışsa `parts.port` değeri `None` olur; varsayılanı
(443) kendisi doldurmaz.

### Sorgu dizesini okumak: `parse_qs`

```python
from urllib.parse import parse_qs

params = parse_qs("city=Istanbul&units=metric&tag=sea&tag=museum")
print(params)
# {'city': ['Istanbul'], 'units': ['metric'], 'tag': ['sea', 'museum']}
```

Dikkat: **her değer bir liste.** Aynı ad birden çok kez gelebildiği için
`parse_qs` tek değeri de listeye koyuyor. Şehri almak için
`params["city"][0]` yazarsın.

### Sorgu dizesi kurmak: `urlencode`

```python
from urllib.parse import urlencode

query = urlencode({"city": "New York", "units": "metric", "days": 3})
print(query)   # city=New+York&units=metric&days=3
```

`urlencode` boşluğu `+` yapıyor, sayıyı metne çeviriyor, `&` ve `=`
karakterlerini kendisi kodluyor. Adresi kurmak için başına `?` eklersin:

```python
url = "https://api.example.com/v1/forecast?" + query
```

Aynı adı birden çok kez göndermek için listeyi `doseq=True` ile verirsin:
`urlencode({"tag": ["sea", "museum"]}, doseq=True)` → `tag=sea&tag=museum`.

### Tek bir değeri kodlamak: `quote`

```python
from urllib.parse import quote, unquote

print(quote("fish & chips"))        # fish%20%26%20chips
print(quote("Kadıköy"))             # Kad%C4%B1k%C3%B6y
print(unquote("Kad%C4%B1k%C3%B6y")) # Kadıköy
```

`quote` yolun içine bir değer koyarken işe yarar: `/cities/` + `quote(ad)`.

## Taban adres ve uç noktayı birleştirmek

API belgeleri genellikle bir **taban adres** (base URL) verir:
`https://api.example.com/v1`. Uç noktalar onun arkasına eklenir. En sık
hata, aradaki eğik çizgi:

```text
https://api.example.com/v1  +  weather   →  .../v1weather     (eksik)
https://api.example.com/v1/ +  /weather  →  .../v1//weather   (fazla)
```

Güvenli yol, iki taraftaki çizgiyi temizleyip tek çizgiyle birleştirmek:

```python
base = "https://api.example.com/v1/"
path = "/weather"
url = base.rstrip("/") + "/" + path.lstrip("/")
print(url)   # https://api.example.com/v1/weather
```

`rstrip("/")` sağdaki, `lstrip("/")` soldaki çizgileri siliyor. Alıştırmada
bunu bir fonksiyona dönüştüreceksin.

## Sık yapılan hatalar

- **Sorgu dizesini elle yapıştırmak.** `"?q=" + text` yazınca metindeki
  boşluk ve `&` adresi bozar. `urlencode` kullan.
- **İki kez `?` yazmak.** Adrese parametre eklerken, adreste zaten `?` var
  mı bak; ikinci parametreler `&` ile gelir.
- **`#`'nin sunucuya gittiğini sanmak.** Gitmez.
- **`parse_qs` değerini liste olduğunu unutup kullanmak.** `params["city"]`
  bir liste, `params["city"][0]` değer.

## Özet

- URL'nin parçaları: **şema** (`https`), **ana makine** (`api.example.com`),
  **port** (`:8443`, çoğu zaman yazılmaz), **yol** (`/v1/weather`), **sorgu
  dizesi** (`?city=Istanbul&units=metric`), **parça** (`#today`).
- Yol **neyi**, sorgu dizesi **nasıl** istediğini söyler. Parça sunucuya
  gitmez.
- `localhost` / `127.0.0.1` kendi bilgisayarın.
- Özel karakterler ve Türkçe harfler **yüzde kodlamasıyla** yazılır.
- `urlparse` ayırır, `parse_qs` sorguyu okur (değerler liste), `urlencode`
  sorgu kurar, `quote` tek değeri kodlar.
