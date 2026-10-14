# Sıfır ve Az Örnekli Prompt

Bir işi anlatmanın iki yolu var: kuralı söylemek ya da örnek göstermek.
Yalnızca talimat verdiğin prompt'a **sıfır örnekli** (zero-shot), birkaç
çözülmüş örnek eklediğine **az örnekli** (few-shot) prompt denir. Örnekler
modele hem görevi hem cevabın biçimini gösterir: "yalnızca kategori adı"
demek yerine, kategori adından ibaret birkaç cevap gösterirsin. Bu
bölümde az örnekli prompt'u kod olarak kuruyoruz ve asıl soruya
odaklanıyoruz: **hangi örnekleri** koymalı? Bu soru modele değil veriye
bağlı ve burada gerçekten ölçülebilir.

## Veri: etiketli destek mesajları

`shop_data.py` bir outdoor mağazasının 40 destek mesajını ve bir
çalışanın onlara verdiği kategoriyi içeriyor; mesajlar dersler için elle
yazıldı. Önce iki parçaya ayırıyoruz: örnek seçeceğimiz **havuz** ve
promptu sınayacağımız **test** mesajları. İkisi asla karışmamalı; test
mesajı aynı zamanda örnek olarak prompt'ta durursa, prompt'un başarısı
olduğundan iyi görünür.

```python
from collections import Counter

from shop_data import TICKETS, LABELS

test = [t for t in TICKETS if t["id"] % 4 == 0]
pool = [t for t in TICKETS if t["id"] % 4 != 0]
print(len(pool), "examples to choose from,", len(test), "for testing")
print(Counter(t["label"] for t in test))
print(pool[0]["text"], "->", pool[0]["label"])
```

```text
30 examples to choose from, 10 for testing
Counter({'warranty': 2, 'refunds': 2, 'returns': 2, 'shipping': 2, 'payment': 2})
My parcel should have arrived on Monday. Where is it? -> shipping
```

## Örnekler mesaj olarak

Örnekleri prompt'a koymanın bir yolu onları sohbetin geçmişiymiş gibi
vermek: her örnek bir `user` mesajı ve onun `assistant` cevabı. Model
cevabın tam biçimini (küçük harfle tek kelime) bu cevaplardan görür.

```python
from llm_client import ChatClient, count_message_tokens

SYSTEM = ("Put the customer message into one category: "
          + ", ".join(LABELS) + ". Answer with the category only.")


def build_messages(examples, text):
    messages = [{"role": "system", "content": SYSTEM}]
    for example in examples:
        messages.append({"role": "user", "content": example["text"]})
        messages.append({"role": "assistant", "content": example["label"]})
    messages.append({"role": "user", "content": text})
    return messages


question = test[0]["text"]
for k in [0, 2, 5, 10]:
    tokens = count_message_tokens(build_messages(pool[:k], question))
    print(k, "examples:", tokens, "tokens")

client = ChatClient(["warranty"])
client.chat(build_messages(pool[:2], question), max_tokens=5)
print([m["role"] for m in client.calls[0]["messages"]])
```

```text
0 examples: 56 tokens
2 examples: 107 tokens
5 examples: 178 tokens
10 examples: 287 tokens
['system', 'user', 'assistant', 'user', 'assistant', 'user']
```

Her örnek, mesajı ve cevabıyla birlikte her çağrıda yeniden gönderilir;
token sayısı örnek sayısıyla doğrusal büyüyor. On örnek, sıfır örnekli
prompt'un 5,1 katı. Örnekler bedava değil, bu yüzden az ama iyi
seçilmiş örnek istiyoruz.

Örnekler ayrıca tek bir metnin içine de yazılabilir (`Message: ...
Category: ...` satırları). Hangisinin senin modelinde daha iyi çalıştığı
bir ölçüm sorusu; mesaj biçimi sohbet modellerinde yaygın olanı.

## Rastgele örnek kategori kaçırır

En kolay yol havuzdan rastgele beş örnek çekmek. Beş kategori ve beş
örnek varken bu her kategoriyi göstermeye yeter mi? Bin farklı çekilişte
sayalım:

```python
import random

missing = 0
for seed in range(1000):
    picked = random.Random(seed).sample(pool, 5)
    missing += len({t["label"] for t in picked}) < len(LABELS)
print("random draws missing a category:", missing, "of 1000")


def balanced(pool, per_label, seed):
    rng = random.Random(seed)
    chosen = []
    for label in LABELS:
        same = [t for t in pool if t["label"] == label]
        chosen += rng.sample(same, per_label)
    rng.shuffle(chosen)
    return chosen


print([t["label"] for t in balanced(pool, 1, seed=3)])
```

