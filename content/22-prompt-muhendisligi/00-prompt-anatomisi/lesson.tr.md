# Bir Promptun Anatomisi

Bir dil modeline gönderdiğin metne **prompt** (istem) denir. Önceki
modülde sohbet API'sinin bir mesaj listesi aldığını, token saydığını ve
her çağrının bir bedeli olduğunu gördük. Bu modülün konusu o listenin
içi: modelden ne istediğini nasıl yazacağın ve gelen cevabı nasıl
kullanacağın. Bu bölümde bir promptu parçalarına ayırıyoruz, her parçanın
ne işe yaradığına ve kaç token tuttuğuna bakıyoruz ve cevabın her zaman
beklediğin biçimde gelmediğini görüyoruz.

## Bu modülde nasıl çalışacağız

Program çevrimdışı ve gerçek bir modele bağlanmıyor. Önceki modüldeki
kayıtlı yanıtlı istemciyi (`llm_client.py`) kullanmaya devam ediyoruz:
`ChatClient(script)` her çağrıya listedeki sıradaki yanıtla cevap veriyor.
Bu yanıtlar önceden yazıldı; bir modelden alınmadılar, yani **örnek
yanıtlardır**. Bu yüzden derste "şu prompt daha iyi cevap verdi" gibi bir
ölçüm yok ve olamaz.

Burada iki şeyi öğreneceğiz:

- **Prompt yazmanın ilkeleri.** Bunlar pek çok modelde işe yarayan
  alışkanlıklar, ama bir ilkenin senin modelinde ne kadar fark yarattığını
  ancak kendi modelinde, kendi örneklerinle ölçerek öğrenebilirsin.
  Promptları değerlendirme bölümü bunun nasıl yapılacağını gösteriyor.
- **Modelin etrafındaki program.** Promptu kuran, cevabı ayrıştıran,
  doğrulayan, hatada yeniden deneyen, maliyeti tutan kod. Bu kısım
  modelden bağımsız ve burada gerçekten çalıştırılıp ölçülüyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Promptu kur</span>
    <span class="arrow">→</span>
    <span class="node acc">Örnek yanıtlarla programı sına</span>
    <span class="arrow">→</span>
    <span class="node">Kendi modelinde ölç</span>
  </div>
  <figcaption>Program burada sınanıyor; promptun etkisi senin modelinde, senin değerlendirme kümende ölçülür.</figcaption>
</figure>

## Prompt bir mesaj listesidir

Sohbet API'sinde prompt tek bir metin değil, rolleri olan mesajlardan
oluşan bir listedir:

- `system`: modelin rolü ve uyacağı kurallar. Sohbetin başında bir kez
  yazılır, her çağrıda yeniden gönderilir.
- `user`: kullanıcının mesajı ya da programın modele verdiği iş.
- `assistant`: modelin önceki cevapları (geçmiş ya da örnek olarak).

## Promptun parçaları

İyi bir promptta çoğu zaman şu parçalar bulunur. Hepsi her promptta
gerekmez, ama eksik olan parçayı model kendi tahminiyle doldurur:

<figure class="fig anat">
  <div class="anat-row"><span>Rol</span><span>Model kim gibi davranacak: "bir mağazanın destek asistanısın"</span></div>
  <div class="anat-row"><span>Görev</span><span>Ne yapılacak: "mesajı bir kategoriye koy"</span></div>
  <div class="anat-row"><span>Bağlam</span><span>İş için gereken bilgi: kategorilerin listesi, kurallar, belgeler</span></div>
  <div class="anat-row"><span>Biçim</span><span>Cevap nasıl görünecek: "yalnızca kategori adı, küçük harfle"</span></div>
  <div class="anat-row"><span>Girdi</span><span>Bu çağrıda işlenecek veri: müşterinin mesajı</span></div>
</figure>

Sonraki bölümlerde iki parça daha ekleyeceğiz: **örnekler** (az örnekli
prompt) ve **kısıtlar** (uzunluk, ton, yasaklar). Bir outdoor mağazasının
destek mesajlarını sınıflandıran bir prompt kuralım. Sabit parçalar sistem
mesajına, değişen girdi kullanıcı mesajına gidiyor:

```python
from llm_client import count_tokens, count_message_tokens

PARTS = {
    "role": "You are a support assistant for an outdoor gear shop.",
    "task": "Put the customer message into one category.",
    "labels": "Categories: shipping, returns, refunds, warranty, payment.",
    "format": "Answer with the category name only, in lower case.",
    "input": "My parcel should have arrived on Monday. Where is it?",
}


def build_messages(parts):
    system = " ".join(parts[k] for k in ["role", "task", "labels", "format"])
    return [{"role": "system", "content": system},
            {"role": "user", "content": parts["input"]}]


messages = build_messages(PARTS)
for name, text in PARTS.items():
    print(f"{name:7} {count_tokens(text):2} tokens")
print("message list", count_message_tokens(messages), "tokens")
```

```text
role    15 tokens
task    11 tokens
labels  19 tokens
format  14 tokens
input   17 tokens
message list 86 tokens
```

Promptu tek bir uzun metin olarak elle yazmak yerine parçalardan kurmanın
iki faydası var: hangi parçanın ne kadar yer tuttuğunu görüyorsun ve bir
parçayı değiştirip ötekilere dokunmadan deneyebiliyorsun. Promptu
sistemli iyileştirirken (bu modülün sonlarında) tam olarak bunu yapacağız.

## Göndermek ve cevabı denetlemek

