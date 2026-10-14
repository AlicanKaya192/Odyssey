# Araç Çağırma

Bir dil modeli müşterinin siparişinin nerede olduğunu bilemez; o bilgi
mağazanın veritabanında. Modelin bilmediği ya da yapamadığı bir şey
gerektiğinde ona **araçlar** (tools) tanıtılır: "sipariş numarasıyla
siparişi getiren bir fonksiyon var". Model cevap yerine bir **araç
çağrısı** döndürür: hangi aracı, hangi argümanlarla çağırmak istediğini.
Aracı **program** çalıştırır ve sonucu modele geri verir; model son
cevabı o sonuçla yazar. Bu bölümde bu döngüyü kuruyoruz ve en önemli
kuralı görüyoruz: modelin istediği çağrı, program tarafından
**doğrulanmadan** çalıştırılmaz.

<figure class="fig">
  <div class="flow">
    <span class="node">Soru + araç listesi</span>
    <span class="arrow">→</span>
    <span class="node">Model: araç çağrısı</span>
    <span class="arrow">→</span>
    <span class="node acc">Program doğrular ve çalıştırır</span>
    <span class="arrow">→</span>
    <span class="node">Model: son cevap</span>
  </div>
  <figcaption>Model aracı çalıştırmaz; yalnızca çağırmak istediğini söyler.</figcaption>
</figure>

## Araçları tanımlamak

Her aracın bir adı, modelin ne zaman kullanacağını anlatan bir açıklaması
ve argümanları var. `shop_data.py`'ye eklediğimiz kurgusal siparişlerle
iki araç yazalım: siparişi getiren `get_order` ve siparişi iptal eden
`cancel_order`. İptal geri alınamaz bir iş; onu ayrıca işaretliyoruz:

```python
import json
import re

from shop_data import ORDERS


def get_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    return {"order_id": order_id, "status": order["status"],
            "date": order["date"]}


def cancel_order(order_id):
    return {"order_id": order_id, "cancelled": True}


TOOLS = {
    "get_order": {"function": get_order, "confirm": False,
                  "description": "Look up an order's status by its number.",
                  "parameters": {"order_id": r"ORD-\d{5}"}},
    "cancel_order": {"function": cancel_order, "confirm": True,
                     "description": "Cancel an order that has not shipped.",
                     "parameters": {"order_id": r"ORD-\d{5}"}},
}


def schema(tools):
    return [{"name": name, "description": tool["description"],
             "parameters": list(tool["parameters"])}
            for name, tool in tools.items()]


print(json.dumps(schema(TOOLS)[0], indent=1))
print(get_order("ORD-48213"))
```

```text
{
 "name": "get_order",
 "description": "Look up an order's status by its number.",
 "parameters": [
  "order_id"
 ]
}
{'order_id': 'ORD-48213', 'status': 'shipped', 'date': '2026-10-09'}
```

Modele giden yalnızca `schema(TOOLS)`: adlar, açıklamalar, argüman
adları. Fonksiyonların kendisi, argüman kalıpları ve "onay gerekir"
işareti programda kalır. Gerçek sohbet API'leri argümanları JSON Schema
ile, türleri ve açıklamalarıyla birlikte ister; buradaki liste aynı fikrin
kısaltılmışı. Açıklamalar önemli: model hangi aracı ne zaman seçeceğine
çoğu zaman yalnızca açıklamaya bakarak karar verir.

## Çağrıyı doğrulamak

Modelin döndürdüğü araç çağrısı bir **istektir**, emir değil. Model var
olmayan bir aracı, yanlış biçimde bir argümanı ya da kullanıcının
istemediği geri alınamaz bir işi isteyebilir. Program her çağrıyı
çalıştırmadan önce denetler:

```python
def run_tool(call):
    tool = TOOLS.get(call["name"])
    if tool is None:
        return {"error": f"unknown tool {call['name']}"}
    args = call.get("arguments", {})
    if set(args) != set(tool["parameters"]):
        return {"error": "arguments must be " + ", ".join(tool["parameters"])}
    for name, pattern in tool["parameters"].items():
        if not re.fullmatch(pattern, str(args[name])):
            return {"error": f"{name} has the wrong form"}
    if tool["confirm"]:
        return {"pending": "needs the customer's confirmation"}
    return tool["function"](**args)


CALLS = [{"name": "get_order", "arguments": {"order_id": "ORD-48213"}},
         {"name": "get_order", "arguments": {"order_id": "48213"}},
         {"name": "get_order", "arguments": {"order_id": "ORD-99999"}},
         {"name": "cancel_order", "arguments": {"order_id": "ORD-23345"}},
         {"name": "delete_account", "arguments": {}}]
for call in CALLS:
    print(call["name"], json.dumps(run_tool(call)))
```

```text
get_order {"order_id": "ORD-48213", "status": "shipped", "date": "2026-10-09"}
get_order {"error": "order_id has the wrong form"}
get_order {"error": "no order ORD-99999"}
cancel_order {"pending": "needs the customer's confirmation"}
delete_account {"error": "unknown tool delete_account"}
```

