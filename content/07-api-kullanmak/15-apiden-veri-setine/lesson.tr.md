# API'den Veri Setine

Patika boyunca parçaları tek tek öğrendin: istek, parametreler, kimlik,
sayfalama, hatalar, hız sınırı, iç içe yanıtı düzleştirmek. Bu bölümde
hepsini bir araya getirip bir veri bilimcisinin gerçekten yaptığı işi
yapacağız: **bir API'den analiz edilebilir bir veri seti çıkarmak.**

Hedef: kütüphanenin bütün kitaplarını çekip `books.csv` adlı düzenli bir
tabloya dökmek; bunu güvenilir, tekrar çalıştırılabilir ve sunucuya saygılı
biçimde yapmak.

## Hattın adımları

Bu işe genellikle **veri hattı** (data pipeline) denir: veriyi kaynaktan
alıp temizleyip hedefe yazan, sırayla çalışan adımlar.

<figure class="fig">
  <div class="flow">
    <span class="node">1. Çek<br><small>sayfa, deneme</small></span><span class="arrow">→</span>
    <span class="node">2. Sakla<br><small>ham JSON</small></span><span class="arrow">→</span>
    <span class="node">3. Düzleştir<br><small>satır, tür</small></span><span class="arrow">→</span>
    <span class="node">4. Denetle<br><small>kopya, eksik</small></span><span class="arrow">→</span>
    <span class="node acc">5. Yaz<br><small>books.csv</small></span>
  </div>
  <figcaption>Her adım ayrı bir fonksiyon. Ham veri diske yazıldığı için sonraki adımları API'ye yeniden gitmeden tekrar tekrar deneyebilirsin.</figcaption>
</figure>

Her adımı ayrı bir fonksiyon yapmak işi kolaylaştırır: bir adım bozulunca
nerede olduğunu bilirsin, bir adımı değiştirmek ötekilere dokunmaz.

## 1. Çek: bütün sayfalar, güvenli istekle

Önceki bölümlerin bütün alışkanlıkları burada:

```python
import time
import requests

BASE = "http://api.odyssey.test"

def get_json(session, path, params=None, attempts=3):
    for attempt in range(attempts):
        try:
            r = session.get(BASE + path, params=params, timeout=10)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 1)))
                continue
            r.raise_for_status()
            return r.json()
        except (requests.Timeout, requests.ConnectionError):
            time.sleep(2 ** attempt)
    raise RuntimeError("giving up on " + path)

def fetch_all(session):
    books, page = [], 1
    while True:
        body = get_json(session, "/books", {"page": page, "per_page": 20})
        books.extend(body["data"])
        if page >= body["meta"]["pages"]:
            return books
        page += 1
```

- `timeout` her istekte (Bölüm 11).
- `429`'da `Retry-After` kadar bekle (Bölüm 12); bağlantı sorunlarında
  bekleyerek yeniden dene.
- `4xx` gelirse `raise_for_status()` durdurur: düzeltilmesi gereken bir şey
  var, sessizce geçme.
- Büyük sayfa (`per_page=20`): daha az istek (Bölüm 10).
- Bir `Session`: başlıklar bir kez, bağlantı yeniden kullanılıyor
  (Bölüm 08).

## 2. Sakla: ham yanıtı diske yaz

Veriyi çektikten sonra işlemeden önce **ham hâliyle** bir dosyaya yaz.
Buna **önbellek** (cache) diyebiliriz:

```python
import json
import os

CACHE = "books_raw.json"

def load_books(session):
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as handle:
            return json.load(handle)
    books = fetch_all(session)
    with open(CACHE, "w", encoding="utf-8") as handle:
        json.dump(books, handle, ensure_ascii=False)
    return books
```

Neden bu kadar önemli?

- **Temizlemeyi yüz kez deneyebilirsin**, API'ye bir kez gidersin. Düzleştirme
  kodunda bir hata bulunca yeniden çekmek gerekmez.
