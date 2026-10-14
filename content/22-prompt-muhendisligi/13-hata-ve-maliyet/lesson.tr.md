# Hatalar, Yeniden Deneme ve Maliyet

Şimdiye kadar her çağrı bir cevap döndürdü. Gerçek bir serviste öyle
olmaz: istek sınırı dolar, servis bir an cevap veremez, istek bağlam
penceresine sığmaz, cevap yarıda kesilir. Bir LLM uygulamasının kodunun
büyük bir kısmı bu durumlarla uğraşır. Bu bölümde hangi hatanın yeniden
denendiğini, ne kadar bekleneceğini, kesilen cevabın neye mal olduğunu ve
maliyeti düşüren basit bir önbelleği ölçüyoruz.

Bu bölümdeki hatalar da kayıtlı yanıtlı istemcinin senaryosundan geliyor:
senaryoya bir hata nesnesi konursa o çağrıda o hata fırlatılıyor. Hata
adları ve mesajları **örnek**; gerçek servislerin hata türleri ve kodları
birbirinden farklı.

## Hangi hata yeniden denenir?

Hataları iki gruba ayırmak gerekir:

- **Geçici hatalar:** istek sınırı doldu (çoğu serviste HTTP 429),
  servis bir an cevap veremedi (5xx). Aynı istek biraz sonra başarılı
  olabilir; yeniden denemek mantıklı.
- **Kalıcı hatalar:** istek bağlam penceresine sığmıyor, mesaj listesi
  bozuk, kimlik bilgisi yanlış. Aynı isteği ne kadar tekrar gönderirsen
  gönder aynı hatayı alırsın; yeniden denemek yalnızca zaman kaybettirir.
  İsteği değiştirmek gerekir.

Yeniden denerken her seferinde bekleme süresini ikiye katlamak yaygın bir
yoldur: **üstel geri çekilme** (exponential backoff). Kodda beklemeyi
`time.sleep` yerine dışarıdan verilen bir fonksiyonla yapıyoruz; böylece
örnekte gerçekten beklemeden hangi sürelerin beklendiğini görebiliyoruz:

```python
import time

from llm_client import ChatClient, ContextLengthError, RateLimitError, ServerError

RETRYABLE = (RateLimitError, ServerError)


def call_with_retry(client, messages, attempts=4, base=1.0, sleep=time.sleep):
    for attempt in range(attempts):
        try:
            return client.chat(messages, max_tokens=60)
        except RETRYABLE:
            if attempt == attempts - 1:
                raise
            sleep(base * 2 ** attempt)


MESSAGES = [{"role": "user", "content": "Where is my order ORD-48213?"}]
CASES = {
    "two failures": [RateLimitError("429 too many requests"),
                     ServerError("503 unavailable"),
                     "Your parcel left the depot today."],
    "always busy": [RateLimitError("429 too many requests")] * 4,
}
for name, script in CASES.items():
    waits = []
    try:
        reply = call_with_retry(ChatClient(script), MESSAGES, sleep=waits.append)
        result = reply.text
    except RateLimitError as error:
        result = f"gave up ({error})"
    print(f"{name}: waits {waits} -> {result}")

LONG = [{"role": "user", "content": "Where is my order? " * 8}]
waits = []
try:
    call_with_retry(ChatClient(["never sent"], context_window=60), LONG,
                    sleep=waits.append)
except ContextLengthError as error:
    print(f"too long: waits {waits} -> {error}")
```

```text
two failures: waits [1.0, 2.0] -> Your parcel left the depot today.
always busy: waits [1.0, 2.0, 4.0] -> gave up (429 too many requests)
too long: waits [] -> 62 input + 60 output tokens > window of 60
```

İlk senaryoda iki geçici hatadan sonra üçüncü deneme cevap aldı; araya 1
ve 2 saniyelik beklemeler girdi. İkinci senaryoda servis hep meşgul: 1, 2
ve 4 saniye bekledikten sonra dördüncü denemede de hata gelince fonksiyon
pes etti ve hatayı yukarı iletti. Deneme sayısının bir sınırı olmalı;
yoksa uygulama sonsuza kadar bekler. Üçüncü durumda istek pencereye
sığmıyor; bu hata `RETRYABLE` içinde olmadığı için hiç beklenmeden hemen
yukarı çıktı. Onu çözmek için isteği kısaltmak gerekir (geçmişi kırpmak,
belgeyi parçalamak).

Bazı servisler 429 cevabında ne kadar beklenmesi gerektiğini de söyler
(`Retry-After` başlığı). Söylüyorsa kendi hesabın yerine o süreye uy.

## Herkes aynı anda denerse: rastgele bekleme

