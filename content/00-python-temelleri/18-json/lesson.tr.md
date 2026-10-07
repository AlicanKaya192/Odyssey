# JSON ile Çalışmak

Bir önceki bölümde dosyaya **metin** yazdın ve okudun. Ama programlarında
çoğu zaman metin değil, **yapılı veri** tutuyorsun: bir sözlük, sözlüklerin
listesi, içinde liste olan bir sözlük. Bunları dosyaya nasıl yazacaksın ve
sonra **aynı yapıyla** nasıl geri alacaksın?

Bu bölümün cevabı **JSON**. Ayar dosyaları, bir programın kaydettiği
veriler ve internetteki hemen her servisin verdiği cevaplar bu biçimde.
Python'da onunla çalışmak dört fonksiyondan ibaret.

## Önce sorun: sözlüğü düz metin olarak saklamak

Bir sözlüğü `str()` ile metne çevirip dosyaya yazmak ilk akla gelen yol:

```python
profile = {"name": "Ada", "languages": ["Python", "SQL"]}

with open("profile.txt", "w", encoding="utf-8") as file:
    file.write(str(profile))

with open("profile.txt", encoding="utf-8") as file:
    loaded = file.read()

print(loaded)
print(type(loaded))
```

```text
{'name': 'Ada', 'languages': ['Python', 'SQL']}
<class 'str'>
```

Ekranda sözlük gibi görünüyor ama değil: `loaded` bir **metin** (`str`).
İçinden ad almaya çalışınca:

```python
print(loaded["name"])
```

```text
TypeError: string indices must be integers, not 'str'
```

Metnin içinde sözlüğün **görüntüsü** var, sözlüğün kendisi yok. Geri
sözlüğe çevirmek için o metni harf harf çözmen gerekirdi. JSON tam bu işi
yapıyor: yapıyı metne çevirmenin ve metinden **aynı yapıyı** geri kurmanın
ortak bir kuralı.

## JSON nedir?

**JSON** (*JavaScript Object Notation*, "javascript nesne yazımı") veriyi
metin olarak yazmanın bir biçimi. Adında JavaScript geçse de her dil
okuyup yazabiliyor; bu yüzden programlar arasında veri taşımanın en yaygın
yolu.

Bir JSON metni Python sözlüğüne çok benziyor:

```json
{
  "name": "Ada",
  "age": 36,
  "languages": ["Python", "SQL"],
  "admin": true,
  "manager": null
}
```

Benzerlik büyük ama aynı değil. Farklar küçük, önemli:

<figure class="fig">
  <div class="versus">
    <div><h4>Python sözlüğü</h4>
<pre><code>{'name': 'Ada',
 'admin': True,
 'manager': None}</code></pre>
    </div>
    <div class="ok"><h4>JSON metni</h4>
<pre><code class="language-text">{"name": "Ada",
 "admin": true,
 "manager": null}</code></pre>
    </div>
  </div>
  <figcaption>JSON'da metinler yalnızca çift tırnakla yazılıyor; <code>True</code> yerine <code>true</code>, <code>None</code> yerine <code>null</code>.</figcaption>
</figure>

JSON'daki her parçanın Python'da bir karşılığı var:

| JSON | Python | Örnek |
|---|---|---|
| nesne `{ }` | `dict` | `{"a": 1}` |
| dizi `[ ]` | `list` | `[1, 2, 3]` |
| metin `"..."` | `str` | `"Ada"` |
| sayı | `int` ya da `float` | `36`, `3.5` |
| `true` / `false` | `True` / `False` | |
| `null` | `None` | |

## Metinden Python'a: `json.loads`

`json` Python'la birlikte gelen bir modül; kurmana gerek yok, `import`
etmen yeterli. `json.loads` bir JSON **metnini** alıp Python yapısına
çeviriyor:

```python
import json

text = '{"name": "Ada", "age": 36, "admin": true, "manager": null}'
data = json.loads(text)

print(data)
print(type(data))
print(data["age"] + 1)
```

```text
{'name': 'Ada', 'age': 36, 'admin': True, 'manager': None}
<class 'dict'>
37
```

Bu sefer gerçek bir sözlük geldi: `data["age"]` bir sayı ve üstüne 1
eklenebiliyor. `true` kendiliğinden `True`, `null` da `None` oldu.

JSON metnini tek tırnak içine yazdığımıza dikkat et: metnin **içinde** çift
tırnak var, dışını tek tırnakla sarmak en kolayı.

## Python'dan metne: `json.dumps`

Ters yön `json.dumps`: bir Python yapısını JSON metnine çeviriyor.

```python
profile = {
    "name": "Ada",
    "city": "London",
    "languages": ["Python", "SQL"],
    "active": True,
}

text = json.dumps(profile)
print(text)
print(type(text))
```

```text
{"name": "Ada", "city": "London", "languages": ["Python", "SQL"], "active": true}
<class 'str'>
```

Tırnaklar çift oldu, `True` da `true`. Sonuç bir metin; dosyaya yazılabilir,
internetten gönderilebilir.