Beş örnek çağrıdan yalnızca biri bir sipariş bilgisi döndürdü. Biçimi yanlış sipariş
numarası, var olmayan sipariş ve bilinmeyen araç birer **hata sonucu**
olarak döndü; program çökmedi, hata modele geri gidecek ve model
müşteriye doğru bir şey söyleyebilecek. İptal isteği çalıştırılmadı:
onay bekliyor.

Üç kural:

- **Yalnızca izin listesindeki araçlar.** Modelin verdiği adı hiçbir
  zaman doğrudan bir fonksiyon ya da komut olarak çalıştırma
  (`eval`, `getattr` gibi yollar yok).
- **Argümanları her zaman doğrula.** Model müşterinin yazdığı bir metni
  argümana taşıyabilir; argüman veritabanı sorgusuna ya da dosya yoluna
  gidiyorsa bu bir saldırı yolu olur.
- **Geri alınamaz işler onaysız yapılmaz.** İptal, ödeme, silme gibi
  işlerde son kararı müşteri ya da bir çalışan verir.

## Döngünün tamamı

Şimdi soru, araç çağrısı, araç sonucu ve son cevabı birleştirelim.
Modelin araç çağrısı `assistant` mesajı olarak, aracın sonucu `tool`
rolündeki bir mesaj olarak geçmişe eklenir. Aşağıdaki iki **örnek
yanıt** bir araç çağrısı ve araç sonucunu kullanan bir son cevap:

```python
from llm_client import ChatClient

SYSTEM = ("You are a shop assistant. Use the tools to look up orders; "
          "never guess an order's status.")


def answer(client, question):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    reply = client.chat(messages, tools=schema(TOOLS))
    if reply.tool_calls:
        messages.append({"role": "assistant", "content": "",
                         "tool_calls": reply.tool_calls})
        for call in reply.tool_calls:
            messages.append({"role": "tool",
                             "content": json.dumps(run_tool(call))})
        reply = client.chat(messages, tools=schema(TOOLS))
    return reply.text, messages


client = ChatClient([
    {"tool_calls": [{"name": "get_order",
                     "arguments": {"order_id": "ORD-48213"}}]},
    "Your order ORD-48213 was shipped on 2026-10-09.",
])
text, messages = answer(client, "Where is my order ORD-48213?")
print([m["role"] for m in messages])
print(messages[-1]["content"])
print(text)
print(len(client.calls), "calls")
```

```text
['system', 'user', 'assistant', 'tool']
{"order_id": "ORD-48213", "status": "shipped", "date": "2026-10-09"}
Your order ORD-48213 was shipped on 2026-10-09.
2 calls
```

Bir soru iki çağrı tuttu: biri araç çağrısını almak, biri sonucu
kullanarak cevabı yazmak için. İkinci çağrı ilk soruyu, araç çağrısını ve
araç sonucunu da taşıyor; araç kullanmanın token bedeli bu.

Gerçek API'lerde her araç çağrısının bir kimliği olur ve `tool` mesajı o
kimliğe bağlanır; böylece model aynı anda birden fazla aracı
çağırdığında hangi sonucun hangi çağrıya ait olduğu karışmaz. Buradaki
istemci bunu basitleştiriyor.

## Cevap araç sonucuna dayanıyor mu?

Model araç sonucunu aldıktan sonra bile cevabında başka bir tarih ya da
durum yazabilir. Araç sonucu yapılı olduğu için bunu kodla denetlemek
kolay: cevaptaki tarihlerin araç sonucundaki tarihle aynı olup
olmadığına bakalım.

```python
def grounded(text, tool_result):
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    return all(date == tool_result.get("date") for date in dates)


result = get_order("ORD-48213")
for text in ["Your order ORD-48213 was shipped on 2026-10-09.",
             "Your order ORD-48213 was shipped on 2026-10-07."]:
    print(grounded(text, result), text)
```

```text
True Your order ORD-48213 was shipped on 2026-10-09.
False Your order ORD-48213 was shipped on 2026-10-07.
```

İkinci örnek yanıt, araç sonucunda olmayan bir tarih yazıyor ve denetim
onu yakalıyor. Önceki modülde kaynak gösteren cevapları denetlediğimiz
fikir burada da geçerli: **araç sonucu, cevabın kaynağıdır.**

## Özet

- Araç, modelin bilmediği ya da yapamadığı bir iş için programın sunduğu
  fonksiyondur; modele yalnızca adı, açıklaması ve argümanları gider.
- Model aracı çalıştırmaz, bir çağrı ister; çalıştıran ve sonucu geri
  veren programdır.
- Her çağrı çalıştırılmadan önce doğrulanır: izin listesi, argüman
  kalıpları, geri alınamaz işlerde onay.
- Hatalı çağrı programı çökertmez; hata sonucu modele geri gider.
- Araç kullanmak en az bir çağrı daha demektir.
- Son cevabı araç sonucuyla karşılaştır; tarih, durum, tutar gibi
  yapılı bilgiler kodla denetlenebilir.