```text
random draws missing a category: 932 of 1000
['returns', 'shipping', 'refunds', 'warranty', 'payment']
```

Rastgele beş örnek, çekilişlerin neredeyse hepsinde en az bir kategoriyi
hiç göstermiyor. Dengeli seçim her kategoriden aynı sayıda örnek alıp
sonra karıştırıyor. Karıştırmak önemli: örnekler kategoriye göre sıralı
dursa, son örneğin kategorisi hep aynı olurdu. Örneklerin sırasının ve
etiket dağılımının cevabı etkileyebildiği biliniyor; ne kadar
etkilediği modele göre değişir, bu yüzden dengeli ve karışık vermek
güvenli varsayılan.

## Girdiye benzeyen örnekler

Bir başka yol, her yeni mesaj için havuzdan **ona en çok benzeyen**
örnekleri seçmek. Önceki modülde belge ararken kullandığımız TF-IDF ve
kosinüs benzerliği burada da işe yarıyor:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer().fit([t["text"] for t in pool])
pool_vectors = vectorizer.transform([t["text"] for t in pool])


def similar(text, k):
    scores = (pool_vectors @ vectorizer.transform([text]).T).toarray().ravel()
    best = scores.argsort()[::-1][:k]
    return [pool[i] for i in best]


for t in test[:2]:
    print(t["label"], "|", t["text"])
    for e in similar(t["text"], 3):
        print("    ", e["label"], "|", e["text"])
same = sum(similar(t["text"], 1)[0]["label"] == t["label"] for t in test)
print("nearest example has the same category:", same, "of", len(test))
```

```text
warranty | The zip of my tent broke after one year.
     warranty | The sole of my boots came off after three months.
     warranty | A seam of my backpack is coming apart.
     shipping | Can I change the delivery address after ordering?
refunds | When will the refund reach my credit card?
     refunds | I paid with a gift card, how do I get my refund?
     payment | My card was declined at checkout.
     refunds | Can the refund go to a different bank account?
nearest example has the same category: 6 of 10
```

İlk mesajda en benzer üç örnekten ikisi aynı kategoriden (`warranty`),
ama ortak kelimeler çoğunlukla "the", "of", "my", "after" gibi sıradan
kelimeler; üçüncü örnek bir kargo mesajı. Bütün test mesajlarında en
benzer örneğin kategorisi on mesajın 6'sında aynı. Kelime örtüşmesi zayıf
bir benzerlik ölçüsü: anlamı yakın ama kelimeleri farklı iki mesajı
bulamaz. Anlam düzeyindeki benzerlik için gömme (embedding) modelleri
kullanılır; onlar da aynı yolla ölçülerek seçilir.

Benzer örnek seçmenin iki bedeli var. Birincisi, her mesaj için ayrı bir
arama gerekir. İkincisi, seçilen örneklerin hepsi aynı kategoriden
olabilir ve prompt yalnızca o kategoriyi gösterir. Uygulamada iki yol
birleştirilir: her kategoriden en benzer bir örnek gibi.

## Örnek seçerken kontrol listesi

- **Test mesajlarını örnek yapma.** Havuz ile test ayrı kalsın; yoksa
  ölçtüğün başarı ezber olur.
- **Her kategoriyi göster** ve örnekleri karışık sırayla ver.
- **Örnek cevaplar tam istenen biçimde olsun.** Örnek cevaplardan biri
  "Shipping." diye yazılmışsa model o biçimi de öğrenir.
- **Az ama iyi seç.** Her örnek her çağrıda ödenir; örnek sayısını
  artırmanın değip değmediğini ölç.
- **Zor durumları örnekle göster.** İki kategori arasında kalan mesajlar
  (para iadesi mi, iade mi?) örnek olarak en çok işe yarayanlardır.

## Özet

- Sıfır örnekli prompt yalnızca talimat verir; az örnekli prompt çözülmüş
  örnekler de gösterir ve cevabın biçimini örnekle öğretir.
- Örnekler `user` / `assistant` mesaj çiftleri olarak verilebilir; her
  biri her çağrıda yeniden ödenir.
- Rastgele beş örnek, beş kategoriden en az birini çekilişlerin
  neredeyse hepsinde kaçırdı; dengeli ve karışık seçim bunu önler.
- Girdiye benzeyen örnekler TF-IDF ile bulunabilir; kategori dengesini
  bozabilir, iki yol birleştirilebilir.
- Örnek havuzu ile test mesajları ayrı tutulur.
