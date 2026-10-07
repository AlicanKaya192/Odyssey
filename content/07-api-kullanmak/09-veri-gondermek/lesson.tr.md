# Veri Göndermek: POST, PUT, PATCH, DELETE

Şimdiye kadar yalnızca **okudun** (`GET`). Bir API'yle iş yapmak çoğu zaman
yazmayı da gerektirir: yeni bir kayıt eklemek, bir alanı düzeltmek, eskiyen
bir kaydı silmek. Bu bölümde Bölüm 02'de tanıdığın yöntemleri gerçekten
kullanacaksın.

Alıştırma sunucusunda kitap eklemek, değiştirmek ve silmek **jeton**
istiyor (Bölüm 08). Örneklerde başlığı bir kez tanımlıyoruz:

```python
import requests

BASE = "http://api.odyssey.test"
AUTH = {"Authorization": "Bearer letmein"}
```

Sunucu her çalıştırmada baştan başlıyor; eklediğin ve sildiğin kitaplar
bir sonraki çalıştırmada eski hâline dönüyor. Gönül rahatlığıyla dene.

## POST: yeni kayıt oluşturmak

Yeni bir kitap, kitap **listesine** (`/books`) `POST` ile gönderilir. Kitabın
bilgileri gövdede, JSON olarak gider:

```python
new = {"title": "Kindred", "author_id": 6, "year": 1979, "price": 11.5}
r = requests.post(BASE + "/books", json=new, headers=AUTH)

print(r.status_code, r.headers["Location"])   # 201 /books/24
book = r.json()
print(book["id"], book["title"], book["author"]["name"])   # 24 Kindred Le Guin
```

Üç şeye dikkat et:

- **`json=` parametresi.** requests sözlüğü JSON metnine çeviriyor
  (`json.dumps`), gövdeye koyuyor ve `Content-Type: application/json`
  başlığını kendisi ekliyor.
- **`201 Created`.** "Oluşturuldu" demek; `200` değil.
- **`Location` başlığı ve yanıt gövdesi.** Kitabın numarasını sen vermedin;
  sunucu verdi (`24`) ve yeni kaydın adresini `Location`'da söyledi. Gövde
  de kaydın son hâlini taşıyor: sunucunun eklediği alanlarla (`author`).

<figure class="fig">
  <div class="flow">
    <span class="node">POST /books<br><small>gövde: yeni kitap</small></span><span class="arrow">→</span>
    <span class="node acc">Sunucu<br><small>doğrular, numara verir</small></span><span class="arrow">→</span>
    <span class="node">201 Created<br><small>Location: /books/24</small></span>
  </div>
  <figcaption>Yeni kayıt listenin adresine gider; numarasını sunucu verir ve yeni adresi <code>Location</code> başlığında söyler.</figcaption>
</figure>

## `json=` ile `data=` aynı şey değil

```python
r = requests.post(BASE + "/books", data={"title": "Kindred", "price": 11.5}, headers=AUTH)
print(r.request.headers["Content-Type"])   # application/x-www-form-urlencoded
print(r.request.body)                      # title=Kindred&price=11.5
print(r.status_code, r.json())
# 422 {'error': 'validation', 'detail': 'the body must be a JSON object'}
```

`data=` sözlüğü **form verisi** olarak gönderir: web sayfalarındaki
formların biçimi (`ad=değer&...`), JSON değil. JSON bekleyen API onu
okuyamaz. **API JSON istiyorsa `json=` kullan.** Hangisini istediğini belge
söyler; günümüz API'lerinin çoğu JSON ister.

## Sunucu reddederse: 401 ve 422

Jetonsuz gönderirsen sunucu kim olduğunu bilmiyor:

```python
r = requests.post(BASE + "/books", json=new)
print(r.status_code, r.json())   # 401 {'error': 'missing or invalid token'}
```

Gövde kurallara uymuyorsa `422`:

```python
r = requests.post(BASE + "/books", json={"title": "", "price": 5}, headers=AUTH)
print(r.status_code, r.json())
# 422 {'error': 'validation', 'detail': 'title must be a non-empty string'}
```

