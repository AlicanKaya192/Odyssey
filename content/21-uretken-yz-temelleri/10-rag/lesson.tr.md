# RAG: Getirmeyle Desteklenen Üretim

Önceki bölümde soruya en ilgili parçaları bulmayı öğrendik. **RAG**
(retrieval-augmented generation, getirmeyle desteklenen üretim) bu
parçaları modele verip cevabı **onlara dayandırmasını** istemek. Düzenek
dört adım:

<figure class="fig">
  <div class="flow">
    <span class="node">Soru</span>
    <span class="arrow">→</span>
    <span class="node acc">Arama</span>
    <span class="arrow">→</span>
    <span class="node">Parçalar + soru</span>
    <span class="arrow">→</span>
    <span class="node acc">Model</span>
    <span class="arrow">→</span>
    <span class="node ok">Cevap + kaynak</span>
  </div>
  <figcaption>Soruya en ilgili parçalar bulunur, numaralanıp soruyla birlikte modele verilir; model cevabı bu parçalara dayandırır ve kaynak numarasını yazar.</figcaption>
</figure>

Modelin genel bilgisi yerine bizim belgelerimiz konuşur: bilgi güncel
tutulabilir, kaynak gösterilebilir ve cevap belgeye karşı denetlenebilir
(08).

## Prompt'u kurmak

09'daki parçalama ve arama kodu `retrieval.py` dosyasında. Parçaları
cümle cümle bölüyoruz. Bulunan parçaları numaralayıp kullanıcı mesajına
koyuyoruz; sistem mesajı modele kurallarını söylüyor: yalnızca kaynaklardan
cevap ver, kaynak numarasını yaz, cevap yoksa bunu söyle.

```python
import re
from retrieval import Index, by_sentence, QUESTIONS
from llm_client import ChatClient

index = Index(by_sentence())
NOT_FOUND = "I could not find this in the sources."
SYSTEM = ("Answer only from the numbered sources. Cite the source number "
          "like [2]. If the sources do not contain the answer, reply: "
          + NOT_FOUND)


def build_messages(question, found):
    sources = "\n".join(f"[{i}] {text}"
                        for i, ((_, text), _) in enumerate(found, 1))
    user = f"Sources:\n{sources}\n\nQuestion: {question}"
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}]


question = "Do gift cards expire?"
messages = build_messages(question, index.search(question, 3))
print(messages[1]["content"])
```

```text
Sources:
[1] Gift cards are available for 25, 50 and 100 euros and are valid for 3 years.
[2] Purchases paid with a gift card are refunded as a new gift card.
[3] Points expire if you make no purchase for 12 months.

Question: Do gift cards expire?
```

## Model yerine bir örnek okuyucu

Gerçek bir model bu mesajı okuyup kendi cümleleriyle bir cevap yazardı.
Program çevrimdışı olduğu için `ChatClient`'a yanıt olarak bir **örnek
okuyucu** fonksiyonu veriyoruz: kaynaklardaki cümlelerden, sorunun
kelimeleriyle en çok ortak kelimesi olanı seçip numarasıyla döndürüyor;
ortak kelime sayısı bir eşiğin altındaysa "bulamadım" diyor. Gerçek bir
modelden çok daha kaba; amacı modelin yerine geçmek değil, düzeneğin geri
kalanını (arama, prompt, kaynak, çekimser kalma) **çalıştırıp ölçmek**.

```python
import textwrap

STOP = {"the", "a", "an", "is", "are", "do", "does", "i", "my", "you",
        "to", "of", "in", "for", "can", "how", "what", "when", "it", "on",
        "and", "or", "will", "if", "be", "me", "we", "your", "with", "at",
        "much", "long", "many"}


def words(text):
    found = re.findall(r"[a-z0-9]+(?:[.:][0-9]+)?", text.lower())
    return {w for w in found if w not in STOP}


def make_reader(min_overlap):
    def reader(messages):
        user = messages[-1]["content"]
        question = user.split("Question: ")[-1]
        best, best_overlap = NOT_FOUND, 0
        for n, source in re.findall(r"\[(\d+)\] (.+)", user):
            overlap = len(words(question) & words(source))
            if overlap > best_overlap:
                best, best_overlap = f"{source} [{n}]", overlap
        return best if best_overlap >= min_overlap else NOT_FOUND
    return reader


def rag(question, k=3, min_overlap=2):
    found = index.search(question, k) if k else []
    client = ChatClient([make_reader(min_overlap)])
    return client.chat(build_messages(question, found), max_tokens=100)


def show(question, answer):
    print(question)
    print(textwrap.fill(answer, 66, initial_indent="    ",
                        subsequent_indent="    "))


for q in ["Do gift cards expire?", "Is the store open on Sunday?",
          "Do you sell bicycles?"]:
    show(q, rag(q).text)
```

```text
Do gift cards expire?
    Gift cards are available for 25, 50 and 100 euros and are
    valid for 3 years. [1]
Is the store open on Sunday?
    Our store is open Monday to Saturday, 10:00 to 19:00, and
    closed on Sundays and public holidays. [1]
Do you sell bicycles?
    I could not find this in the sources.
```

Cevaplar kaynaktan geliyor ve numarası yazılı; belgelerde olmayan
bisiklet sorusunda sistem "bulamadım" diyor.

## Kaynaksız ve kaynaklı

27 sorunun hepsini dört biçimde soralım: hiç kaynak vermeden (`k=0`) ve
3 kaynakla, iki farklı eşikle. Her cevabı dört gruptan birine koyuyoruz:
**doğru** (cevap ifadesi var), **doğru çekimser** (cevabı olmayan soruda
"bulamadım"), **yanlış** (cevap verdi ama ifade yok ya da cevabı olmayan
soruya cevap verdi), **kaçırılan** (cevabı olan soruda "bulamadım").

