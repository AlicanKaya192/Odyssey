# Bitirme: Belge Soru-Cevap Sistemi

Bu bölümde modülün LLM kısmındaki parçaları tek bir sistemde
birleştiriyoruz: mağazanın yardım makalelerinden soru cevaplayan bir
**belge soru-cevap** (document Q&A) sistemi. Her adım daha önce ayrı ayrı
gördüğümüz bir tekniğe dayanıyor:

<figure class="fig">
  <div class="flow">
    <span class="node">Maskele</span>
    <span class="arrow">→</span>
    <span class="node acc">İki aşamalı arama</span>
    <span class="arrow">→</span>
    <span class="node">Prompt + bütçe</span>
    <span class="arrow">→</span>
    <span class="node acc">Okuyucu</span>
    <span class="arrow">→</span>
    <span class="node">Doğrula + kaydet</span>
  </div>
  <figcaption>Soru önce maskelenir; en ilgili makalenin cümleleri bütçeye sığacak kadar prompt'a girer; cevap kaynağa karşı doğrulanır ve maliyetiyle kaydedilir.</figcaption>
</figure>

Sistemi önce kuracak, sonra 10'daki temel düzenekle aynı 27 soruda
karşılaştıracağız. Model yerine yine 10'daki **örnek okuyucu** çalışıyor;
ölçtüğümüz, onun etrafındaki sistem.

## Parçalar

Kişisel veriyi maskeleyen fonksiyon (14) ve **iki aşamalı arama**: önce
sorunun en ilgili makalesini buluyoruz (makale düzeyinde arama 09'da
ilk üçte %100 isabetliydi), sonra yalnızca o makalenin cümlelerini kaynak
olarak veriyoruz. Kaynaklar bir token bütçesini aşmıyor (07).

```python
import re
import textwrap
from retrieval import Index, by_article, by_sentence, QUESTIONS
from rag_tools import build_messages, make_reader, NOT_FOUND, rag
from llm_client import ChatClient, count_tokens

PATTERNS = {"EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
            "PHONE": r"\+?\(?\d[\d\s()-]{8,}\d",
            "ORDER": r"ORD-\d{5}"}


def mask(text):
    for label, pattern in PATTERNS.items():
        text = re.sub(pattern, f"[{label}]", text)
    return text


articles = Index(by_article())
SENTENCES = by_sentence()


def find_sources(question, budget=150):
    (doc, _), score = articles.search(question, 1)[0]
    sources, used = [], 0
    for d, sentence in SENTENCES:
        cost = count_tokens(sentence)
        if d == doc and used + cost <= budget:
            sources.append(((d, sentence), score))
            used += cost
    return sources


for (doc, text), _ in find_sources("Do gift cards expire?"):
    print(text)
```

```text
Gift cards are available for 25, 50 and 100 euros and are valid for 3 years.
They cannot be exchanged for cash.
You can use one gift card and one discount code per order.
```

## Doğrulama

Model cevabı yazdıktan sonra iki şeyi denetliyoruz (08): cevaptaki kaynak
numarası gerçekten var mı ve cevabın sayıları o kaynakta geçiyor mu?

```python
def verify(answer, sources):
    if answer == NOT_FOUND:
        return True
    cite = re.search(r"\[(\d+)\]", answer)
    if not cite or not 1 <= int(cite.group(1)) <= len(sources):
        return False
    source = sources[int(cite.group(1)) - 1][0][1]
    claims = re.findall(r"\d+", answer.replace(cite.group(0), ""))
    return all(c in re.findall(r"\d+", source) for c in claims)
```

## Sistem

```python
class DocQA:
    PRICE_IN, PRICE_OUT = 0.50, 1.50

    def __init__(self, min_overlap=2):
        self.min_overlap = min_overlap
        self.log = []

    def answer(self, question, reply=None):
        question = mask(question)
        sources = find_sources(question)
        client = ChatClient([reply or make_reader(self.min_overlap)])
        result = client.chat(build_messages(question, sources),
                             max_tokens=100)
        ok = verify(result.text, sources)
        text = result.text if ok else NOT_FOUND
        cost = (result.input_tokens * self.PRICE_IN
                + result.output_tokens * self.PRICE_OUT) / 1_000_000
        self.log.append({"question": question, "verified": ok,
                         "tokens": result.input_tokens, "cost": cost})
        return text


qa = DocQA()
for q in ["Do gift cards expire?",
          "I am ana@example.com, can I return worn boots?",
          "Do you sell bicycles?"]:
    print(textwrap.fill(qa.answer(q), 70))
print(qa.log[1]["question"])
```

