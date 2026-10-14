# Promptları Zincirlemek

Bir destek mesajına cevap vermek aslında birkaç iş: mesajın konusunu
bulmak, içindeki sipariş numarasını çıkarmak, ilgili kuralı bulmak ve
müşteriye bir cevap yazmak. Bunların hepsini tek bir uzun prompt'la
istemek mümkün; ama bir şey ters gittiğinde **hangi adımda** gittiğini
göremezsin. Bir başka yol işi küçük adımlara bölüp her adımı ayrı bir
çağrıyla yapmak ve bir adımın çıktısını sonrakine vermek: **prompt
zinciri** (prompt chaining). Bu bölümde bir zincir kuruyoruz, her adımın
çıktısını doğrulayıp hatada zinciri durduruyoruz ve zincirin token
bedelini tek prompt'la karşılaştırıyoruz.

## Üç adımlı zincir

<figure class="fig">
  <div class="flow">
    <span class="node">Sınıflandır</span>
    <span class="arrow">→</span>
    <span class="node">Sipariş no çıkar</span>
    <span class="arrow">→</span>
    <span class="node acc">İlgili kuralla cevap yaz</span>
  </div>
  <figcaption>Her adımın çıktısı doğrulanır; doğrulanamayan adım zinciri durdurur.</figcaption>
</figure>

İlk iki adım JSON döndürüyor ve doğrulanıyor. Üçüncü adım, birinci
adımın bulduğu kategoriye göre önceki modüldeki yardım merkezi
makalesini (`doc_data.py`) prompt'a koyuyor. Her adımın sonucunu ve giren
token'ını bir kayda yazıyoruz:

```python
import json

from doc_data import DOCS
from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
POLICY = {doc["id"]: doc["text"] for doc in DOCS}


def ask(client, instruction, text, max_tokens=60):
    messages = [{"role": "system", "content": instruction},
                {"role": "user", "content": text}]
    reply = client.chat(messages, max_tokens=max_tokens)
    return reply.text, reply.input_tokens


def parse(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def run_chain(client, message):
    log = []
    text, used = ask(client, 'Give the category as JSON: {"category": ...}',
                     message)
    data = parse(text)
    ok = isinstance(data, dict) and data.get("category") in LABELS
    log.append(("classify", ok, used))
    if not ok:
        return log, None
    category = data["category"]
    text, used = ask(client, 'Give the order number as JSON: '
                     '{"order_id": "ORD-12345" or null}', message)
    data = parse(text)
    ok = isinstance(data, dict) and "order_id" in data
    log.append(("extract", ok, used))
    if not ok:
        return log, None
    instruction = ("Answer in at most 3 sentences, using only this "
                   "policy:\n" + POLICY[category])
    text, used = ask(client, instruction, message, max_tokens=120)
    log.append(("reply", True, used))
    return log, text


client = ChatClient([
    '{"category": "shipping"}', '{"order_id": "ORD-48213"}',
    "Delivery takes 3 to 5 working days; ORD-48213 is on its way.",
    "refunds",
])
for message in ["Where is my order ORD-48213?",
                "I still have no money back for my return."]:
    log, answer = run_chain(client, message)
    print(log)
    print("answer:", answer)
```

```text
[('classify', True, 38), ('extract', True, 45), ('reply', True, 132)]
answer: Delivery takes 3 to 5 working days; ORD-48213 is on its way.
[('classify', False, 40)]
answer: None
```

İkinci mesajda ilk adımın cevabı JSON değil (`refunds` düz metin);
zincir orada duruyor ve kayıt **nerede** durduğunu söylüyor. Tek bir
uzun prompt'ta aynı hata, müşteriye giden cevabın bir yerinde ortaya
çıkardı ve sebebi görünmezdi. Zincirin asıl faydası bu: her adımın
girdisi ve çıktısı ayrı ayrı denetlenebilir, ayrı ayrı iyileştirilebilir.

