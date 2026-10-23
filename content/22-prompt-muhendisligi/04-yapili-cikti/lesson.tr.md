# Yapılı Çıktı ve Doğrulama

Şimdiye kadar modelden tek bir kelime ya da tek bir sayı istedik. Çoğu
uygulama birden fazla bilgi ister: bir destek mesajının kategorisi, acil
olup olmadığı, içindeki sipariş numarası. Bunları serbest metin olarak
istemek, programı her cevapta metin içinde arama yapmaya zorlar. Bunun
yerine cevabı **yapılı** bir biçimde, çoğu zaman JSON olarak isteriz. Bu
bölümde gelen JSON'u adım adım ayrıştırmayı, bir şemaya göre
doğrulamayı ve geçersiz cevapta modele hatayı söyleyip yeniden sormayı
kuruyoruz.

## Şemayı yazmak

Talimatta cevabın tam biçimini, alan alan söylüyoruz:

<figure class="fig anat">
  <div class="anat-row"><span><code>category</code></span><span>Şu beşinden biri: shipping, returns, refunds, warranty, payment</span></div>
  <div class="anat-row"><span><code>urgent</code></span><span><code>true</code> ya da <code>false</code></span></div>
  <div class="anat-row"><span><code>order_id</code></span><span><code>ORD-</code> ve beş rakam, mesajda yoksa <code>null</code></span></div>
</figure>

Talimatın sonuna "Yalnızca JSON nesnesini yaz, başka metin ekleme" de
yazılır. Bazı sohbet API'leri cevabın geçerli bir JSON ya da verilen bir
şemaya uygun olmasını zorlayan bir ayar sunar; kullandığın serviste varsa
kullan. Ama o ayar yalnızca **biçimi** garanti eder; kategorinin doğru
seçilip seçilmediğini yine programın denetler.

## Gelen cevap her zaman temiz JSON değildir

Aşağıdaki altı **örnek yanıt**, böyle bir talimata gelebilecek cevapları
temsil ediyor: temiz JSON, kod bloğuna sarılmış JSON, önüne bir cümle
eklenmiş JSON, Python sözlüğü gibi tek tırnaklı yazılmış nesne, biçimi
doğru ama değerleri yanlış JSON ve `max_tokens`'ta kesilmiş JSON.
Ayrıştırıcımız üç yolu sırayla deniyor: metnin kendisi, kod bloğu
işaretleri atılmış hâli ve ilk `{` ile son `}` arasındaki parça.

```python
import json
import re

FENCE = "`" * 3
REPLIES = [
    '{"category": "shipping", "urgent": true, "order_id": "ORD-48213"}',
    FENCE + 'json\n{"category": "refunds", "urgent": false, '
    '"order_id": null}\n' + FENCE,
    'Sure! Here is the JSON:\n{"category": "warranty", '
    '"urgent": false, "order_id": "ORD-10077"}',
    "{'category': 'payment', 'urgent': True, 'order_id': None}",
    '{"category": "delivery", "urgent": "yes", "order_id": "48213"}',
    '{"category": "returns", "urgent": false, "order_id": "ORD-',
]


def parse_json(text):
    attempts = {
        "as is": text,
        "fence": re.sub(r"^`{3}(?:json)?\s*|\s*`{3}$", "", text.strip()),
        "braces": text[text.find("{"): text.rfind("}") + 1],
    }
    for name, candidate in attempts.items():
        try:
            return json.loads(candidate), name
        except json.JSONDecodeError:
            pass
    return None, "failed"


for number, reply in enumerate(REPLIES, 1):
    print(number, parse_json(reply)[1])
```

```text
1 as is
2 fence
3 braces
4 failed
5 as is
6 failed
```

Altı cevabın dördü bir yolla ayrıştırıldı. Kod bloğu ve öndeki cümle
zararsız ekler; onları atmak güvenli. Tek tırnaklı nesne JSON değil;
Python'un kendi okuyucusuyla kurtarmak mümkün olsa da hangi biçimlerin
kabul edildiği belirsizleşir, yeniden sormak daha temiz. Kesilmiş cevap
ise hiçbir yolla kurtarılamaz: burada önce `finish_reason`'a bakmak
gerekir; `length` ise `max_tokens` cevaba yetmemiştir.

## Şemaya göre doğrulamak

Ayrıştırılan her JSON doğru değildir. Beşinci cevap geçerli bir JSON ama
kategori listede yok, `urgent` metin, sipariş numarası eksik biçimde.
Şemayı koda çevirelim:

```python
LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]


