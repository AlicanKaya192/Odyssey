# Sohbet Geçmişi ve Bellek

Sohbet API'si durumsuzdur: model önceki mesajları hatırlamaz, program
her çağrıda geçmişi yeniden gönderir. Önceki modülde (Token, Bağlam
Penceresi ve Maliyet) bunun bedelini ölçmüştük: toplam token mesaj
sayısıyla hızla büyüyor ve geçmişi kırpınca model ilk mesajdaki adı
unutuyor. Bu bölümde unutmadan kısaltmanın yollarına bakıyoruz: eski
mesajları **özetlemek** ve önemli bilgileri ayrı bir **bellekte**
tutmak. İkisini de aynı sohbette ölçüyoruz ve belleğin getirdiği yeni
sorumluluğu görüyoruz: kişisel veri.

## Üç yol, aynı sohbet

On mesajlık bir destek sohbeti. Müşteri adını ilk mesajda, sipariş
numarasını ikincide söylüyor; son mesajda siparişin nerede olduğunu
soruyor. Üç yol deniyoruz:

- **full:** bütün geçmiş her çağrıda.
- **last4:** yalnızca son dört mesaj.
- **memory:** son dört mesaj ve sistem mesajına eklenen bir bilgi
  listesi. Program her kullanıcı mesajından ad ve sipariş numarasını
  düzenli ifadeyle çıkarıp bellekte tutuyor.

```python
import re

from llm_client import count_message_tokens

SYSTEM = "You are the support assistant of an outdoor gear shop."
USER = [
    "Hi, my name is Ada.",
    "My order ORD-48213 has not arrived.",
    "It was supposed to come on Monday.",
    "Can you check where it is?",
    "I need the backpack for a trip.",
    "The trip starts on Friday.",
    "Is express delivery possible next time?",
    "How much does express delivery cost?",
    "Do you ship to Norway?",
    "So where is my order now?",
]
REPLY = "Thanks, I am looking into it."
FACTS = {"name": re.compile(r"my name is (\w+)", re.I),
         "order": re.compile(r"\bORD-\d{5}\b")}


def remember(memory, text):
    for key, pattern in FACTS.items():
        found = pattern.search(text)
        if found:
            memory[key] = found.group(found.lastindex or 0)


def conversation(strategy, keep=4):
    history, memory, sizes = [], {}, []
    for text in USER:
        remember(memory, text)
        history.append({"role": "user", "content": text})
        system = SYSTEM
        if strategy == "memory" and memory:
            facts = "; ".join(f"{k}={v}" for k, v in memory.items())
            system += " Known facts: " + facts
        recent = history if strategy == "full" else history[-keep:]
        sent = [{"role": "system", "content": system}] + recent
        sizes.append(count_message_tokens(sent))
        history.append({"role": "assistant", "content": REPLY})
    return sizes, sent


for strategy in ["full", "last4", "memory"]:
    sizes, sent = conversation(strategy)
    knows = "ORD-48213" in " ".join(m["content"] for m in sent)
    print(f"{strategy:6} total {sum(sizes):4} last {sizes[-1]:3} "
          f"knows the order: {knows}")
```

```text
full   total 1565 last 277 knows the order: True
last4  total  695 last  73 knows the order: False
memory total  847 last  89 knows the order: True
```

Bütün geçmiş sipariş numarasını biliyor ama on çağrıda 1565 token
harcıyor; son çağrı tek başına 277. Son dört mesaj toplamı 695'e
indiriyor ama son soruda sipariş numarası gönderilen mesajların hiçbirinde
yok: model "hangi sipariş?" diye sormak ya da tahmin etmek zorunda. Bellek
yolu numarayı tutuyor ve 847 token harcıyor, bütün geçmişin yarısından
biraz fazlası; bedeli her çağrıda sistem mesajına eklenen birkaç kelime.

## Özet: kısa ama kayıplı

Belleğin bir alternatifi, eski mesajları bir model çağrısıyla tek
cümleye özetleyip sistem mesajına koymak. Aşağıdaki özet bir **örnek
yanıt**; ilk dört mesajın yerine geçecek:

