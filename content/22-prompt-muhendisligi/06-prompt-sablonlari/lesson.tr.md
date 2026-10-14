# Prompt Şablonları

Gerçek bir uygulamada prompt elle yazılmaz; bir **şablondan** her çağrıda
yeniden kurulur: sabit metin aynı kalır, müşterinin mesajı, sipariş
numarası, belge parçaları gibi **değişkenler** yerine konur. Şablon
basit bir metin işlemi gibi görünür, ama üç tuzağı var ve üçü de sessiz
çalışır: JSON örneğindeki süslü parantezler, eksik kalan değişkenler ve
değişkenin içinden gelen şablon işaretleri. Bu bölümde üçünü de Python'da
gerçekten çalıştırıp görüyor ve güvenli bir şablon fonksiyonu yazıyoruz.

## `str.format` ve JSON

Python'da ilk akla gelen `str.format`. Ama talimatımızda bir JSON örneği
varsa süslü parantezler `format`'ın kendi işaretleriyle karışır:

```python
TEMPLATE = ('Put the message into one category.\n'
            'Answer as JSON: {"category": "<name>"}\n'
            'Message: {message}')
try:
    print(TEMPLATE.format(message="Where is my parcel?"))
except KeyError as error:
    print("KeyError:", error)

SAFE = ('Put the message into one category.\n'
        'Answer as JSON: {{"category": "<name>"}}\n'
        'Message: {message}')
print(SAFE.format(message="Where is my parcel?"))
```

```text
KeyError: '"category"'
Put the message into one category.
Answer as JSON: {"category": "<name>"}
Message: Where is my parcel?
```

`format`, `{"category": "<name>"}` kısmını bir değişken sandı ve öyle bir
değişken verilmediği için hata verdi. Düzeltmesi JSON'daki parantezleri
ikiye katlamak (`{{` ve `}}`). Hata en azından **gürültülü**: program
çalışmadan durdu.

## Sessiz eksik değişken

`string.Template` `$ad` biçiminde yer tutucu kullanır; JSON parantezleriyle
çakışmaz. İki fonksiyonu var ve farkları önemli:

```python
from string import Template

t = Template("Hello $name, your order $order_id is on its way.")
print(t.safe_substitute(name="Ada"))
try:
    t.substitute(name="Ada")
except KeyError as error:
    print("KeyError:", error)
```

```text
Hello Ada, your order $order_id is on its way.
KeyError: 'order_id'
```

`safe_substitute` eksik değişkeni olduğu gibi bırakıyor ve hiçbir şey
söylemiyor: modele `$order_id` yazan bir prompt gider ve model bunu
kendince yorumlar. `substitute` ise hata veriyor. Prompt kurarken
**gürültülü hata sessiz hatadan iyidir**: eksik değişken, model çalışmadan
yakalanmalı.

## Değişkenin içinden gelen işaret

Şablonları `{{ad}}` biçiminde yazıp her değişken için `replace` yapmak da
yaygın bir yol. Müşterinin mesajı bir şablon işareti içerirse ne olur?

```python
import re

SLOT = re.compile(r"\{\{(\w+)\}\}")
T = "Customer {{name}} wrote: {{message}}\nOrder: {{order_id}}"
VALUES = {"name": "Ada", "message": "Is {{order_id}} shipped?",
          "order_id": "ORD-48213"}


def render_naive(template, values):
    for name, value in values.items():
        template = template.replace("{{" + name + "}}", str(value))
    return template


def render(template, values):
    names = set(SLOT.findall(template))
    missing, unused = names - values.keys(), values.keys() - names
    if missing or unused:
        raise ValueError(f"missing {sorted(missing)}, unused {sorted(unused)}")
    return SLOT.sub(lambda m: str(values[m.group(1)]), template)


print(render_naive(T, VALUES))
print(render(T, VALUES))
try:
    render(T, {"name": "Ada"})
except ValueError as error:
    print("ValueError:", error)
```

