# Sorgu Parametreleri ve Filtreleme

Bir API'den "bütün kitapları" istemek nadiren işine yarar. Çoğu zaman
istediğin şey daha dar: **Austen'ın** kitapları, **bilimkurgu** etiketli
olanlar, **en yeniden eskiye** sıralı, **ilk 3** tanesi. Bu ayrıntıları
sunucuya sorgu parametreleriyle söylersin.

Bölüm 01'de sorgu dizesini (`?author=Austen&sort=year`) tanıdın ve
`urlencode` ile elle kurdun. requests bu işi senin için yapıyor; sen yalnızca
bir sözlük veriyorsun.

## `params=`: sözlükten sorgu dizesine

```python
import requests

BASE = "http://api.odyssey.test"
r = requests.get(BASE + "/books", params={"author": "Austen"})
print(r.url)
# http://api.odyssey.test/books?author=Austen
print([b["title"] for b in r.json()["data"]])
# ['Emma', 'Persuasion', 'Pride and Prejudice', 'Sense and Sensibility']
```

`params` sözlüğünü requests sorgu dizesine çeviriyor ve adresin sonuna
ekliyor. `r.url` isteğin **gerçekten gittiği** adresi gösteriyor; parametreler
doğru gitti mi diye bakmanın en kolay yolu bu.

<figure class="fig">
  <div class="flow">
    <span class="node">params={"author": "Austen"}</span><span class="arrow">→ requests →</span>
    <span class="node acc">/books?author=Austen</span><span class="arrow">→</span>
    <span class="node">Sunucu süzüyor</span>
  </div>
  <figcaption>Sözlüğü sen veriyorsun; adresi requests kuruyor ve değerleri kodluyor. <code>r.url</code> sonucu gösterir.</figcaption>
</figure>

Neden adresi elle yazmıyoruz? `BASE + "/books?q=" + text` yazınca metindeki
boşluk ya da `&` adresi bozar (Bölüm 01). `params=` her değeri kendisi
kodluyor:

```python
r = requests.get(BASE + "/books", params={"q": "the lighthouse"})
print(r.url)   # http://api.odyssey.test/books?q=the+lighthouse
```

## Birden çok parametre

Sözlüğe istediğin kadar anahtar koyabilirsin. Hepsi `&` ile birleşir:

```python
r = requests.get(BASE + "/books", params={"tag": "scifi", "sort": "-year", "per_page": 3})
print(r.url)
# http://api.odyssey.test/books?tag=scifi&sort=-year&per_page=3
print([(b["title"], b["year"]) for b in r.json()["data"]])
# [('Fiasco', 1986), ('The Dispossessed', 1974), ('The Lathe of Heaven', 1971)]
```

Sayılar (`3`) kendiliğinden metne çevriliyor. Hangi parametrelerin olduğunu
ve ne anlama geldiklerini **API'nin belgesi** söyler; alıştırma sunucusunun
belgesi bir önceki bölümün notlarında.

## Parametrelerin üç işi

Sorgu parametreleri genellikle üç işten birini yapar:

**Süzme (filtering):** listeyi daraltır.

```text
?author=Austen            yazara göre
?tag=scifi                etikete göre
?year_min=1900&year_max=1930   aralığa göre
?q=dune                   başlıkta geçen kelimeye göre
```

**Sıralama (sorting):** sırayı belirler. Bu API'de `sort=year` küçükten
büyüğe, `sort=-year` büyükten küçüğe. Başka API'ler `order=desc` gibi ayrı bir
parametre kullanabilir; belgeye bakarsın.

**Sınırlama ve sayfa (limiting, paging):** kaç kayıt geleceğini söyler:
`per_page=3`, `page=2`. Sayfalamayı Bölüm 10'da ayrıntısıyla göreceğiz.

## Aynı ad birden çok kez: liste

İki etiketi birlikte istemek için değere bir **liste** verirsin:

```python
r = requests.get(BASE + "/books", params={"tag": ["scifi", "humor"]})
print(r.url)
# http://api.odyssey.test/books?tag=scifi&tag=humor
print([b["title"] for b in r.json()["data"]])
# ['The Cyberiad']
```

requests listeyi `tag=scifi&tag=humor` diye yazıyor. Bu API iki etiketi
"**ikisi de** olsun" diye okuyor. Başka bir API "**biri** olsun" diye ya da
`tags=scifi,humor` gibi virgüllü bir biçimle okuyabilir. Bir kez daha:
belgede yazar.

## `None` olan parametre gönderilmez

```python
r = requests.get(BASE + "/books", params={"author": "Orwell", "tag": None})
print(r.url)   # http://api.odyssey.test/books?author=Orwell
```

Değeri `None` olan anahtarı requests hiç yazmıyor. Bu, isteğe bağlı
parametreleri tek bir fonksiyonda toplamayı kolaylaştırıyor:

```python
def search(author=None, tag=None, sort=None):
    params = {"author": author, "tag": tag, "sort": sort}
    return requests.get(BASE + "/books", params=params).json()["data"]
```

Yalnızca verilen değerler adrese giriyor; ötekiler sessizce düşüyor.

## Sonuç yoksa: boş liste, hata değil

Süzme bir şey bulamazsa çoğu API **hata vermez**; boş bir liste döndürür:

```python
r = requests.get(BASE + "/books", params={"author": "nobody"})
print(r.status_code, r.json()["data"])   # 200 []
```

`200` ve boş `data` "istek doğru, eşleşen kayıt yok" demek. `404` ise "böyle
bir adres ya da kayıt yok". İkisini karıştırma: boş liste için kodun çökmemesi,
"bulunamadı" demesi gerekir.

## Sunucuda süzmek mi, Python'da mı?

Bütün kitapları çekip Python'da süzmek de mümkün:

```python
books = requests.get(BASE + "/books", params={"per_page": 20}).json()["data"]
austen = [b for b in books if b["author"]["name"] == "Austen"]
```

Ama gerçek API'lerde listede binlerce, milyonlarca kayıt olabilir. Hepsini
indirmek hem yavaş hem de sunucuya yük. **API süzmeyi destekliyorsa süzmeyi
sunucuya bırak**; yalnızca ihtiyacın olan kayıtlar gelsin. Python'da süzmek,
API'nin desteklemediği koşullar için kalsın.

## Yol mu, sorgu mu? (hatırlatma)

Bölüm 01'deki ayrım burada da geçerli:

- `/books/42` → **tek bir kitap** (yol parametresi).
- `/books?author=Austen` → **listeyi süz** (sorgu parametresi).

`/books?id=42` gibi bir biçim de görebilirsin, ama REST tarzında tek kaynağın
adresi yol olur. Bunu Bölüm 13'te tekrar konuşacağız.

## Özet

- `requests.get(url, params={...})` sözlüğü kodlanmış bir sorgu dizesine
  çevirip adrese ekler. Adresi elle yapıştırma.
- `r.url` isteğin gerçekten gittiği adresi gösterir; parametreleri denetlemek
  için ona bak.
- Parametreler süzer (`author`, `tag`, `q`), sıralar (`sort`) ve sınırlar
  (`per_page`, `page`). Hangisinin olduğunu belge söyler.
- Liste değer aynı adı tekrar eder (`tag=a&tag=b`); `None` değer gönderilmez.
- Eşleşme yoksa çoğu API `200` ve boş liste döndürür; bu bir hata değil.
- API süzebiliyorsa süzmeyi sunucuya bırak.