```python
def evaluate(k, min_overlap):
    counts = {"correct": 0, "abstain ok": 0, "wrong": 0, "missed": 0}
    tokens = 0
    for q in QUESTIONS:
        reply = rag(q["q"], k, min_overlap)
        tokens += reply.input_tokens
        if q["key"] is None:
            group = "abstain ok" if reply.text == NOT_FOUND else "wrong"
        elif reply.text == NOT_FOUND:
            group = "missed"
        else:
            group = "correct" if q["key"] in reply.text else "wrong"
        counts[group] += 1
    return counts, round(tokens / len(QUESTIONS))


for k, min_overlap in [(0, 2), (3, 2), (3, 1)]:
    print(f"k={k} overlap>={min_overlap}", *evaluate(k, min_overlap))
```

```text
k=0 overlap>=2 {'correct': 0, 'abstain ok': 3, 'wrong': 0, 'missed': 24} 74
k=3 overlap>=2 {'correct': 15, 'abstain ok': 3, 'wrong': 2, 'missed': 7} 132
k=3 overlap>=1 {'correct': 17, 'abstain ok': 1, 'wrong': 7, 'missed': 2} 132
```

Kaynak vermeden düzenek 24 sorunun hepsini kaçırıyor: okuyucunun
dayanacağı metin yok. (Gerçek bir model kaynaksız da bir cevap yazardı,
ama genel bilgisinden; bu mağazanın kurallarını bilemezdi.) 3 kaynakla ve
eşik 2 iken 24 sorunun 15'i doğru, cevabı olmayan üç sorunun üçünde de
"bulamadım" deniyor, yalnızca 2 cevap yanlış; ama 7 soru kaçırılıyor.
Eşiği 1'e düşürünce doğru cevap 17'ye çıkıp kaçırılan 2'ye iniyor; buna
karşılık yanlış cevap 7'ye çıkıyor ve cevabı olmayan sorulardan ikisine
de cevap veriliyor. Hangisinin iyi olduğu uygulamaya bağlı: yanlış cevabın
pahalı olduğu yerde (para, sağlık, hukuk) yüksek eşik seçilir. Kaynaklar
her çağrıya ortalama 58 token ekliyor (74 → 132).

## Neler yanlış gidiyor?

```python
for q in QUESTIONS:
    reply = rag(q["q"], 3, 1)
    if q["key"] is None or q["key"] not in reply.text:
        show(q["q"], reply.text)
```

```text
How much does shipping cost for a 30 euro order?
    Shipping costs are refunded only if you return the whole
    order. [1]
Can I return boots I wore on a hike?
    Brush off dried mud after every hike. [1]
How long do I have to send something back?
    To make a claim, send a photo of the damage and your order
    number. [1]
When will I get my money back?
    I could not find this in the sources.
How long is the warranty on a tent zipper?
    Store the tent loosely, not tightly packed. [1]
How much does it cost to fix a broken zip after the warranty?
    We repair broken zips for free while the product is under
    warranty. [1]
Do you deliver to Canada?
    I could not find this in the sources.
Do you sell bicycles?
    I could not find this in the sources.
In which year was the shop founded?
    Wash down sleeping bags at most twice a year at 30 degrees
    with a special down detergent. [1]
Can I pick up my order in the store?
    Shipping costs are refunded only if you return the whole
    order. [1]
```

Hatalar iki türden. **Yanlış getirme:** arama doğru cümleyi bulamıyor;
"send something back" ile "money back" 09'da gördüğümüz kelime
uyuşmazlığına takılıyor. **Getirileni yanlış kullanma:** okuyucu tek bir
ortak kelimeye kanıyor; "In which year was the shop founded?" sorusu
"year" kelimesi yüzünden uyku tulumu yıkama cümlesine, "Can I pick up my
order in the store?" sorusu "order" kelimesiyle kargo ücretinin iadesi
cümlesine bağlanıyor. Gerçek bir model bu okuyucu kadar kaba değildir;
ama bu iki tür hata gerçek RAG sistemlerinde de görülür. Bir sonraki bölüm
ikisini ayrı ayrı ölçüyor.

## Gerçek RAG sistemlerinde

- **Arama kalitesi her şeyin başı.** Model, verilmeyen bir parçadaki
  bilgiyi kullanamaz. Önce aramayı ölç (09), sonra cevabı.
- **Sistem mesajı** cevabı kaynaklara bağlamayı, kaynak göstermeyi ve
  "bulamadım" demeyi açıkça ister; ama modelin buna her zaman uyacağı
  varsayılmaz, cevap denetlenir (08).
- **Kaynak sayısı** bir ödünleşim: çok parça token ve maliyet getirir,
  ilgisiz parçalar modeli şaşırtabilir; az parça bilgiyi kaçırabilir.
- **Güncellik:** belge değişince yalnızca o belgenin parçaları yeniden
  vektöre çevrilir; modeli yeniden eğitmek gerekmez.

## Özet

- RAG: soruya ilgili parçaları bul, numaralayıp prompt'a koy, modelden
  yalnızca onlara dayanarak ve kaynak göstererek cevap iste, cevabı denetle.
- Kaynaksız düzenek hiçbir soruyu cevaplayamadı; kaynaklı düzenek
  cevapladı.
- Çekimser kalma eşiği bir ödünleşim: düşük eşik daha çok doğru ama daha
  çok yanlış cevap, yüksek eşik daha az yanlış ama daha çok kaçırma.
- Bu bölümdeki okuyucu gerçek modelin yerine konmuş kaba bir örnek;
  sayılar düzeneğin davranışını gösteriyor, bir modelin başarısını değil.