def validate(data):
    if not isinstance(data, dict):
        return ["the answer must be a JSON object"]
    errors = [f"missing {key}" for key in ["category", "urgent", "order_id"]
              if key not in data]
    if data.get("category") not in LABELS:
        errors.append("category must be one of " + ", ".join(LABELS))
    if not isinstance(data.get("urgent"), bool):
        errors.append("urgent must be true or false")
    order = data.get("order_id")
    if order is not None and not re.fullmatch(r"ORD-\d{5}", str(order)):
        errors.append("order_id must look like ORD-12345 or be null")
    return errors


for number, reply in enumerate(REPLIES, 1):
    data, stage = parse_json(reply)
    errors = validate(data) if data is not None else ["not valid JSON"]
    print(number, "ok" if not errors else f"{len(errors)} error(s)")
print(*validate(parse_json(REPLIES[4])[0]), sep="\n")
```

```text
1 ok
2 ok
3 ok
4 1 error(s)
5 3 error(s)
6 1 error(s)
category must be one of shipping, returns, refunds, warranty, payment
urgent must be true or false
order_id must look like ORD-12345 or be null
```

Altı cevabın yalnızca üçü kullanılabilir. Hata mesajlarını özellikle
**okunur cümleler** olarak yazdık: bir sonraki adımda onları modele
göndereceğiz.

## Hatayı söyleyip yeniden sormak

Geçersiz bir cevap geldiğinde en basit onarım, modelin cevabını ve hata
listesini sohbete ekleyip yeniden sormaktır. Model ne yanlış yaptığını
görür. Sınırsız denemek yerine bir üst sınır koyarız:

```python
import textwrap

from llm_client import ChatClient, count_message_tokens


def ask_json(client, messages, max_tries=3):
    messages = list(messages)
    for tries in range(1, max_tries + 1):
        reply = client.chat(messages, max_tokens=60)
        data, stage = parse_json(reply.text)
        errors = validate(data) if data is not None else ["not valid JSON"]
        if not errors:
            return data, tries
        feedback = ("Your answer was not valid: " + "; ".join(errors)
                    + ". Reply with the JSON object only.")
        messages += [{"role": "assistant", "content": reply.text},
                     {"role": "user", "content": feedback}]
    return None, max_tries


client = ChatClient([REPLIES[4], REPLIES[0]])
question = [{"role": "user", "content": "My parcel ORD-48213 is late!"}]
data, tries = ask_json(client, question)
print(data, tries)
print(textwrap.fill(client.calls[1]["messages"][-1]["content"], 64))
print([count_message_tokens(call["messages"]) for call in client.calls])
```

```text
{'category': 'shipping', 'urgent': True, 'order_id': 'ORD-48213'} 2
Your answer was not valid: category must be one of shipping,
returns, refunds, warranty, payment; urgent must be true or
false; order_id must look like ORD-12345 or be null. Reply with
the JSON object only.
[16, 114]
```

İkinci denemede geçerli bir cevap geldi. Onarımın da bir bedeli var:
ikinci çağrı ilk soruyu, yanlış cevabı ve hata mesajını birlikte
gönderiyor; giren token 16'dan 114'e çıktı. Bu yüzden önce
talimatı ve örnekleri iyileştirip geçersiz cevapları azaltmak, onarımı
yalnızca kalan durumlar için kullanmak gerekir. Deneme sınırı dolarsa
cevap bir insana ya da varsayılan bir yola (`needs_review`) gider.

## Şemadan geçen ama belirsiz cevap

Şema biçimi denetler, anlamı denetlemez. Müşteri "Call me tomorrow at 7"
(yarın 7'de ara) yazdı diyelim. Model bir geri arama saati çıkarırken
sabah mı akşam mı olduğunu bilemez, ama şema bir saat istediği için yine
de birini **seçer**: `"07:00"`. Cevap kusursuz bir JSON'dur ve şemadan
geçer, oysa doğru cevap müşteriye sormaktır. NLP Temelleri'nin Bilgi
Çıkarma bölümünde gördüğümüz gibi, "yarın" ancak bugün bilinince bir güne
dönüşür; o yüzden referans anı modele **bağlam** olarak veririz ve
cevabın kaynağını, müşterinin kendi sözlerini (`source`) de isteriz.

Aşağıdaki beş **örnek yanıt** böyle bir talimata gelebilecek cevaplar.
Program her birini üç sonuçtan birine ayırır: `accepted` (kabul),
`rejected` (ret) ya da `needs_clarification` (açıklama gerekiyor):

```python
import json
from collections import Counter
from datetime import datetime, timedelta

NOW = "2026-03-14T01:30:00+03:00"
SYSTEM = ("Extract the callback time as JSON with date (YYYY-MM-DD), "
          "time (HH:MM, 24-hour) and source (the customer's exact words). "
          "The current time is " + NOW + ".")