Sunucunun gelen veriyi kurallara göre denetlemesine **doğrulama**
(validation) deniyor: başlık boş olamaz, fiyat pozitif olmalı. `detail`
alanı neyin yanlış olduğunu tam olarak söylüyor; hata aldığında ilk okuyacağın
yer.

## PATCH: bir kısmını değiştirmek

Dune'un yalnızca fiyatını değiştirelim:

```python
r = requests.patch(BASE + "/books/2", json={"price": 8.99}, headers=AUTH)
book = r.json()
print(r.status_code, book["title"], book["price"], book["year"])   # 200 Dune 8.99 1965
```

Yalnızca fiyatı gönderdik; başlık ve yıl olduğu gibi kaldı. Adres bu kez
**tek kaydın** adresi (`/books/2`).

## PUT: tamamen değiştirmek

`PUT` kaydı gönderdiğinle **bütünüyle değiştirir**:

```python
r = requests.put(BASE + "/books/4", json={"title": "Solaris", "price": 12.0}, headers=AUTH)
book = r.json()
print(r.status_code, book["title"], book["price"], book["year"], book["tags"])
# 200 Solaris 12.0 0 []
```

Yalnızca başlık ve fiyat gönderdik; yıl `0`, etiketler boş oldu. Göndermediğin
alanlar varsayılana döndü. Bölüm 02'deki uyarı gerçek oldu: **kısmi
değişiklik için `PATCH`; kaydın tamamını gönderiyorsan `PUT`.**

## DELETE: silmek

```python
r = requests.delete(BASE + "/books/9", headers=AUTH)
print(r.status_code, repr(r.text))   # 204 ''
print(requests.get(BASE + "/books/9").status_code)   # 404
```

`204 No Content`: "silindi, söylenecek bir şey yok". Gövde boş; `r.json()`
burada hata verir. Silindiğini doğrulamak için tekrar `GET` yapınca `404`.

Aynı kitabı bir daha silmeye çalışınca:

```python
print(requests.delete(BASE + "/books/9", headers=AUTH).status_code)   # 404
```

Kod farklı (`404`) ama **sonuç aynı**: kitap yok. `DELETE`'in tekrarlanabilir
olması bu demek; ikinci gönderim durumu değiştirmiyor.

## Yaz, sonra doğrula

Yazan bir isteğin ardından iki iyi alışkanlık:

1. **Durum kodunu denetle.** `201`, `200`, `204` beklediğin kodlar; başka bir
   şey geldiyse gövdedeki `detail`'i oku.
2. **Sonucu yanıttan ya da yeni bir `GET` ile doğrula.** Sunucu gönderdiğini
   değiştirmiş olabilir (yuvarlanan fiyat, eklenen alan).

```python
r = requests.post(BASE + "/books", json=new, headers=AUTH)
if r.status_code == 201:
    location = r.headers["Location"]
    saved = requests.get(BASE + location).json()
    print("saved:", saved["title"], saved["price"])
else:
    print("failed:", r.status_code, r.json().get("detail"))
```

## POST'u iki kez gönderme

Bölüm 02'deki uyarı burada somutlaşıyor: `POST` tekrarlanabilir değil.
Yukarıdaki kodu iki kez çalıştırırsan **iki** Kindred kaydı oluşur (24 ve
25). Bağlantı kesildi diye `POST`'u otomatik tekrarlayan kod, kopya kayıtlar
üretir. Bölüm 11'de yeniden denemeyi yazarken `POST`'u bu yüzden ayrı
tutacağız.

## Özet

- `POST /books` + `json=` yeni kayıt oluşturur → `201`, `Location` başlığı,
  gövdede kaydın son hâli.
- `json=` JSON gövde ve `Content-Type: application/json` gönderir; `data=`
  form verisi gönderir. API JSON istiyorsa `json=`.
- `PATCH /books/2` yalnızca gönderilen alanları değiştirir; `PUT` kaydın
  tamamını değiştirir, göndermediklerin kaybolabilir.
- `DELETE` → `204`, gövde boş. İkinci silme `404` verebilir ama sonuç aynı.
- `401` jeton eksik, `422` gövde kurallara uymuyor: `detail`'i oku.
- Yazdıktan sonra kodu denetle ve sonucu doğrula; `POST`'u otomatik tekrar
  etme.
