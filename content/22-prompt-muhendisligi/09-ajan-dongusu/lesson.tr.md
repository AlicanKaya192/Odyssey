# Ajan Döngüsü

Önceki bölümde model bir araç çağırdı, program sonucu verdi ve model
cevap yazdı: tek tur. Bazı sorular birkaç araç çağrısı gerektirir ve hangi
çağrının gerektiğini önceden bilemezsin: "İki siparişimden hangisi daha
pahalıydı ve o kargoya verildi mi?" Model önce iki tutarı, sonra pahalı
olanın durumunu sorar. Modelin her adımda bir sonraki eylemi seçtiği,
programın araçları çalıştırıp sonucu geri verdiği bu döngüye **ajan**
(agent) denir. Bu bölümde bir ajan döngüsü kuruyoruz ve onu güvenli
yapan şeylere odaklanıyoruz: adım sınırı, tekrar eden çağrıyı yakalamak,
hatayı geri vermek ve her adımda büyüyen token bedeli.

<figure class="fig">
  <div class="flow">
    <span class="node">Model: sonraki eylem</span>
    <span class="arrow">→</span>
    <span class="node acc">Program: aracı çalıştır</span>
    <span class="arrow">→</span>
    <span class="node">Sonucu geçmişe ekle</span>
    <span class="arrow">→</span>
    <span class="node">Cevap ya da yeni tur</span>
  </div>
  <figcaption>Döngüyü model değil program yönetir: ne zaman duracağına program karar verir.</figcaption>
</figure>

## Döngü

