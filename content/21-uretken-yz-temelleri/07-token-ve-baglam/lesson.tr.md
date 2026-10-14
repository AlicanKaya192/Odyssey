# Token, Bağlam Penceresi ve Maliyet

Önceki bölümün sonunda gördük: sohbet API'leri durumsuz, geçmiş her
çağrıda yeniden gönderiliyor. Bu bölüm bunun üç sonucunu ölçüyor: model
metni **token** olarak okur, okuyabileceği token sayısının bir **sınırı**
vardır ve ücretli bir serviste her token'ın bir **bedeli** vardır. Bunları
ölçmek için alıştırmalarda da kullanacağımız küçük bir araç tanıtıyoruz.

## Kayıtlı yanıtlı istemci

Program çevrimdışı çalışıyor ve gerçek bir modele bağlanmıyor. Bu yüzden
`llm_client.py` adında, sohbet API'si gibi davranan bir istemci yazdık:

- `ChatClient(script)`: her çağrıya `script` listesindeki **sıradaki
  yanıtla** cevap veriyor. Yanıtlar önceden yazıldı; bir modelden
  alınmadılar, yani **örnek yanıtlardır**, bir modelin ölçümü değildir.
- `client.chat(messages, max_tokens=...)`: mesaj listesini denetliyor,
  token sayıyor, bağlam penceresini aşan isteği reddediyor, cevabı
  `max_tokens`'ta kesiyor ve `Reply` döndürüyor (metin, bitiş nedeni, giren
  ve çıkan token sayısı).
- `client.calls`: yapılan her çağrının kaydı. Programının modele **ne
  gönderdiğini** buradan denetleyebilirsin.

Modelin ne cevap verdiği önceden belli olduğu için burada öğrenilen şey
modelin kendisi değil, **onu kullanan programın** doğru çalışması: doğru
mesajları göndermek, sınırları gözetmek, maliyeti hesaplamak.

## Token saymak

Gerçek modeller metni NLP patikasında gördüğümüz BPE gibi yöntemlerle
parçalara böler; her modelin kendi parçalayıcısı (tokenizer) vardır ve
sayılar modelden modele değişir. `llm_client` **basitleştirilmiş** bir
sayaç kullanıyor: her noktalama işareti bir token, her kelime başladığı
her dört karakter için bir token. Gerçek sayılar farklıdır ama büyüklükleri
benzer; buradaki her hesap aynı mantıkla gerçek sayılarla yapılır.

```python
from llm_client import count_tokens, count_message_tokens

for text in ["cat", "capital", "Hello, world!", "internationalization",
             "What is the capital of Peru?",
             "Peru'nun başkenti neresidir?"]:
    print(count_tokens(text), text)
```

```text
1 cat
2 capital
6 Hello, world!
5 internationalization
8 What is the capital of Peru?
9 Peru'nun başkenti neresidir?
```

Uzun kelimeler daha çok token tutuyor. Aynı soru Türkçede daha az ama
daha uzun kelimeyle yazılıyor ve bu sayaçta 9 token tutuyor
(İngilizcesi 8). Gerçek parçalayıcılarda da aynı metnin token sayısı dile
göre değişir.

Bir mesaj listesinin token sayısına, içeriklerin yanında her mesajın rol
işaretleri de eklenir (`count_message_tokens`; bu sayaçta mesaj başına 4,
cevabın başlangıcı için 2).

## Bağlam penceresi

Bir model bir çağrıda sınırlı sayıda token işleyebilir: **bağlam
penceresi** (context window). Giren mesajlar ile üretilecek cevabın toplamı
pencereye sığmalıdır. Sığmayan istek reddedilir:

```python
from llm_client import ChatClient, ContextLengthError

messages = [
    {"role": "system", "content": "You are a helpful travel assistant."},
    {"role": "user", "content": "What is the capital of Peru?"},
]
print("input tokens", count_message_tokens(messages))
client = ChatClient(["The capital of Peru is Lima."], context_window=60)
reply = client.chat(messages, max_tokens=20)
print(reply.text, reply.finish_reason, reply.input_tokens,
      reply.output_tokens)
try:
    client.chat(messages, max_tokens=50)
except ContextLengthError as error:
    print("error:", error)
```

```text
input tokens 29
The capital of Peru is Lima. stop 29 8
error: 29 input + 50 output tokens > window of 60
```

İlk çağrıda 29 giren + 20 çıkan token 60'lık pencereye
sığıyor. İkinci çağrıda cevaba 50 token yer ayırmak toplamı pencerenin
üstüne çıkarıyor ve istek daha model çalışmadan reddediliyor. Gerçek
modellerin pencereleri binlerce, hatta yüz binlerce token'dır; ama uzun
belgeler ve uzun sohbetler oraya da sığmayabilir.

## Sohbet uzadıkça

Bir seyahat asistanıyla sekiz mesajlık bir sohbet yapalım. Her çağrıda
bütün geçmişi gönderiyoruz ve her çağrının giren token sayısını
kaydediyoruz. Son soru, ilk mesajda söylenen adı soruyor; o yanıt,
gönderilen mesajlarda adın geçip geçmediğine göre değişen bir fonksiyon:

