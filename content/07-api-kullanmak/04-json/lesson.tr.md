# JSON: API'lerin Dili

Bir API'nin yanıtındaki veri neredeyse her zaman aynı biçimde yazılıyor:

```json
{"city": "Istanbul", "temp": 18.5, "rain": false, "days": ["mon", "tue"]}
```

Bu biçimin adı **JSON** (JavaScript Object Notation). Adında JavaScript
geçiyor ama bugün her dil okuyup yazabiliyor. Sevilmesinin sebebi basit:
hem insan gözüyle okunabiliyor hem de programlar onu kolayca işliyor.

İyi haber: Python bildiğin için JSON'un çoğunu zaten biliyorsun. Bir
Python sözlüğüne çok benziyor. Bu bölümde benzerlikleri, **farkları** ve
Python'un hazır `json` modülünü öğreneceksin.

## JSON neden metin?

İstemci ile sunucu arasında yalnızca **metin** (aslında baytlar) gidip
gelebiliyor. Python sözlüğü bellekteki bir nesne; onu olduğu gibi kabloya
koyamazsın. Bu yüzden iki adım var:

<figure class="fig">
  <div class="flow">
    <span class="node">Python sözlüğü<br><small>sunucuda</small></span><span class="arrow">→ json.dumps →</span>
    <span class="node acc">JSON metni<br><small>yolda</small></span><span class="arrow">→ json.loads →</span>
    <span class="node">Python sözlüğü<br><small>sende</small></span>
  </div>
  <figcaption>Kablodan yalnızca metin geçiyor. Nesne metne çevrilip gönderiliyor, karşıda yeniden nesneye çevriliyor.</figcaption>
</figure>

- Bir nesneyi metne çevirmeye **serileştirme** (serialization) deniyor.
- Metni geri nesneye çevirmeye **ayrıştırma** (parsing) ya da
  **serileştirmeyi çözme** (deserialization) deniyor.

Sunucu verisini JSON metnine çevirip gönderiyor; sen gelen metni Python
nesnesine çevirip kullanıyorsun.

## JSON'un altı türü

JSON'da yalnızca altı tür değer var ve her birinin Python'da bir karşılığı
var:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Nesne (object)</span><span><code>{"city": "Izmir"}</code> → Python <code>dict</code></span></div>
    <div class="anat-row"><span>Dizi (array)</span><span><code>["mon", "tue"]</code> → Python <code>list</code></span></div>
    <div class="anat-row"><span>Metin (string)</span><span><code>"Izmir"</code> → Python <code>str</code></span></div>
    <div class="anat-row"><span>Sayı (number)</span><span><code>18</code>, <code>18.5</code> → Python <code>int</code>, <code>float</code></span></div>
    <div class="anat-row"><span>Mantıksal</span><span><code>true</code>, <code>false</code> → Python <code>True</code>, <code>False</code></span></div>
    <div class="anat-row"><span>Boş</span><span><code>null</code> → Python <code>None</code></span></div>
  </div>
  <figcaption>JSON'un bütün türleri. Nesne ve dizi iç içe girebiliyor; gerisi tek değer.</figcaption>
</figure>

Bu kadar. Tarih, küme, demet gibi türler JSON'da yok; onları nasıl
taşıyacağımızı birazdan göreceğiz.

## Python sözlüğünden farkları

İkisi çok benzediği için farklar kolayca gözden kaçıyor:

| | JSON | Python |
|---|---|---|
| Metin tırnağı | Yalnızca **çift** tırnak: `"city"` | Tek ya da çift: `'city'` |
| Doğru / yanlış | `true`, `false` (küçük harf) | `True`, `False` |
| Boş değer | `null` | `None` |
| Sözlük anahtarı | Yalnızca **metin** | Metin, sayı, demet... |
| Son virgül | **Yasak**: `[1, 2,]` hata | Serbest |
| Yorum | Yok | `# ...` |

En sık yapılan hata birinci satır: Python'un `print` ettiği sözlüğü JSON
sanmak. `{'city': 'Izmir'}` **geçerli JSON değil**, çünkü tırnaklar tek.

## `json.loads`: metinden Python'a

```python
import json

text = '{"city": "Istanbul", "temp": 18.5, "rain": false, "wind": null}'
data = json.loads(text)

print(data)          # {'city': 'Istanbul', 'temp': 18.5, 'rain': False, 'wind': None}
print(data["temp"])  # 18.5
print(type(data))    # <class 'dict'>
```

`loads` "load string" demek: metni yükle. Sonuç sıradan bir Python
sözlüğü; `false` artık `False`, `null` artık `None`. Bundan sonra sözlükle
nasıl çalışıyorsan öyle çalışırsın.

## `json.dumps`: Python'dan metne

```python
import json

book = {"title": "Emma", "tags": ["classic", "novel"], "price": 12.5}
text = json.dumps(book)
print(text)   # {"title": "Emma", "tags": ["classic", "novel"], "price": 12.5}
```