Servis bir an durduğunda onu kullanan bütün istemciler aynı anda hata
alır. Hepsi aynı kuralla "1 saniye bekle" derse, 1 saniye sonra hepsi
aynı anda yeniden gelir ve servis yine dolar. Bunun çaresi beklemeye
rastgelelik katmak: **jitter**. Aşağıda 100 istemci aynı anda hata
alıyor; servis her 0,1 saniyede en fazla 20 istek kabul ediyor:

```python
import random

CLIENTS, CAPACITY, SLOT = 100, 20, 0.1


def retry_times(rng, jitter, base=1.0):
    if jitter:
        return [rng.uniform(0, base) for _ in range(CLIENTS)]
    return [base] * CLIENTS


def rejected(times):
    slots = {}
    for t in times:
        slots[int(t / SLOT)] = slots.get(int(t / SLOT), 0) + 1
    return max(slots.values()), sum(max(0, n - CAPACITY) for n in slots.values())


rng = random.Random(1)
for jitter in (False, True):
    busiest, failed = rejected(retry_times(rng, jitter))
    label = "with jitter" if jitter else "no jitter"
    print(f"{label}: busiest {SLOT} s {busiest} requests, rejected again {failed}")
```

```text
no jitter: busiest 0.1 s 100 requests, rejected again 80
with jitter: busiest 0.1 s 16 requests, rejected again 0
```

Jitter olmadan 100 istemcinin hepsi aynı 0,1 saniyeye düştü ve 80'i
yeniden reddedildi. Bekleme 0 ile 1 saniye arasında rastgele seçilince en
kalabalık dilimde 16 istek kaldı ve bu tohumda hiçbiri reddedilmedi.
Yeniden deneme kodunda bekleme `base * 2 ** attempt` yerine
`random.uniform(0, base * 2 ** attempt)` olur.

## Yeniden denemenin tehlikesi: iki kez yapılan iş

Modele "şu soruyu cevapla" demeyi tekrar etmek zararsızdır. Ama bir araç
çağrısı bir şeyi **değiştiriyorsa** (siparişi iptal etmek, para iadesi
başlatmak) onu yeniden denemek işi iki kez yapabilir. Zaman aşımı daha da
sinsi: cevap gelmedi diye istek işlenmedi sanılır, oysa işlenmiş ve cevap
yolda kaybolmuş olabilir.

Çözüm, değiştiren her isteğe bir **istek kimliği** (idempotency key)
koymak: aynı kimlikle gelen ikinci istek yeniden işlenmez, ilk sonucu
döndürür. Kısacası yeniden deneme yalnızca tekrarlanması güvenli olan
işlerde kendiliğinden yapılır.

## Kesilen cevap iki kez ödenir

Cevap `max_tokens` sınırına çarparsa yarıda kesilir ve `finish_reason`
`"length"` olur. JSON bekleyen bir program kesilmiş JSON'u ayrıştıramaz.
Yaygın bir çare sınırı büyütüp yeniden istemek. Ama her yeni istekte
prompt baştan gönderilir:

```python
import json

from llm_client import ChatClient

REPLY = ('{"category": "returns", "order": "ORD-10077", '
         '"summary": "The customer wants to return the tent."}')
SYSTEM = "Answer with JSON: category, order, summary."
MESSAGES = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Can I return the tent from ORD-10077?"}]


def ask_json(client, max_tokens, tries=3):
    paid_in = paid_out = 0
    for _ in range(tries):
        reply = client.chat(MESSAGES, max_tokens=max_tokens)
        paid_in += reply.input_tokens
        paid_out += reply.output_tokens
        if reply.finish_reason != "length":
            return json.loads(reply.text), paid_in, paid_out
        print(f"  cut at {max_tokens}: ...{reply.text[-20:]}")
        max_tokens *= 2
    raise ValueError("the answer did not fit")


for start in (12, 48):
    print(f"max_tokens {start}:")
    data, paid_in, paid_out = ask_json(ChatClient([REPLY] * 3), start)
    print(f"  {data['category']}, paid {paid_in} in + {paid_out} out")
```

```text
max_tokens 12:
  cut at 12: ...egory": "returns", "
  cut at 24: ...der": "ORD-10077", "
  returns, paid 108 in + 78 out
max_tokens 48:
  returns, paid 36 in + 42 out
```

12 token'la başlayan istek iki kez kesildi: önce 12, sonra 24 token'da.
Üçüncü çağrı 48 token'la sığdı. Toplamda 108 giren ve 78 çıkan token
ödendi; prompt üç kez gönderildi ve kesilen iki cevabın token'ları da
üretildi (ücret genellikle üretilen token için). Baştan 48 ile başlayan
istek tek çağrıda 36 giren + 42 çıkan token'la bitti. `max_tokens` cevabın
beklenen boyuna göre seçilir: çok küçükse cevap kesilip yeniden istenir,
büyük bir sınır ise ücret getirmez, yalnızca pencerede yer ayırır.
Deneme sayısı burada da sınırlı; cevap hiç sığmazsa fonksiyon hata
veriyor.