```text
Customer Ada wrote: Is ORD-48213 shipped?
Order: ORD-48213
Customer Ada wrote: Is {{order_id}} shipped?
Order: ORD-48213
ValueError: missing ['message', 'order_id'], unused []
```

Sırayla `replace` yapan sürüm müşterinin mesajını **değiştirdi**:
mesajın içindeki `{{order_id}}`, mesaj şablona yerleştikten sonra gelen
`replace` tarafından doldu. Burada zararsız görünüyor, ama aynı yol
müşterinin yazdığı bir metnin, şablonun başka bir yerine konan gizli bir
değeri (bir iç not, başka bir müşterinin bilgisi) kendi mesajına
çekmesine izin verir. Güvenli `render` iki şey yapıyor:

- Şablonu **tek geçişte** dolduruyor (`SLOT.sub`): yerleştirilen değer
  bir daha taranmıyor.
- Şablondaki değişkenlerle verilen değerleri karşılaştırıp eksik ya da
  kullanılmayan bir değişken varsa çalışmadan duruyor. Kullanılmayan
  değişken çoğu zaman bir yazım hatasıdır (`order` yerine `order_id`).

## Değişkene bütçe

Bir değişken çok uzun olabilir: müşteri uzun bir mesaj yazar, bir belge
parçası beklenenden büyük gelir. Bütçeyi aşan metni kesmek gerekir, ama
**nereden** kestiğin önemli:

```python
def fit_start(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + " ..."


def fit_middle(text, max_words):
    words = text.split()
    if len(words) <= max_words:
        return text
    head = max_words // 2
    tail = max_words - head
    return " ".join(words[:head]) + " ... " + " ".join(words[-tail:])


LONG = ("I bought the Trail 40 backpack in May. " * 6
        + "Yesterday the main zip broke and I need it for a trip on Friday.")
print(len(LONG.split()), "words")
for fit in [fit_start, fit_middle]:
    short = fit(LONG, 24)
    print(fit.__name__, len(short.split()), "zip" in short)
```

```text
62 words
fit_start 25 False
fit_middle 25 True
```

Baştan kesen sürüm mesajın asıl derdini (fermuar bozuldu, cuma günü
lazım) attı; ortadan kesen sürüm başı ve sonu tuttu. Hangisinin doğru
olduğu veriye bağlı: destek mesajlarında asıl istek çoğu zaman sondadır,
bir belgede ise başlık ve ilk paragraf. Kestiğini de belli et (`...`);
model metnin eksik olduğunu bilmeli.

## Şablonları yönetmek

- **Şablonları koddan ayrı ve adlı tut:** `classify`, `summarize`,
  `reply`. Her birinin bir **sürümü** olsun; değiştirdiğinde yeni sürüm
  aç, eskisini silme. Değerlendirme (sonraki bölümler) iki sürümü aynı
  kümede karşılaştırır.
- **Kayda şablonun adını ve sürümünü yaz** (Sistem Mesajı bölümündeki
  özet gibi).
- **Şablonu test et:** her şablon için beklenen değişkenlerle bir
  örnek kur ve sonucu bir kez gözle oku; `render`'ın hata vermesi yetmez.

## Özet

- Şablon sabit metin ile değişkenlerden her çağrıda prompt kurar.
- `str.format`'ta JSON örneğinin parantezleri ikiye katlanır (`{{ }}`);
  yoksa `KeyError`.
- `safe_substitute` eksik değişkeni sessizce bırakır; prompt kurarken
  eksik değişken hata vermeli.
- Sırayla `replace` müşterinin metnindeki işaretleri de doldurur; şablonu
  tek geçişte doldur ve değişken listesini denetle.
- Uzun değişkeni bütçeye sığdırırken nereden kestiğine dikkat et ve
  kestiğini belli et.
- Şablonlara ad ve sürüm ver; kayda yaz.