Mesaj listesini istemciye gönderiyoruz. Cevap bu sefer tek kelime;
`max_tokens`'ı da ona göre küçük tutuyoruz:

```python
from llm_client import ChatClient

LABELS = ["shipping", "returns", "refunds", "warranty", "payment"]
client = ChatClient(["shipping"])
reply = client.chat(messages, max_tokens=5, temperature=0.0)
print(repr(reply.text), reply.finish_reason, reply.text in LABELS)

sent = client.calls[0]
print([m["role"] for m in sent["messages"]], sent["max_tokens"])
```

```text
'shipping' stop True
['system', 'user'] 5
```

Son satır önemli: `client.calls` programının modele **gerçekte ne
gönderdiğini** gösteriyor. Hatalı bir prompt çoğu zaman yanlış yazılmış
bir talimattan değil, programın yanlış mesajı göndermesinden çıkar: rol
yanlış, girdi eksik, sistem mesajı hiç eklenmemiş. Gerçek bir uygulamada
da giden isteği kayda geçirmek ilk hata ayıklama aracıdır.

Sınıflandırmada `temperature=0.0` yazdık: aynı mesaja her seferinde aynı
cevap gelmesini istiyoruz. Sıcaklık sıfırken bile gerçek modellerin her
zaman birebir aynı cevabı vereceğinin garantisi yoktur; ama yaratıcı metin
istemediğimiz yerde düşük sıcaklık doğal seçimdir.

## Cevap beklediğin biçimde gelmeyebilir

"Yalnızca kategori adı" dedik, ama bir model bu talimata her zaman uymaz:
büyük harfle başlar, nokta koyar, bir cümle kurar ya da iki kategori
arasında kalır. Aşağıdaki altı yanıt bu tür durumları temsil eden **örnek
yanıtlar**. İki ayrıştırıcıyı karşılaştıralım: biri cevabı yalnızca
temizleyip listede arıyor (katı), öteki listedeki ilk kategori adını
metnin herhangi bir yerinde arıyor (gevşek):

```python
EXAMPLE_REPLIES = ["shipping", "Shipping.", " refunds\n",
                   "The category is returns.",
                   "warranty, maybe payment", "I would say shipping."]


def strict(text):
    label = text.strip().lower().rstrip(".!")
    return label if label in LABELS else "needs_review"


def lenient(text):
    found = [label for label in LABELS if label in text.lower()]
    return found[0] if found else "needs_review"


for text in EXAMPLE_REPLIES:
    print(f"{text!r:27} {strict(text):13} {lenient(text)}")
```

```text
'shipping'                  shipping      shipping
'Shipping.'                 shipping      shipping
' refunds\n'                refunds       refunds
'The category is returns.'  needs_review  returns
'warranty, maybe payment'   needs_review  warranty
'I would say shipping.'     needs_review  shipping
```

Katı ayrıştırıcı ilk üç yanıtı kurtarıyor; boşluk, büyük harf ve sondaki
nokta zararsız farklar. Kalan üçünü `needs_review` (incelenmeli) diye
ayırıyor. Gevşek ayrıştırıcı her yanıta bir kategori veriyor; cümle
kuran iki yanıtta makul bir kategori buluyor, ama
`"warranty, maybe payment"` için **emin olmadığı halde** `warranty`
seçiyor. Model iki kategori arasında kalmıştı ve bu bilgi kayboldu;
gevşek ayrıştırıcı hangi cevabın şüpheli olduğunu artık söyleyemiyor.

Ders şu: cevabın biçimini prompt'ta açıkça istemek gerekir ama yetmez;
program gelen cevabı **doğrulamalıdır**. Doğrulanamayan cevabı tahminle
düzeltmek yerine ayırmak, ya da hata mesajıyla yeniden sormak (Yapılı
Çıktı bölümünde) daha güvenlidir.

## Sabit kısım her çağrıda ödenir

Sınıflandırıcı binlerce mesaj işleyecekse sistem mesajı her çağrıda
yeniden gönderilir. Değişen tek şey girdi:

```python
INPUTS = ["Where is my parcel?",
          "The zip of my tent broke after one year.",
          "Can I pay in three instalments?"]
fixed = count_tokens(messages[0]["content"])
for text in INPUTS:
    total = count_message_tokens(build_messages({**PARTS, "input": text}))
    print(f"{total:3} tokens, system part {fixed} ({fixed / total:.0%})")
print("system tokens for 10000 messages:", fixed * 10000)
```

```text
 76 tokens, system part 59 (78%)
 81 tokens, system part 59 (73%)
 79 tokens, system part 59 (75%)
system tokens for 10000 messages: 590000
```

Kısa mesajlarda giden token'ların %73–78'i sabit kısım. Bu, sistem mesajını
kısa tutmak için bir sebep; ama gereken bir talimatı ya da bağlamı atmak
için sebep değil. Önce doğru çalışan promptu yaz, sonra gereksiz kelimeleri
ölçerek at.

## Özet

- Prompt, rolleri olan bir mesaj listesidir: `system`, `user`,
  `assistant`.
- İyi bir promptun parçaları rol, görev, bağlam, biçim ve girdi;
  eksik parçayı model tahminle doldurur.
- Promptu parçalardan kurmak, parçaları ayrı ayrı ölçmeyi ve değiştirmeyi
  kolaylaştırır.
- `client.calls` gibi bir kayıtla programın gerçekte ne gönderdiğine bak.
- Biçimi istemek yetmez; cevabı doğrula, doğrulanamayanı ayır.
- Bu modüldeki yanıtlar örnek yanıt; bir ilkenin etkisini kendi modelinde
  ölçersin.