İki araç kullanıyoruz: siparişin durumunu veren `get_order` ve tutarını
hesaplayan `order_total` (`shop_data.py`'deki kurgusal siparişlerle).
Döngü en fazla `max_steps` tur dönüyor; aynı çağrı ikinci kez gelirse
çalıştırılmıyor, modele "bunu zaten yaptın" diye bir hata dönüyor. Her
turun giren token'ını bir izde (trace) tutuyoruz:

```python
import json

from llm_client import ChatClient
from shop_data import ORDERS

SYSTEM = "You are a shop assistant. Use the tools; answer when you know."
SCHEMA = [{"name": "get_order", "parameters": ["order_id"]},
          {"name": "order_total", "parameters": ["order_id"]}]


def get_order(order_id):
    order = ORDERS[order_id]
    return {"status": order["status"], "date": order["date"]}


def order_total(order_id):
    items = ORDERS[order_id]["items"]
    return {"total": round(sum(p * c for _, p, c in items), 2)}


TOOLS = {"get_order": get_order, "order_total": order_total}


def run_tool(call):
    function = TOOLS.get(call["name"])
    if function is None:
        return {"error": f"unknown tool {call['name']}"}
    try:
        return function(**call.get("arguments", {}))
    except (TypeError, KeyError):
        return {"error": "wrong arguments"}


def agent(client, question, max_steps=5):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    seen, trace = set(), []
    for step in range(1, max_steps + 1):
        reply = client.chat(messages, tools=SCHEMA)
        trace.append(reply.input_tokens)
        if not reply.tool_calls:
            return reply.text, step, trace
        messages.append({"role": "assistant", "content": "",
                         "tool_calls": reply.tool_calls})
        for call in reply.tool_calls:
            key = json.dumps(call, sort_keys=True)
            if key in seen:
                result = {"error": "you already made this call"}
            else:
                result = run_tool(call)
            seen.add(key)
            messages.append({"role": "tool", "content": json.dumps(result)})
    return None, max_steps, trace
```

Döngünün iki çıkışı var: model araç çağırmadan bir cevap verirse o cevap,
`max_steps` dolarsa `None`. İkinci çıkış önemli: modelin "bitti" demesine
güvenip sonsuza kadar dönen bir döngü hem para hem zaman yakar.

## Üç senaryo

Aşağıdaki üç **örnek yanıt dizisi** üç durumu temsil ediyor: soruyu
çözen bir ajan, aynı çağrıyı tekrar tekrar yapan bir ajan ve yanlış araç
adıyla başlayıp hatadan sonra düzelen bir ajan.

```python
def call(name, order_id):
    return {"name": name, "arguments": {"order_id": order_id}}


QUESTION = "Which of ORD-10077 and ORD-61890 cost more, and has it shipped?"
SCRIPTS = {
    "solves": [
        {"tool_calls": [call("order_total", "ORD-10077"),
                        call("order_total", "ORD-61890")]},
        {"tool_calls": [call("get_order", "ORD-10077")]},
        "ORD-10077 cost more (214.90) and it was delivered.",
    ],
    "repeats": [{"tool_calls": [call("get_order", "ORD-10077")]}] * 6,
    "recovers": [
        {"tool_calls": [call("get_status", "ORD-10077")]},
        {"tool_calls": [call("get_order", "ORD-10077")]},
        "ORD-10077 was delivered on 2026-09-28.",
    ],
}
for name, script in SCRIPTS.items():
    text, steps, trace = agent(ChatClient(script), QUESTION)
    print(name, steps, trace, sum(trace))
    print("   ", text)
```

```text
solves 3 [50, 82, 114] 246
    ORD-10077 cost more (214.90) and it was delivered.
repeats 5 [50, 82, 105, 128, 151] 516
    None
recovers 3 [50, 73, 105] 228
    ORD-10077 was delivered on 2026-09-28.
```

Birinci ajan üç turda cevap verdi: önce iki tutarı tek turda iki çağrıyla
istedi, sonra pahalı siparişin durumunu. İkincisi aynı çağrıyı tekrarladı;
ikinci turdan itibaren her seferinde "bunu zaten yaptın" hatası aldı ama
durmadı ve beşinci turda program onu durdurdu, cevap `None`. Üçüncüsü var
olmayan bir araçla başladı, hatayı görünce doğru araca geçti. Ama cevabı
soruyu yarım bırakıyor: hangi siparişin daha pahalı olduğunu söylemiyor.
Döngünün düzgün bitmesi cevabın doğru ve tam olduğu anlamına gelmez;
bunu değerlendirme gösterir.

## Her tur daha pahalı

İzdeki sayılar her turda büyüyor: ajan geçmişi, araç çağrılarını ve
sonuçlarını her turda yeniden gönderiyor. Tekrar eden ajan beş turda
516 giren token harcadı ve hiçbir şey üretmedi. Bir ajan
için iki sınır birlikte konur: **adım sınırı** ve **token bütçesi**.
Hangisi önce dolarsa döngü durur ve iş bir insana ya da sabit bir yola
gider.

## Ajanı güvenli yapan kurallar

- **Döngüyü program yönetir.** Adım sınırı, token bütçesi, zaman sınırı
  programda; modelin "bitti" demesine bağlı değil.
- **Tekrarı yakala.** Aynı argümanlarla aynı çağrı genellikle ajanın
  takıldığının işaretidir.
- **Hataları geri ver.** Bilinmeyen araç ya da yanlış argüman programı
  çökertmez; hata modele gider ve model düzelebilir (üçüncü senaryo).
- **Önceki bölümün araç kuralları aynen geçerli:** izin listesi, argüman
  doğrulaması, geri alınamaz işlerde onay. Ajan daha çok araç çağırdığı
  için bu kuralların önemi artar.
- **İzi kaydet.** Her turda hangi araç, hangi argüman, hangi sonuç ve kaç
  token; bir ajanın neden yanlış cevap verdiği ancak izden anlaşılır.

## Ne zaman ajan?

Ajan, adımların sırası önceden bilinmediğinde işe yarar. Adımlar her
zaman aynıysa (sınıflandır, çıkar, cevap yaz) önceki bölümlerdeki zincir
daha öngörülebilir, daha ucuz ve daha kolay test edilir. Kural: **önce
zincir dene; adımların sırası gerçekten girdiye göre değişiyorsa ajana
geç.**

## Özet

- Ajan, modelin her turda bir sonraki eylemi seçtiği ve programın
  araçları çalıştırdığı bir döngüdür.
- Döngünün çıkışı yalnızca modelin cevabı değil, programın sınırıdır:
  adım sınırı ve token bütçesi.
- Aynı çağrının tekrarı yakalanır ve modele hata olarak bildirilir.
- Araç hataları modele geri verilir; ajan düzelebilir.
- Her tur geçmişi yeniden gönderir; token bedeli turla büyür.
- Adımlar sabitse zincir, değişiyorsa ajan.