Tek satır insan için okunaksız. `indent=2` her düzeyi iki boşluk içeri
alarak yazıyor:

```python
print(json.dumps(profile, indent=2))
```

```text
{
  "name": "Ada",
  "city": "London",
  "languages": [
    "Python",
    "SQL"
  ],
  "active": true
}
```

Bir ayrıntı daha: JSON varsayılan olarak Türkçe harfleri kaçış dizisiyle
yazıyor. `ensure_ascii=False` onları olduğu gibi bırakıyor:

```python
city = {"city": "İzmir"}
print(json.dumps(city))
print(json.dumps(city, ensure_ascii=False))
```

```text
{"city": "\u0130zmir"}
{"city": "İzmir"}
```

İkisi de geçerli JSON ve geri okununca ikisi de `"İzmir"` oluyor; fark
yalnızca dosyayı açıp bakan insan için.

<figure class="fig">
  <div class="flow">
    <span class="node">Python<br>sözlük, liste</span><span class="arrow">→</span>
    <span class="node acc"><code>json.dumps</code><br>metne çevir</span><span class="arrow">→</span>
    <span class="node">JSON metni<br>dosya, internet</span><span class="arrow">→</span>
    <span class="node acc"><code>json.loads</code><br>geri çevir</span><span class="arrow">→</span>
    <span class="node ok">aynı yapı</span>
  </div>
  <figcaption>Gidiş <code>dumps</code>, dönüş <code>loads</code>. Aradaki metin her dilin okuyabildiği ortak biçim.</figcaption>
</figure>

## Dosyaya yazmak ve dosyadan okumak: `json.dump` ve `json.load`

Dosyayla çalışırken metni aradan çıkaran iki kardeş fonksiyon var. Sonlarında
`s` yok:

```python
with open("profile.json", "w", encoding="utf-8") as file:
    json.dump(profile, file, indent=2)
```

Dosyanın içi:

```text
{
  "name": "Ada",
  "city": "London",
  "languages": [
    "Python",
    "SQL"
  ],
  "active": true
}
```

Geri okumak:

```python
with open("profile.json", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded["languages"][1])
print(loaded == profile)
```

```text
SQL
True
```

Yazdığın sözlük, dosyaya gidip geri geldiğinde **aynı** sözlük. Programın
kapanıp açılsa da veri kaybolmuyor.

Dört fonksiyonu karıştırmamak için tek kural yeter: **`s` "string" yani
metin demek.**

| Fonksiyon | Ne alır | Ne verir |
|---|---|---|
| `json.loads(metin)` | JSON metni | Python yapısı |
| `json.dumps(yapı)` | Python yapısı | JSON metni |
| `json.load(dosya)` | açık dosya | Python yapısı |
| `json.dump(yapı, dosya)` | Python yapısı + açık dosya | dosyaya yazar |

## İç içe veri

Gerçek JSON çoğunlukla iç içe: bir sözlüğün içinde liste, listenin içinde
sözlükler.

```python
text = """
{
  "course": "Python",
  "students": [
    {"name": "Ada", "scores": [90, 85]},
    {"name": "Alan", "scores": [70, 95]}
  ]
}
"""
data = json.loads(text)

print(data["students"][0]["name"])
print(data["students"][1]["scores"][1])
```

```text
Ada
95
```

Uzun bir erişim zinciri korkutucu görünebilir; soldan sağa, her adımda
elinde ne olduğuna bakarak oku:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span><code>data</code></span><span>bütün yapı: bir <b>sözlük</b></span></div>
    <div class="anat-row"><span><code>["students"]</code></span><span>sözlükte "students" anahtarı: bir <b>liste</b></span></div>
    <div class="anat-row"><span><code>[0]</code></span><span>listenin ilk öğesi: bir <b>sözlük</b> (Ada)</span></div>
    <div class="anat-row"><span><code>["name"]</code></span><span>o sözlükte "name" anahtarı: <code>"Ada"</code></span></div>
  </div>
  <figcaption><code>data["students"][0]["name"]</code> soldan sağa dört adım. Sözlükte anahtarla, listede sırayla içeri giriliyor.</figcaption>
</figure>

Her köşeli parantez bir adım içeri giriyor. Sözlükte **anahtarla**
(`["students"]`), listede **sırayla** (`[0]`). Takıldığında ara adımı
yazdır: `print(data["students"])` sana elindeki şeyin liste mi sözlük mü
olduğunu gösterir.

Listenin içindeki sözlükleri döngüyle dolaşmak da aynı:

```python
for student in data["students"]:
    print(student["name"], sum(student["scores"]))
```

```text
Ada 175
Alan 165
```

## Olmayabilecek anahtarlar: `get`

Dışarıdan gelen JSON'da her alan her zaman olmayabilir. Olmayan anahtarı
köşeli parantezle istemek hata veriyor:

```python
student = data["students"][0]
print(student["email"])
```

```text
KeyError: 'email'
```