```python
from llm_client import ChatClient

client = ChatClient(["The customer Ada says her order is late "
                     "and asks where it is."])
old = [{"role": "user", "content": text} for text in USER[:4]]
instruction = {"role": "system",
               "content": "Summarize this support chat in one sentence."}
summary = client.chat([instruction] + old, max_tokens=40).text
print(summary)
print("order number kept:", "ORD-48213" in summary)
print(count_message_tokens(old), "tokens ->",
      count_message_tokens([{"role": "system", "content": summary}]))
```

```text
The customer Ada says her order is late and asks where it is.
order number kept: False
56 tokens -> 23
```

Özet mesajları kısalttı ama sipariş numarasını düşürdü. Özet bir modelin
yazdığı metin: neyi tutacağına o karar veriyor ve önemli bir ayrıntıyı
atabilir. Özetin bir de kendi çağrısı ve bedeli var. Bu yüzden iki yol
çoğu zaman birlikte kullanılır: **kesin bilgiler** (ad, sipariş
numarası, seçilen ürün) yapılı bir bellekte, **konuşmanın gidişi**
özette.

Bilgiyi düzenli ifade yerine modelle de çıkarabilirsin (Yapılı Çıktı
bölümündeki gibi JSON olarak); o zaman çıkan değeri yine doğrularsın.

## Bellek kişisel veri tutar

Bellek, müşteri hakkında bir kayıt demek. Neyi tuttuğuna dikkat etmen
gerekir: parola, kart numarası gibi bilgiler hiç saklanmamalı, gereken
bilgiler gerektiği kadar tutulmalı ve silinebilmeli. Saklamadan önce bir
süzgeç:

```python
SECRET = re.compile(r"password|passcode|\b\d{4} \d{4} \d{4} \d{4}\b", re.I)


def remember_safely(memory, text):
    if SECRET.search(text):
        return "not stored"
    remember(memory, text)
    return "stored"


memory = {}
for text in ["My name is Ada.",
             "My password is hunter2, can you reset it?",
             "My card is 1234 5678 9012 3456.",
             "Please check ORD-10077."]:
    print(remember_safely(memory, text), "|", text)
print(memory)
```

```text
stored | My name is Ada.
not stored | My password is hunter2, can you reset it?
not stored | My card is 1234 5678 9012 3456.
stored | Please check ORD-10077.
{'name': 'Ada', 'order': 'ORD-10077'}
```

Parola ve kart numarası içeren mesajlardan hiçbir şey belleğe girmedi.
Bu süzgeç basit: başka bir yazımı ("pass word", tireli kart numarası)
kaçırabilir; önceki modüldeki maskeleme dersinde gördüğümüz gibi
düzenli ifadeler eksik kalır. Kural yine de net: **bellek, müşterinin
söylediği her şeyi değil, işin gerektirdiğini tutar.**

Uzun süreli bellek (bir sonraki sohbette de hatırlamak) daha da
dikkat ister:

- Bellek **kullanıcıya bağlı** tutulur; bir müşterinin belleği başka
  bir müşterinin sohbetine asla girmez.
- Müşteri belleğini görebilmeli ve silebilmeli.
- Kayıtların bir **ömrü** olur; eski bilgiler kendiliğinden silinir.

## Özet

- Geçmişin tamamını göndermek pahalı, son mesajları tutmak bilgi
  kaybettirir.
- Kesin bilgileri (ad, sipariş numarası) yapılı bir bellekte tut ve
  sistem mesajına ekle; az token'la unutmayı önler.
- Özet konuşmanın gidişini kısaltır ama modelin yazdığı bir metindir;
  önemli bir ayrıntıyı düşürebilir.
- Belleğe neyin girdiğini süz: parola, kart numarası gibi bilgiler hiç
  saklanmaz.
- Uzun süreli bellek kullanıcıya bağlı, görülebilir, silinebilir ve
  süreli olmalı.