`dumps` "dump string": metne dök. Bir API'ye veri gönderirken (`POST`
gövdesi) bunu kullanırsın. Çıktı artık bir **metin**; içinden
`text["title"]` diye bir şey alamazsın.

### Okunur çıktı: `indent`

Uzun bir JSON tek satırda okunmuyor. `indent` girinti ekliyor:

```python
print(json.dumps(book, indent=2))
```

```json
{
  "title": "Emma",
  "tags": [
    "classic",
    "novel"
  ],
  "price": 12.5
}
```

Bir API'nin yanıtını incelerken bunu çok kullanacaksın.

### Türkçe harfler: `ensure_ascii`

```python
print(json.dumps({"city": "Kadıköy"}))
# {"city": "Kadıköy"}

print(json.dumps({"city": "Kadıköy"}, ensure_ascii=False))
# {"city": "Kadıköy"}
```

Varsayılan olarak `dumps` İngilizce olmayan harfleri `ı` gibi kodlarla
yazıyor. Bu yanlış değil; `loads` onu yine `ı` olarak okur. Ama dosyaya
yazarken ya da ekranda okurken `ensure_ascii=False` daha okunaklı.

## Dosyadan okumak ve dosyaya yazmak

Sonunda `s` olmayan `load` ve `dump` aynı işi bir **dosyayla** yapıyor:

```python
import json

with open("books.json", encoding="utf-8") as handle:
    books = json.load(handle)

with open("copy.json", "w", encoding="utf-8") as handle:
    json.dump(books, handle, indent=2, ensure_ascii=False)
```

Kısaca: **`s` varsa metin** (string), yoksa dosya.

## İç içe yapılar

API yanıtları çoğu zaman iç içedir: sözlüğün içinde liste, listenin içinde
sözlük.

```python
text = '''
{
  "city": "Izmir",
  "forecast": [
    {"day": "mon", "temp": 24},
    {"day": "tue", "temp": 21}
  ]
}
'''
data = json.loads(text)
print(data["forecast"][1]["temp"])   # 21
```

Okurken dıştan içe in: `data["forecast"]` bir liste, `[1]` ikinci gün (bir
sözlük), `["temp"]` o günün sıcaklığı. Kayboluyorsan yolun her adımında
`type(...)` ile ne elinde olduğuna bak.

## Eksik anahtar: `get`

Yanıttaki her kayıtta her alan olmayabilir. `data["wind"]` anahtar yoksa
`KeyError` verir; `get` ise varsayılan bir değer döndürür:

```python
day = {"day": "mon", "temp": 24}
print(day.get("wind"))        # None
print(day.get("wind", 0))     # 0
```

Gerçek API'lerle çalışırken `get` en çok kullanacağın şeylerden biri.

## Bozuk JSON: `JSONDecodeError`

Gelen metin geçerli JSON değilse `loads` hata verir:

```python
import json

try:
    json.loads("{'city': 'Izmir'}")
except json.JSONDecodeError as error:
    print("not JSON:", error)
# not JSON: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

Mesaj sorunun yerini de söylüyor: 1. satır 2. sütun, yani ilk tek tırnak.
Bir API bazen hata durumunda JSON yerine bir HTML sayfası döndürür; durum
koduna bakmadan `loads` çağıran kod tam burada düşer.

## JSON'da olmayan türler

`dumps` yalnızca altı türü bilir. Diğerlerini önce onlardan birine
çevirmen gerekir:

- **Demet** (`tuple`) listeye dönüşür: `(1, 2)` → `[1, 2]`. Geri okununca
  liste olarak gelir.
- **Küme** (`set`) hata verir: `Object of type set is not JSON
  serializable`. Önce `sorted(...)` ya da `list(...)` ile listeye çevir.
- **Tarih** de hata verir. Genellikle metin olarak taşınır:
  `"2024-03-01"` (Bölüm 01'deki ISO 8601 biçimi).
- **Sayı anahtar** metne dönüşür: `{1: "a"}` → `{"1": "a"}`. Geri okununca
  anahtar artık `"1"`, `1` değil.

## Özet

- JSON, API'lerin veri yazdığı metin biçimi. Altı türü var: nesne, dizi,
  metin, sayı, `true`/`false`, `null`.
- Python sözlüğünden farkları: yalnızca çift tırnak, küçük harfli
  `true`/`false`/`null`, anahtarlar yalnızca metin, sonda virgül yok.
- `json.loads(metin)` → Python nesnesi; `json.dumps(nesne)` → metin.
  `s`'siz `load`/`dump` dosyayla çalışır.
- `indent=2` okunur çıktı, `ensure_ascii=False` Türkçe harfleri olduğu
  gibi yazar.
- İç içe veride dıştan içe in; eksik olabilecek alanlar için `get`.
- Geçersiz metin `json.JSONDecodeError` verir; kümeler ve tarihler önce
  listeye ve metne çevrilir.