```python
QUESTIONS = [
    "My name is Ada and I am planning a trip to Peru.",
    "What is the capital of Peru?",
    "Which currency do they use there?",
    "Is it cold in Lima in July?",
    "What should I pack for a week?",
    "How long is a flight from Madrid to Lima?",
    "Do I need a visa?",
    "What is my name?",
]


def name_reply(messages):
    seen = any("Ada" in m["content"] for m in messages[:-1])
    return "Your name is Ada." if seen else "I do not know your name."


REPLIES = [
    "Nice to meet you, Ada. Peru is a great choice.",
    "The capital of Peru is Lima.",
    "Peru uses the sol.",
    "July is winter in Lima, so it is cool and often cloudy.",
    "Pack layers, a light jacket and comfortable shoes.",
    "A direct flight takes about twelve hours.",
    "It depends on your passport; check the official embassy site.",
    name_reply,
]
SYSTEM = {"role": "system", "content": "You are a helpful travel assistant."}


def run_chat(keep=None):
    client = ChatClient(REPLIES)
    history = [SYSTEM]
    replies = []
    for question in QUESTIONS:
        history.append({"role": "user", "content": question})
        sent = history if keep is None else [SYSTEM] + history[1:][-keep:]
        reply = client.chat(sent, max_tokens=100)
        history.append({"role": "assistant", "content": reply.text})
        replies.append(reply)
    return client, replies


client, replies = run_chat()
inputs = [r.input_tokens for r in replies]
print(inputs)
print("input tokens in total", sum(inputs))
print("last answer:", replies[-1].text)
```

```text
[35, 66, 92, 113, 147, 183, 211, 241]
input tokens in total 1088
last answer: Your name is Ada.
```

Her çağrının girdisi bir öncekinden büyük: geçmiş biriktikçe aynı mesajlar
tekrar tekrar gönderiliyor. Sekiz kısa mesajlık bu sohbette bile toplam
giren token sayısı, son çağrınınkinin 4,5 katı. Sohbet uzadıkça
toplam kabaca mesaj sayısının karesiyle büyür: $n$ mesajlık sohbette
1, 2, …, $n$ mesaj gönderilir, toplamı $n(n+1)/2$.

## Geçmişi kırpmak

En basit çare, sistem mesajını tutup yalnızca son birkaç mesajı
göndermek. Aynı sohbeti son 4 mesajla tekrarlayalım:

```python
trimmed, short_replies = run_chat(keep=4)
inputs = [r.input_tokens for r in short_replies]
print(inputs)
print("input tokens in total", sum(inputs))
print("last answer:", short_replies[-1].text)
```

```text
[35, 66, 74, 64, 72, 87, 81, 75]
input tokens in total 554
last answer: I do not know your name.
```

Token sayısı artık belli bir düzeyde duruyor ve toplam belirgin biçimde
düşüyor. Ama bedeli var: ad ilk mesajda söylenmişti ve kırpılan geçmişte
artık yok; son soruya "bilmiyorum" cevabı geliyor. Kırpmak **unutmak**
demektir. Pratikte iki yol birleştirilir: önemli bilgiler (kişinin adı,
tercihleri, verilen kararlar) ayrı tutulup sistem mesajına eklenir ya da
eski kısım kısa bir özetle değiştirilir. Modül 2'nin Sohbet Geçmişi ve
Bellek bölümü bunları ayrıntısıyla ele alıyor.

## Maliyet

Ücretli servisler genellikle giren ve çıkan token'ları ayrı fiyatlar;
çıkan token çoğu zaman daha pahalıdır. Aşağıdaki fiyatlar **örnek**:
milyon giren token için 0,50, milyon çıkan token için 1,50 birim. Gerçek
fiyatlar servisten servise ve zamanla değişir.

```python
PRICE_IN, PRICE_OUT = 0.50, 1.50


def cost(replies):
    tokens_in = sum(r.input_tokens for r in replies)
    tokens_out = sum(r.output_tokens for r in replies)
    return (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000


full, short = cost(replies), cost(short_replies)
print(f"full history {full:.6f}  trimmed {short:.6f}")
print(f"per 100000 chats: {full * 100_000:.2f} vs {short * 100_000:.2f}")
```

```text
full history 0.000690  trimmed 0.000425
per 100000 chats: 68.95 vs 42.55
```

Tek bir sohbetin bedeli küçük görünüyor; ama bir uygulama günde binlerce
sohbet yapar. Ölçek büyüdükçe "her çağrıda neyi gönderiyorum?" sorusu
doğrudan bir maliyet sorusuna dönüşür. Uzun bir sistem mesajı, gereksiz
geçmiş ya da gereksiz uzun cevaplar her çağrıda yeniden ödenir. (`max_tokens`
kendisi ödenmez, yalnızca pencerede yer ayırır; ücret genellikle üretilen
token için.)

## Özet

- Model metni token olarak okur; token sayısı kelime uzunluğuna ve dile
  göre değişir. Bu bölümdeki sayaç basitleştirilmiş, gerçek sayılar
  modelden modele farklı.
- Giren ve çıkan token'ların toplamı bağlam penceresine sığmalı; sığmayan
  istek reddedilir.
- Sohbet geçmişi her çağrıda yeniden gönderildiği için toplam token sayısı
  mesaj sayısıyla hızla büyür.
- Geçmişi kırpmak token'ı azaltır ama bilgiyi de kaybettirir; önemli
  bilgiler ayrı tutulmalı.
- Maliyet = giren token × giriş fiyatı + çıkan token × çıkış fiyatı;
  her gereksiz token her çağrıda yeniden ödenir.
