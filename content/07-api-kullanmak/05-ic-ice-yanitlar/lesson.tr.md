# İç İçe Yanıtları Tabloya Dökmek

API'den veri çekmenin amacı çoğu zaman bir **tablo** elde etmek: her satırı
bir kayıt, her sütunu bir alan olan, Excel'de açılabilen, pandas'a
yüklenebilen, grafiği çizilebilen bir tablo.

Ama API'ler veriyi tablo olarak göndermiyor. Yanıt iç içe: kayıtlar bir
listenin içinde, listenin kendisi bir sözlüğün içinde, kayıtların içinde
yine sözlükler ve listeler. Bu bölümde bu ağacı **düz satırlara** çevirmeyi
öğreneceksin. Veri bilimcinin API ile yaptığı işin büyük kısmı tam olarak
bu.

## Tipik bir yanıt

Bir kitap API'sinin `/books` yanıtı:

```json
{
  "data": [
    {"id": 1, "title": "Emma", "price": "12.50",
     "author": {"name": "Austen", "country": "UK"}, "tags": ["classic", "novel"]},
    {"id": 2, "title": "Dune", "price": "9.99",
     "author": {"name": "Herbert"}, "tags": ["scifi"]},
    {"id": 3, "title": "Ulysses", "price": "15.00",
     "author": {"name": "Joyce", "country": "IE"}, "tags": []}
  ],
  "meta": {"page": 1, "per_page": 3, "total": 42}
}
```

Hedefimiz şu tablo:

```text
id  title    price  author_name  author_country  tags
1   Emma     12.5   Austen       UK              classic|novel
2   Dune     9.99   Herbert      unknown         scifi
3   Ulysses  15.0   Joyce        IE
```

Aradaki yolu beş adımda yürüyeceğiz.

<figure class="fig">
  <div class="flow">
    <span class="node">1. Zarf</span><span class="arrow">→</span>
    <span class="node">2. Sütunlar</span><span class="arrow">→</span>
    <span class="node">3. Düzleştir</span><span class="arrow">→</span>
    <span class="node">4. Listeler</span><span class="arrow">→</span>
    <span class="node acc">5. Türler</span>
  </div>
  <figcaption>İç içe bir yanıttan düz bir tabloya giden beş adım. Her yeni API'de aynı sırayla ilerlersin.</figcaption>
</figure>

## Adım 1: Zarfı aç

Yanıtın en dışındaki sözlüğe **zarf** (envelope) diyebiliriz. Kayıtlar
zarfın içinde bir anahtarda duruyor; burada `data`. Başka API'lerde `items`,
`results`, `records` ya da `books` olabilir. Hangisi olduğunu belgeden ya da
yanıta bakarak öğrenirsin.

```python
items = response["data"]
print(len(items))              # 3
print(response["meta"]["total"])  # 42
```

Zarfın geri kalanı da işe yarar: `meta` "toplam 42 kitap var, sen 1.
sayfadasın" diyor. Yani elindeki 3 kayıt, verinin tamamı değil. Sayfaların
hepsini çekmeyi Bölüm 10'da göreceğiz.

## Adım 2: Hangi sütunları istiyorsun?

Bir kayıtta onlarca alan olabilir. Tabloya hepsini dökmek yerine işine
yarayanları seç. Her kayıttan yeni, düz bir sözlük kuruyorsun:

```python
rows = []
for item in items:
    rows.append({"id": item["id"], "title": item["title"]})
```

`rows` artık **sözlüklerden oluşan bir liste**: her sözlük bir satır, her
anahtar bir sütun. Tablonun Python'daki en yaygın hâli bu.

## Adım 3: İç içe alanları düzleştir

`author` alanı kendisi bir sözlük. Tabloda bir hücreye sözlük koyamazsın;
içindeki değerleri ayrı sütunlara çıkarırsın. Sütun adı, yolu birleştirerek
kurulur: `author` + `name` → `author_name`.

```python
for item in items:
    author = item["author"]
    row = {
        "id": item["id"],
        "author_name": author["name"],
        "author_country": author.get("country", "unknown"),
    }
```

Herbert'in kaydında `country` yok. `author["country"]` burada `KeyError`
verirdi; `get` ile varsayılan bir değer koyuyoruz. Bir önceki bölümün
alışkanlığı burada çok işe yarıyor: **API'nin her alanı her kayıtta
göndereceğine güvenme.**

### Her derinlikte düzleştirmek

İç içelik birkaç kat olabilir (`author.address.city`). Her katı elle yazmak
yerine, iç içe her sözlüğe aynı işi yapan küçük bir fonksiyon yazılabilir:

