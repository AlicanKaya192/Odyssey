# Adım Adım Düşündürmek

Bir müşteri soruyor: "189,90 avroluk bir çadır ve tanesi 12,50 avrodan
iki çift çorap aldım, bütün siparişte %10 indirim kodu kullandım; ne
ödeyeceğim?" Bu soruyu tek adımda cevaplamak zor; önce çorapların
tutarını, sonra toplamı, sonra indirimi bulmak gerekiyor. Modelden
cevaptan önce adımları yazmasını istemeye **adım adım düşündürmek**
(chain-of-thought, düşünce zinciri) denir. Bu bölümde böyle bir cevabı
programın nasıl kullanacağını görüyoruz: son cevabı ayrıştırmak, adımları
denetlemek ve en önemlisi, **kodla hesaplanabilen bir şeyi modele
bırakmamak**.

## Ne zaman işe yarar?

Araştırmalarda büyük modellerin çok adımlı aritmetik ve mantık
sorularında, cevaptan önce ara adımları yazdıklarında daha sık doğru
cevap verdiği gösterildi. Bunun iki yolu var: talimata "önce adımları
yaz, sonra cevabı ver" eklemek ya da az örnekli prompt'taki örnek
cevapları adımlarıyla birlikte yazmak.

Üç uyarı:

- **Her işte gerekmez.** Bir mesajı kategoriye koymak gibi tek adımlı
  işlerde fark etmeyebilir; ama token bedeli her zaman ödenir.
- **Bazı modeller zaten adım adım düşünür.** Cevaptan önce kendiliğinden
  uzun bir akıl yürütme üretecek şekilde eğitilmiş modellerde bu talimat
  gereksiz olabilir.
- **Yazılan adımlar doğru olmak zorunda değil.** Adımlar cevabı daha
  denetlenebilir yapar, ama kendileri de yanlış olabilir.

## Son cevabı ayrıştırmak

Adımlı bir cevabı programın kullanabilmesi için son cevabın sabit bir
yerde durması gerekir. Talimata "son satır `Answer: <sayı>` olsun"
yazarız. Aşağıdaki dört **örnek yanıt** bu soruya gelebilecek cevapları
temsil ediyor: doğru bir akıl yürütme, bir çifti unutan bir akıl
yürütme, çarpmada yanılan bir akıl yürütme ve son satırı unutan bir
cevap.

```python
import re

REPLIES = [
    "Socks: 2 * 12.50 = 25.00\nTotal: 189.90 + 25.00 = 214.90\n"
    "Discount: 214.90 * 0.10 = 21.49\n"
    "To pay: 214.90 - 21.49 = 193.41\nAnswer: 193.41",
    "Total: 189.90 + 12.50 = 202.40\n"
    "Discount: 202.40 * 0.10 = 20.24\n"
    "To pay: 202.40 - 20.24 = 182.16\nAnswer: 182.16",
    "Socks: 2 * 12.50 = 25.00\nTotal: 189.90 + 25.00 = 214.90\n"
    "Discount: 214.90 * 0.10 = 21.94\n"
    "To pay: 214.90 - 21.94 = 192.96\nAnswer: 192.96",
    "The tent and the socks cost 214.90 euros, so with the "
    "discount you pay about 193 euros.",
]


def final_answer(text):
    found = re.search(r"^Answer:\s*(\d+(?:\.\d+)?)\s*$", text, flags=re.M)
    return float(found.group(1)) if found else None


for reply in REPLIES:
    print(final_answer(reply))
```

```text
193.41
182.16
192.96
None
```

Dördüncü cevap muhtemelen doğru sonuca yakın, ama program onu
kullanamaz: "about 193" bir sayı değil bir tahmin. Son satır yoksa cevap
`None` olarak işaretlenir ve yeniden sorulur ya da bir insana gider.

## Adımları denetlemek

Adımlar yazıldığı için onları kodla denetleyebiliriz. `a + b = c`
biçimindeki her işlemi bulup yeniden hesaplayalım:

```python
STEP = re.compile(r"(\d+(?:\.\d+)?) ([-+*]) (\d+(?:\.\d+)?) = (\d+(?:\.\d+)?)")
OPS = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
       "*": lambda a, b: a * b}


def wrong_steps(text):
    wrong = []
    for a, op, b, c in STEP.findall(text):
        if abs(OPS[op](float(a), float(b)) - float(c)) > 0.005:
            wrong.append(f"{a} {op} {b} = {c}")
    return wrong


for reply in REPLIES:
    print(wrong_steps(reply))
```