- **Hız sınırına takılmazsın.**
- **Ne aldığını kanıtlayabilirsin:** analizin hangi veriyle yapıldığı belli.

Önbelleği yenilemek istediğinde dosyayı silmen yeter.

## 3. Düzleştir ve türleri düzelt

Bölüm 05'teki tarif:

```python
def to_row(book):
    author = book.get("author") or {}
    return {
        "id": book["id"],
        "title": book["title"],
        "author": author.get("name", ""),
        "country": author.get("country", ""),
        "year": int(book["year"]),
        "price": float(book["price"]),
        "tags": "|".join(book.get("tags", [])),
    }

rows = [to_row(book) for book in books]
```

## 4. Denetle

Yazmadan önce birkaç basit soru, hatalı bir veri setini analiz etmekten
kurtarır:

```python
ids = [row["id"] for row in rows]
assert len(ids) == len(set(ids)), "duplicate ids"
assert len(rows) == expected_total, "some pages are missing"
```

- **Kopya kayıt var mı?** Sayfalama sırasında liste değişirse aynı kayıt iki
  kez gelebilir (Bölüm 10).
- **Sayı tutuyor mu?** `meta.total` ile topladığın kayıt sayısı aynı mı?
- **Boş ya da garip değer var mı?** Negatif fiyat, gelecekte bir yıl...

`assert koşul, mesaj` koşul yanlışsa programı mesajla durdurur. Veri
hattında "sessizce yanlış sonuç" en kötü sonuçtur; durmak ondan iyidir.

## 5. Yaz

```python
import csv

with open("books.csv", "w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
```

Bu dosya artık Excel'de açılır, pandas'a `pd.read_csv("books.csv")` ile
yüklenir, grafiği çizilir.

## Yalnızca yeniyi çekmek: artımlı güncelleme

Ertesi gün veri setini güncellemek istiyorsun. Her şeyi yeniden çekmek yerine
yalnızca **değişenleri** çekmek hem hızlı hem kibar. Birçok API buna izin
verir: "şu tarihten beri değişenleri ver". Alıştırma sunucusunda:

```python
r = requests.get(BASE + "/changes", params={"since": "2024-03-05"})
print([(b["id"], b["updated"]) for b in r.json()["data"]])
# [(6, '2024-03-05'), (10, '2024-03-08'), (13, '2024-03-10'),
#  (20, '2024-03-12'), (23, '2024-03-14')]
```

Elindeki veri setini kimliğe göre bir sözlükte tutup gelenleri üstüne
yazarsın: var olanlar güncellenir, yeniler eklenir. Son güncelleme tarihini
bir dosyada saklarsın; bir sonraki çalıştırmada oradan devam edersin. Buna
**artımlı** (incremental) güncelleme deniyor.

## Tekrar çalıştırılabilir olmak

İyi bir veri hattı **iki kez çalıştırıldığında aynı sonucu** verir ve yarıda
kalırsa baştan başlamak zorunda bırakmaz:

- Önbellek ve son güncelleme tarihi dosyada.
- Yazma işlemi dosyayı baştan yazıyor (eklemiyor): ikinci çalıştırma kopya
  satır üretmiyor.
- Hatalar açıkça raporlanıyor; yarım bir dosya "tamam" gibi görünmüyor.

## Özet

- Veri hattı: **çek → sakla → düzleştir → denetle → yaz**; her adım ayrı bir
  fonksiyon.
- Çekerken bütün alışkanlıklar: `Session`, `timeout`, yeniden deneme,
  `Retry-After`, büyük sayfa, `raise_for_status`.
- Ham yanıtı **önbelleğe** yaz: temizlemeyi tekrar tekrar dene, API'ye bir kez
  git.
- Yazmadan önce denetle: kopya kimlik, eksik sayfa, garip değer. `assert` ile
  açıkça dur.
- Güncellemeyi **artımlı** yap: yalnızca değişenleri çek, kimliğe göre
  birleştir.
- Hattın iki kez çalıştırılması aynı sonucu vermeli.