Durunca ne olacağına program karar verir: o adımı hata mesajıyla
yeniden sormak (Yapılı Çıktı bölümündeki onarım), varsayılan bir yola
geçmek ya da mesajı bir insana göndermek.

## Zincirin token bedeli

Zincir her adımda mesajı yeniden gönderiyor; tek prompt ise bir kez.
Ama tek prompt hangi kuralın gerektiğini bilmediği için **bütün
kuralları** taşımak zorunda. İkisini ölçelim:

```python
from llm_client import count_message_tokens

single = [{"role": "system", "content":
           "Classify the message, find the order number and answer "
           "in at most 3 sentences using the right policy:\n"
           + "\n".join(POLICY[label] for label in LABELS)},
          {"role": "user", "content": "Where is my order ORD-48213?"}]
fresh = ChatClient(['{"category": "shipping"}',
                    '{"order_id": "ORD-48213"}', "On its way."])
log, _ = run_chain(fresh, "Where is my order ORD-48213?")
chain_total = sum(used for _, _, used in log)
print("single prompt:", count_message_tokens(single))
print("chain, 3 calls:", chain_total)
```

```text
single prompt: 412
chain, 3 calls: 215
```

Bu örnekte zincir daha ucuz: tek prompt beş kuralın hepsini taşıdığı için
412 token, zincirin üç çağrısının toplamı 215. Ama bu sonuç bağlamın
büyüklüğüne bağlı. Kurallar kısa ya da az olsaydı, zincirin mesajı her
adımda yeniden göndermesi ve her adımın ayrı bir cevap üretmesi tabloyu
tersine çevirebilirdi. Hangisinin ucuz olduğunu tahmin etme, kendi
verinle ölç.

## Gerekmeyen adımı atla

Her mesaj her adımı gerektirmez. Ödeme sorularında çoğu zaman sipariş
numarası gerekmez; ödeme ve garanti mesajlarında çıkarma adımını
atlarsak çağrı sayısı düşer. Önceki bölümlerin test mesajlarında sayalım:

```python
from shop_data import TICKETS

NEEDS_ORDER = {"shipping", "returns", "refunds"}
test = [t for t in TICKETS if t["id"] % 4 == 0]
fixed = 3 * len(test)
conditional = sum(3 if t["label"] in NEEDS_ORDER else 2 for t in test)
print("calls, every step:", fixed)
print("calls, skipping extract:", conditional)
```

```text
calls, every step: 30
calls, skipping extract: 26
```

Atlama kararı birinci adımın çıktısına dayanıyor; birinci adım yanlışsa
atlama da yanlış olur. Bu yüzden zincirde ilk adımlar en çok denetlenen
adımlardır.

## Ne zaman zincir, ne zaman tek prompt?

| Zincir | Tek prompt |
|---|---|
| Adımlar ayrı ayrı denetlenip iyileştirilebilir | Tek çağrı, daha az gecikme |
| Her adıma yalnızca gereken bağlam gider | Bütün bağlam her çağrıda gider |
| Hata hangi adımda belli olur | Hata cevabın içinde kaybolur |
| Daha çok çağrı, girdi tekrar gönderilir | Ara sonuçlar denetlenemez |

Kural: iş birbirinden farklı alt işlerden oluşuyorsa ve bir alt işin
hatası sonrakileri bozuyorsa zincir kur. Tek, basit bir işi zincire
bölmek yalnızca çağrı sayısını artırır.

## Özet

- Prompt zinciri bir işi adımlara böler; her adımın çıktısı sonrakinin
  girdisi olur.
- Her adımın çıktısını doğrula; doğrulanamayan adımda zinciri durdur ve
  nerede durduğunu kaydet.
- Zincir her adıma yalnızca gereken bağlamı gönderebilir; ama girdiyi
  her adımda yeniden gönderir. Bedeli ölç.
- Gerekmeyen adımı atlamak çağrı sayısını düşürür; atlama kararı önceki
  adımın doğruluğuna bağlıdır.
- Tek basit bir işi zincire bölme.
