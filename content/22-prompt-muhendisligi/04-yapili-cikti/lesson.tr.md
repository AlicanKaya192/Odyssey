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