```text
[]
[]
['214.90 * 0.10 = 21.94']
[]
```

Üçüncü cevaptaki çarpma hatası (`21.49` yerine `21.94`) yakalandı. Ama
ikinci cevap temiz çıktı, oysa sonucu yanlış: `189.90 + 12.50 = 202.40`
işlemi **doğru hesaplanmış**, yalnızca yanlış adım; ikinci çift çorap
unutulmuş. Adım denetleyicisi hesap hatasını bulur, akıl yürütme
hatasını bulamaz.

## Hesaplanabileni kod hesaplasın

Bu sorunun cevabı aslında hesaplanabilir: fiyatlar, adetler ve indirim
belliyse doğru tutarı program kendisi bulur. Modelin işi o zaman
hesaplamak değil, müşterinin mesajından **sayıları çıkarmak** olur
(Yapılı Çıktı ve Araç Çağırma bölümlerinde). Doğru tutarı kodla bulup
cevapları onunla karşılaştıralım:

```python
def order_total(items, discount):
    subtotal = sum(price * count for price, count in items)
    return round(subtotal * (1 - discount), 2)


expected = order_total([(189.90, 1), (12.50, 2)], 0.10)
print("expected", expected)
for reply in REPLIES:
    answer = final_answer(reply)
    print(answer, "ok" if answer == expected else "wrong or missing")
```

```text
expected 193.41
193.41 ok
182.16 wrong or missing
192.96 wrong or missing
None wrong or missing
```

Dört cevaptan yalnızca biri doğru tutarı veriyor ve kod üç sorunu da
ayırıyor: unutulan adımı, hesap hatasını ve eksik son satırı. Kural
şu: **para, tarih, birim çevirme gibi kesin hesapları modele bırakma.**
Model işin dil tarafını yapsın (sayıları bulmak, cevabı yazmak), hesabı
kod yapsın.

## Birkaç cevap, çoğunluk oyu

Hesaplanamayan ama tek doğru cevabı olan sorularda bir başka yol, aynı
soruyu sıfırdan büyük bir sıcaklıkla birkaç kez sorup son cevaplarda
**çoğunluk oyu** almak (önceki modülde gördüğümüz tutarlılık fikri).
Aşağıdaki beş değer beş ayrı denemenin örnek son cevapları:

```python
from collections import Counter

from llm_client import count_tokens

samples = [193.41, 193.41, 182.16, 193.41, None]
votes = Counter(a for a in samples if a is not None)
answer, count = votes.most_common(1)[0]
print(answer, count, "of", len(samples))
print("tokens: steps", count_tokens(REPLIES[0]),
      "direct", count_tokens("Answer: 193.41"))
```

```text
193.41 3 of 5
tokens: steps 60 direct 6
```

Çoğunluk 193,41'de, beş denemenin üçüyle. Bu yol, hatalar dağınıkken
güvenilirliği artırır; ama aynı hatayı tekrar tekrar yapan bir modelde
çoğunluk da yanlış olur. Bedeli de büyük: beş deneme beş çağrı, ve adımlı
bir cevap doğrudan cevabın 10 katı token. Adım adım düşündürmek
ve çoğunluk oyu, ancak hatanın bedeli bu token'lardan büyükse değer.

## Adımları kime gösterirsin?

Adımlar programın denetlemesi içindir; müşteriye çoğu zaman yalnızca son
cevap gösterilir. Adımlarda yanlış bir ara sonuç, iç bir kural ya da
müşteriye yazılmaması gereken bir bilgi bulunabilir. Son satırı ayrı
ayrıştırmanın bir faydası da budur.

## Özet

- Adım adım düşündürmek çok adımlı sorularda yardımcı olabilir; her işte
  gerekmez ve token bedeli büyüktür.
- Son cevabı sabit bir satıra (`Answer: ...`) koydur ve yalnızca onu
  ayrıştır; satır yoksa cevabı kullanma.
- Adımlardaki işlemleri kodla yeniden hesaplamak hesap hatalarını bulur,
  akıl yürütme hatalarını bulamaz.
- Kesin hesapları (para, tarih, birim) kod yapsın; model sayıları
  çıkarsın.
- Çoğunluk oyu dağınık hataları azaltır ama çağrı sayısını katlar.