```python
def flatten(obj, prefix=""):
    flat = {}
    for key, value in obj.items():
        name = prefix + key
        if isinstance(value, dict):
            flat.update(flatten(value, name + "_"))
        else:
            flat[name] = value
    return flat

print(flatten(items[0]))
# {'id': 1, 'title': 'Emma', 'price': '12.50', 'author_name': 'Austen',
#  'author_country': 'UK', 'tags': ['classic', 'novel']}
```

Fonksiyon bir sözlükle karşılaşınca **kendini** o sözlük için yeniden
çağırıyor ve adın önüne `author_` ekliyor. Bir fonksiyonun kendini
çağırmasına **özyineleme** (recursion) deniyor. `isinstance(value, dict)`
"bu değer bir sözlük mü?" diye soruyor. `update` bir sözlüğün içeriğini
ötekine ekliyor.

## Adım 4: Listeler için karar ver

`tags` bir liste. Tabloya koymanın iki yolu var ve hangisinin doğru olduğu
soruna bağlı:

**a) Tek hücrede birleştirmek.** Kayıt başına bir satır kalır:

```python
row["tags"] = "|".join(item["tags"])    # "classic|novel"
```

Ayraç olarak virgül yerine `|` seçmek, ileride CSV'ye yazarken karışıklığı
önler.

**b) Her öğe için ayrı satır açmak.** Bir kitabın iki etiketi varsa iki
satır olur:

```text
book_id  tag
1        classic
1        novel
2        scifi
```

Bu biçim "hangi etiket kaç kitapta var?" gibi soruları sayarak
cevaplamayı kolaylaştırır. Kitabın kendisini değil, kitap–etiket
**ilişkisini** tutan ayrı bir tablo gibi düşün. Etiketi olmayan Ulysses bu
tabloda hiç görünmez.

## Adım 5: Türleri düzelt

Bu API fiyatı metin olarak gönderiyor: `"12.50"`. Metinle toplama yapamazsın.
Satırı kurarken doğru türe çevir:

```python
row["price"] = float(item["price"])
```

API'lerde sık görülen tür sorunları:

- sayıların metin gelmesi (`"12.50"`, `"42"`),
- tarihlerin metin gelmesi (`"2024-03-01T09:00:00Z"`; Zaman Serileri
  patikası bunlarla çalışmayı anlatıyor),
- boş değer için farklı yazımlar (`null`, `""`, `"N/A"`).

## Tabloyu dosyaya yazmak: `csv`

Python'un hazır `csv` modülü sözlüklerden oluşan bir listeyi doğrudan CSV
dosyasına yazabiliyor:

```python
import csv

with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["id", "title", "price"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
```

- `fieldnames` sütunların sırasını belirliyor.
- `writeheader()` ilk satıra sütun adlarını yazıyor.
- `newline=""` Windows'ta satırlar arasında fazladan boş satır çıkmasını
  önlüyor.

## pandas biliyorsan: `json_normalize`

Veri Bilimi patikasını bitirdiysen, pandas bu işin çoğunu tek satırda
yapıyor:

```python
import pandas as pd

df = pd.json_normalize(response["data"])
print(df)
```

```text
   id    title  price              tags author.name author.country
0   1     Emma  12.50  [classic, novel]      Austen             UK
1   2     Dune   9.99           [scifi]     Herbert            NaN
2   3  Ulysses  15.00                []       Joyce             IE
```

İç içe sözlükleri noktalı sütun adlarıyla düzleştiriyor (`author.name`),
eksik değere `NaN` koyuyor. Ama listeyi (`tags`) olduğu gibi bırakıyor ve
fiyat hâlâ metin. Yani 4. ve 5. adımların kararlarını yine sen veriyorsun.
Elle yapmayı bilmek, aracın ne yaptığını ve neyi yapmadığını görmeni
sağlıyor.

## Özet

- API yanıtı bir ağaç; tablo düz satırlar ister.
- **1.** Zarfı aç: kayıt listesini bul (`data`, `items`, `results`...).
  `meta` gibi alanlar toplamı ve sayfayı söyler.
- **2.** İstediğin sütunları seç; her kayıttan yeni bir düz sözlük kur.
- **3.** İç içe sözlükleri yolu birleştirerek sütunlara aç
  (`author_name`); eksik alanlar için `get`.
- **4.** Listeler için karar ver: tek hücrede birleştir ya da her öğeye
  ayrı satır aç.
- **5.** Türleri düzelt: metin gelen sayılar `float`/`int`.
- `csv.DictWriter` sözlük listesini CSV'ye yazar; pandas'ta
  `json_normalize` düzleştirmenin çoğunu yapar ama kararları vermez.