CASES = [  # müşteri mesajı, örnek yanıt, beklenen sonuç
    ("Call me tomorrow at 7pm.",
     '{"date": "2026-03-15", "time": "19:00", "source": "tomorrow at 7pm"}',
     "accepted"),
    ("Call me tomorrow at 7.",
     '{"date": "2026-03-15", "time": "07:00", "source": "tomorrow at 7"}',
     "needs_clarification"),
    ("Call me today at 9am.",
     '{"date": "2026-03-15", "time": "09:00", "source": "today at 9am"}',
     "rejected"),
    ("Please call me back.",
     '{"date": "2026-03-14", "time": "10:00", "source": "today at 10am"}',
     "rejected"),
    ("Tomorrow at 12pm works.",
     '{"date": "2026-03-15", "time": "12:00", "source": "Tomorrow at 12pm"}',
     "accepted"),
]
PHRASE = r"(today|tomorrow) at (\d{1,2})(am|pm)?"
KEYS = {"date", "time", "source"}


def schema_only(message, data, now):
    keys_ok = isinstance(data, dict) and set(data) == KEYS
    return "accepted" if keys_ok else "rejected"


def check_callback(message, data, now):
    if schema_only(message, data, now) == "rejected":
        return "rejected"
    m = re.fullmatch(PHRASE, str(data["source"]).lower())
    if m is None or str(data["source"]).lower() not in message.lower():
        return "rejected"
    if m[3] is None:
        return "needs_clarification"
    hour = int(m[2]) % 12 + (12 if m[3] == "pm" else 0)
    days = 1 if m[1] == "tomorrow" else 0
    day = datetime.fromisoformat(now).date() + timedelta(days=days)
    if (data["date"], data["time"]) != (day.isoformat(), f"{hour:02d}:00"):
        return "rejected"
    return "accepted"


client = ChatClient([reply for _, reply, _ in CASES])
outcomes = []
for message, _, expected in CASES:
    question = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": message}]
    data, stage = parse_json(client.chat(question, max_tokens=60).text)
    got = check_callback(message, data, NOW)
    outcomes.append((expected, schema_only(message, data, NOW), got))
    print(f"{message:25} {got}")
totals = Counter(e for e, _, _ in outcomes)
print(f"{'':20} schema  check")
for label in ["accepted", "rejected", "needs_clarification"]:
    schema = sum(e == s for e, s, _ in outcomes if e == label)
    check = sum(e == g for e, _, g in outcomes if e == label)
    print(f"{label:20} {schema}/{totals[label]}     {check}/{totals[label]}")
```

```text
Call me tomorrow at 7pm.  accepted
Call me tomorrow at 7.    needs_clarification
Call me today at 9am.     rejected
Please call me back.      rejected
Tomorrow at 12pm works.   accepted
                     schema  check
accepted             2/2     2/2
rejected             0/2     2/2
needs_clarification  0/1     1/1
```

- Beş cevabın beşi de geçerli JSON ve şemadaki üç alana sahip. Yalnızca
  şemaya bakan denetim (`schema` sütunu) beşini de kabul ediyor:
  reddedilmesi gereken iki cevabı ve sorulması gereken birini kaçırıyor.
- İkinci cevapta model `"07:00"` uydurdu. Müşterinin sözlerinde `am`/`pm`
  yok, program bunu kaynaktan görüyor ve sormayı seçiyor.
- Üçüncüde model "today"yi 15 Mart'a çevirmiş; program aynı hesabı referans
  anla kendisi yapıyor ve tutmayınca reddediyor. Dördüncüde `source`
  müşterinin mesajında hiç geçmiyor: model saati uydurmuş.
- Sonuçları **ayrı ayrı** sayıyoruz. Tek bir doğruluk oranı, açıklama
  gereken bir durumu "kabul" sayan bir hatayı, reddedilmesi gereken bir
  cevabı kabul eden hatadan ayırmaz; ikisinin bedeli farklıdır.

## Özet

- Birden fazla bilgi isteniyorsa cevabı JSON gibi yapılı bir biçimde iste
  ve şemayı alan alan yaz.
- Ayrıştırırken zararsız ekleri (kod bloğu, öndeki cümle) temizle; JSON
  olmayanı tahminle kurtarma.
- Kesilmiş JSON'un sebebi `max_tokens`; önce `finish_reason`'a bak.
- Ayrıştırılan veriyi şemaya göre doğrula: alanlar, türler, izin verilen
  değerler, kalıplar.
- Hataları okunur cümleler olarak yaz ve geçersiz cevapta modele
  göndererek yeniden sor; deneme sayısına sınır koy.
- Onarım her denemede daha çok token gönderir; asıl çözüm geçersiz
  cevapları azaltan net bir talimat.
- Şemadan geçmek anlamın doğru olduğunu göstermez. Referans an gibi
  bağlamı modele ver, kaynağı iste ve program kendisi denetlesin; belirsiz
  cevabı kabul etme, sor. Kabul, ret ve açıklama gereken durumları ayrı ölç.