## Maliyet: önbellek

Maliyetin hesabını Üretken Yapay Zekâ Temelleri modülünde gördük: giren
token × giriş fiyatı + çıkan token × çıkış fiyatı. Bir uygulamada
maliyeti düşürmenin yolları büyük ölçüde önceki bölümlerde geçti: kısa
sistem mesajı, gereği kadar örnek, kırpılmış geçmiş, gereği kadar
`max_tokens`. Bir yol daha var: **aynı isteği iki kez göndermemek.**

Destek sayfasında beş hazır soru düğmesi olduğunu düşünelim. 100 isteğin
60'ı bu düğmelerden, 40'ı müşterilerin kendi yazdığı mesajlardan
(`shop_data`'daki 40 mesaj) geliyor. Bu trafik ders için üretildi, gerçek
bir mağazanın ölçümü değil:

```python
import random

from llm_client import count_message_tokens
from shop_data import TICKETS

SYSTEM = ("You are the support assistant of an outdoor shop. Answer in at most "
          "three sentences. Never promise a refund, a delivery date or a discount.")
BUTTONS = ["How do I return an item?", "How long does a refund take?",
           "What does the warranty cover?", "Which payment methods do you accept?",
           "How much is shipping?"]
rng = random.Random(3)
traffic = [rng.choice(BUTTONS) for _ in range(60)] + [t["text"] for t in TICKETS]
rng.shuffle(traffic)


def messages_for(text):
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": text}]


cache, calls, sent, saved = {}, 0, 0, 0
for text in traffic:
    tokens = count_message_tokens(messages_for(text))
    key = (SYSTEM, text, 0.0)
    if key in cache:
        saved += tokens
        continue
    cache[key] = f"answer {len(cache)}"
    calls += 1
    sent += tokens
hits = len(traffic) - calls
print(f"{len(traffic)} requests, {calls} model calls, {hits} from cache")
print(f"input tokens sent {sent}, saved {saved}")
```

```text
100 requests, 45 model calls, 55 from cache
input tokens sent 2888, saved 3313
```

100 isteğin 55'i önbellekten cevaplandı ve modele yalnızca 45 çağrı
gitti: beş düğme sorusunun her biri bir kez, müşterilerin 40 mesajı birer
kez. Giren token'ların 3313'ü hiç gönderilmedi; gönderilen 2888'den fazla.
Önbelleğin işe yaraması için aynı istek gerçekten tekrar etmeli: müşterinin
kendi yazdığı mesajlar bu trafikte hiç tekrar etmedi. Anahtarın içinde
cevabı etkileyen her şey var: sistem mesajı, kullanıcının metni ve ayar
(sıcaklık). Sistem mesajı değişince eski cevaplar kendiliğinden geçersiz
olur. Cevabı müşterinin verisine bağlı olan bir istek (siparişinin durumu)
önbellekten başka birine verilmemeli; anahtarı o müşteriye özel olur ve
paylaşılmaz. Bazı servisler ayrıca aynı başlangıçla gelen istekler için
kendi ön ek önbelleğini sunar; koşulları servisten servise değişir.

## Pes edince ne olur?

Yeniden denemeler de bitebilir. O zaman programın çökmesi değil, kullanıcıya
dürüst bir mesaj göstermesi gerekir: "Şu anda cevap veremiyoruz, mesajınız
bir temsilciye iletildi." Bunun için:

- Toplam bekleme için bir **süre sınırı** koy. Kullanıcı 30 saniye
  beklemez; sıradaki bekleme sınırı aşacaksa beklemeden pes et.
- Pes edince **yedek cevap** ver ve isteği kaydet; bir insan sonradan
  bakabilsin.
- Hataları say. Geçici hata oranı birden artıyorsa sorun senin
  kodunda değil serviste olabilir; kalıcı hatalar artıyorsa sorun büyük
  ihtimalle senin isteklerinde.

## Özet

- Geçici hatalar (istek sınırı, servis hatası) yeniden denenir; kalıcı
  hatalar (pencereye sığmama, bozuk istek) denenmez, istek değiştirilir.
- Bekleme üstel büyür ve bir deneme sınırı vardır. Servis bekleme süresi
  söylüyorsa ona uyulur.
- Rastgele bekleme (jitter) aynı anda hata alan istemcilerin hep birlikte
  geri gelmesini önler.
- Bir şeyi değiştiren istek kendiliğinden yeniden denenmez ya da bir istek
  kimliği taşır; yoksa iş iki kez yapılabilir.
- Kesilen cevabı daha büyük sınırla yeniden istemek prompt'u yeniden
  ödetir; `max_tokens` beklenen cevaba göre seçilir.
- Önbellek aynı isteği ikinci kez göndermez; anahtar cevabı etkileyen her
  şeyi içermelidir.
- Pes edince program çökmez: süre sınırı, yedek cevap ve kayıt.