Sözlükler bölümündeki `get` burada çok işe yarıyor: anahtar yoksa hata
vermek yerine verdiğin varsayılanı döndürüyor.

```python
print(student.get("email", "no email"))
```

```text
no email
```

Kural: **her zaman olacağından emin olduğun** alanı köşeli parantezle,
**olmayabilecek** alanı `get` ile al.

## Gidip gelince değişen türler

JSON'un türleri Python'unkinden az. Bu yüzden bazı şeyler dosyaya gidip
geri gelince **değişiyor**:

```python
point = {"x": 1, "y": 2, "tags": ("a", "b")}
back = json.loads(json.dumps(point))
print(back["tags"])
```

```text
['a', 'b']
```

**Demet listeye dönüyor.** JSON'da demet yok, yalnızca dizi var.

```python
counts = {1: "one", 2: "two"}
back = json.loads(json.dumps(counts))
print(back)
print(back.get(1))
print(back.get("1"))
```

```text
{'1': 'one', '2': 'two'}
None
one
```

**Anahtarlar her zaman metin oluyor.** JSON'da nesnenin anahtarı yalnızca
metin olabilir; `1` anahtarı `"1"` olarak geri geliyor ve `back.get(1)` artık
bir şey bulamıyor. Sayıyı **değer** olarak tutarsan (`{"id": 1}`) sayı olarak
kalıyor; sorun yalnızca anahtarda.

Bir de hiç çevrilemeyenler var. **Küme** (`set`) JSON'da yok:

```python
json.dumps({"tags": {"a", "b"}})
```

```text
TypeError: Object of type set is not JSON serializable
```

Çözüm, yazmadan önce listeye çevirmek: `sorted(tags)` hem liste veriyor hem
de sırayı her seferinde aynı yapıyor.

## Bozuk JSON

JSON kuralları katı. Python sözlüğü gibi yazılmış bir metni okumaya
çalışırsan:

```python
try:
    json.loads("{'name': 'Ada'}")
except json.JSONDecodeError as error:
    print(error)
```

```text
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

Hatanın adı `json.JSONDecodeError` (`json` modülünün içinde). Mesaj
**nerede** takıldığını söylüyor: 1. satır, 2. sütun, yani
tek tırnağın olduğu yer ("çift tırnak içinde bir ad bekleniyordu"). Sık
görülen üç bozukluk:

| Metin | Sorun |
|---|---|
| `{'name': 'Ada'}` | tek tırnak; JSON'da yalnızca çift tırnak |
| `{"a": 1,}` | sondaki virgül; JSON kabul etmiyor |
| `{"a": True}` | büyük harf; JSON'da `true` |

Bir dosya bozuk gelebiliyorsa okumayı `try` ile koru:

```python
DEFAULTS = {"theme": "dark", "language": "en"}

def load_settings(path):
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return DEFAULTS
    except json.JSONDecodeError:
        print("settings file is broken, using defaults")
        return DEFAULTS
```

Dosya yoksa da bozuksa da program çökmeden varsayılan ayarlarla devam
ediyor. Dosya İşlemleri bölümündeki "anlamlı bir karşılığın varsa yakala"
kuralının ta kendisi.

## Hepsi bir arada: kaydedilen yapılacaklar listesi

Program kapanınca kaybolmayan küçük bir yapılacaklar listesi:

```python
import json

def load_tasks():
    try:
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)

tasks = load_tasks()
tasks.append({"title": "learn JSON", "done": False})
save_tasks(tasks)
print(len(tasks), "tasks saved")
```

İlk çalıştırmada dosya yok, liste boş başlıyor:

```text
1 tasks saved
```

İkinci çalıştırmada önceki görev dosyadan geliyor:

```text
2 tasks saved
```

Akış her seferinde aynı: **oku → değiştir → yaz.** Dosyayı `"w"` ile baştan
yazmak önemli; `"a"` ile sonuna eklesen iki JSON metni yan yana dururdu ve
dosya artık geçerli JSON olmazdı (notta ayrıntısı var).

## Özet

- JSON, yapılı veriyi (sözlük, liste, sayı, metin) metin olarak yazmanın
  ortak biçimi. Her dil okuyabiliyor.
- `str(sözlük)` ile yazılan metin geri sözlük olmuyor; JSON oluyor.
- JSON'da yalnızca çift tırnak; `true`, `false`, `null`; sondaki virgül yok.
- `json.loads` metinden, `json.load` dosyadan okur; `json.dumps` metne,
  `json.dump` dosyaya yazar. **`s` = metin.**
- `indent=2` okunur yazar, `ensure_ascii=False` Türkçe harfleri korur.
- İç içe veride her köşeli parantez bir adım içeri: sözlükte anahtar, listede
  sıra. Olmayabilecek alanı `get` ile al.
- Gidip gelince: demet listeye, sayı anahtar metne döner; küme yazılamaz.
- Bozuk JSON `json.JSONDecodeError` verir; anlamlı bir varsayılanın varsa
  `try` ile yakala.