```text
Gift cards are available for 25, 50 and 100 euros and are valid for 3
years. [1]
Boots that have been worn outdoors cannot be returned, so please try
them on indoors first. [5]
I could not find this in the sources.
I am [EMAIL], can I return worn boots?
```

İkinci soruda e-posta adresi aramadan ve kayıttan önce maskelendi;
kayıtta `[EMAIL]` görünüyor.

## Doğrulama işe yarıyor mu?

Örnek okuyucu cümleyi aynen kopyaladığı için hiç yanlış sayı yazmaz.
Doğrulamayı sınamak için okuyucunun yerine yanlış bir sayı içeren **kayıtlı
bir yanıt** veriyoruz (bir modelin yapabileceği türden bir hata):

```python
wrong = "Gift cards are valid for 5 years. [1]"
print(qa.answer("Do gift cards expire?", reply=wrong))
print("verified:", qa.log[-1]["verified"])
```

```text
I could not find this in the sources.
verified: False
```

Kaynakta "3 years" yazıyor; "5" orada yok. Doğrulama cevabı reddetti ve
kullanıcıya uydurma bir süre yerine "bulamadım" gitti.

## Temel düzenekle karşılaştırma

10'daki düzenek (`rag`: cümle düzeyinde arama, 3 kaynak) ile bitirme
sistemini aynı 27 soruda ölçelim:

```python
def evaluate(ask):
    counts = {"correct": 0, "abstain ok": 0, "wrong": 0, "missed": 0}
    for q in QUESTIONS:
        text = ask(q["q"])
        if q["key"] is None:
            group = "abstain ok" if text == NOT_FOUND else "wrong"
        elif text == NOT_FOUND:
            group = "missed"
        else:
            group = "correct" if q["key"] in text else "wrong"
        counts[group] += 1
    return counts


print("baseline", evaluate(lambda q: rag(q, 3, 2).text))
qa = DocQA()
print("capstone", evaluate(qa.answer))
tokens = sum(e["tokens"] for e in qa.log) / len(qa.log)
cost = sum(e["cost"] for e in qa.log)
print(f"capstone tokens per question {tokens:.0f}, cost {cost:.6f}")
```

```text
baseline {'correct': 15, 'abstain ok': 3, 'wrong': 2, 'missed': 7}
capstone {'correct': 15, 'abstain ok': 3, 'wrong': 0, 'missed': 9}
capstone tokens per question 154, cost 0.002820
```

Bitirme sistemi aynı sayıda doğru cevap verdi (15) ama **hiç yanlış cevap
vermedi**; temel düzenekte 2 yanlış vardı. Bedeli 2 kaçırma daha (7 → 9)
ve soru başına daha çok token (154; temel düzenekte 132), çünkü bütün bir
makalenin cümleleri gönderiliyor. Cevabı olmayan üç sorunun üçünde de
"bulamadım" dendi. Hangisinin tercih edileceği uygulamaya bağlı: bir
müşteri destek sisteminde yanlış cevap, "bulamadım" deyip kişiyi bir insana
yönlendirmekten pahalıdır. 27 soruda iki soruluk fark küçüktür (11); karar
için daha büyük bir değerlendirme kümesi gerekir.

## Bundan sonra

Bu sistemin zayıf yanları belli ve her biri modülde gördüğümüz bir
yönteme işaret ediyor:

- **Kaçan sorular** çoğunlukla kelime uyuşmazlığından: gömme ya da karma
  arama (09).
- **Okuyucu** gerçek bir modelle değiştirildiğinde cevaplar serbest metin
  olur: değerlendirme ifade eşleşmesinden insan ve model ile
  değerlendirmeye geçer (11), doğrulama daha da önem kazanır (08).
- **Küme küçük:** 27 soruyla iki sistem arasındaki küçük farklara
  güvenilmez (11); gerçek sorulardan büyük bir küme gerekir.
- **Davranış ince ayarı:** "kaynakta yoksa söyle" davranışı prompt'la
  yetmiyorsa ince ayar ya da LoRA (12, 13).

## Özet

- Belge soru-cevap sistemi: maskele → ara → bütçeye sığdır → prompt kur →
  cevap al → doğrula → kaydet → ölç.
- İki aşamalı arama (önce makale, sonra cümleleri) bu derlemde yanlış
  cevapları sıfırladı; bedeli birkaç kaçırma ve daha çok token.
- Doğrulama, kaynakta olmayan bir sayıyı içeren cevabı yakalayıp
  "bulamadım"a çevirdi.
- Her bileşen ayrı ayrı ölçülebilir; sistem, bileşenlerinin ölçüleriyle
  iyileştirilir.
