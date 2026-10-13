# n-gram Dil Modeli

Şimdiye kadar kelimelerin anlamına baktık; şimdi **sıraya** bakacağız. Bir
**dil modeli** (language model) bir kelime dizisine olasılık verir: "where
is my order" doğal bir cümle, "order my is where" değil. Eşdeğer soru: bu
kelimelerden sonra hangi kelime gelir? Telefonundaki kelime önerisi, yazım
düzeltme, konuşma tanıma ve bugünkü büyük dil modelleri bu soruyu
cevaplar. Bu bölümde en eski ve en basit dil modelini, **n-gram** modelini
sayımlarla kuracağız, onu **şaşkınlık** (perplexity) ile ölçeceğiz ve
onunla metin üreteceğiz.

## Sonraki kelimenin olasılığı

Bir cümlenin olasılığı zincir kuralıyla kelimelerin koşullu olasılıklarının
çarpımıdır. n-gram modeli bunu basitleştirir: bir kelime yalnızca kendinden
önceki n − 1 kelimeye bağlıdır. Bigram (n = 2) için:

`P(w_i | w_1 ... w_(i−1)) ≈ P(w_i | w_(i−1)) = sayı(w_(i−1), w_i) / sayı(w_(i−1))`

Destek taleplerinde deneyelim. Cümle başına `<s>`, sonuna `</s>` ekliyoruz;
test taleplerinde eğitimde görülmemiş kelimeler `<unk>` oluyor.

```python
import math
import re
from collections import Counter

from text_data import make_tickets

TOKEN = re.compile(r"[a-z]+|[.!?]")


def sentences(n, seed):
    return [["<s>"] + TOKEN.findall(t["text"].lower()) + ["</s>"]
            for t in make_tickets(n, seed=seed)]


train = sentences(3000, 1)
vocab = {w for s in train for w in s} | {"<unk>"}
test = [[w if w in vocab else "<unk>" for w in s] for s in sentences(1000, 11)]
bigrams = Counter((a, b) for s in train for a, b in zip(s, s[1:]))
context = Counter(a for s in train for a in s[:-1])
after = {b: n / context["my"] for (a, b), n in bigrams.items() if a == "my"}
print(len(vocab), sum(len(s) for s in train))
print([(w, round(p, 3)) for w, p in sorted(after.items(), key=lambda x: -x[1])[:4]])
```

```text
401 68948
[('account', 0.333), ('order', 0.21), ('card', 0.116), ('package', 0.079)]
```

"my"dan sonra en olası kelimeler "account", "order", "card", "package".
Model talep dilinin kalıplarını yalnızca sayarak öğrendi.

## Görülmemiş çift sorunu

Bir cümlenin olasılığı küçük sayıların çarpımı olduğundan logaritmalarını
toplarız. Ama test verisinde eğitimde hiç görülmemiş bir bigram varsa
olasılık 0, logaritması eksi sonsuz:

```python
unseen = sum(1 for s in test for a, b in zip(s, s[1:]) if (a, b) not in bigrams)
print(unseen, sum(len(s) - 1 for s in test))


def p_bigram(a, b, k):
    return (bigrams[a, b] + k) / (context[a] + k * len(vocab))


def logprob(words, k=0.01):
    s = ["<s>"] + words + ["</s>"]
    return sum(math.log(p_bigram(a, b, k)) for a, b in zip(s, s[1:]))


for text in ["where is my order ?", "order my is where ?"]:
    print(text, round(logprob(text.split()), 2))
```

```text
77 22142
where is my order ? -21.92
order my is where ? -52.77
```

- 22 142 bigramın 77'si eğitimde yok. Sayımdan hesaplanan olasılık
  (**en büyük olabilirlik**, MLE) bunlara 0 verir ve bütün cümleyi
  "imkânsız" yapar.
- Çözüm **düzgünleştirme** (smoothing): her sayıma küçük bir `k` ekle
  (**add-k**; `k = 1` olunca Laplace). Görülmemiş çift sıfır olmayan küçük
  bir olasılık alır. 08'deki Naive Bayes'in yumuşatmasıyla aynı fikir.
- Doğal sıradaki cümlenin log olasılığı −21,9, karışık sıradakinin −52,8:
  doğal sıra yaklaşık `e^31` kat daha olası. Model dilin sırasını öğrenmiş.

## Şaşkınlık

Bir dil modelini test verisinde ölçmenin olağan yolu **şaşkınlık**
(perplexity): test kelimelerine verilen ortalama log olasılığın eksi
üstelinin `e` tabanında alınması.

`PPL = exp( −(1/N) Σ log P(w_i | geçmiş) )`

Sezgisi: model her adımda ortalama kaç kelime arasında **kararsız** kalıyor?
Küçük şaşkınlık daha iyi model demek.

```python
N = sum(len(s) - 1 for s in test)


def perplexity(prob):
    total = 0.0
    for s in test:
        for i in range(1, len(s)):
            p = prob(s, i)
            if p == 0:
                return math.inf
            total += math.log(p)
    return round(math.exp(-total / N), 2)


unigrams = Counter(w for s in train for w in s[1:])
n_uni = sum(unigrams.values())
print("unigram", perplexity(lambda s, i: (unigrams[s[i]] + 1) / (n_uni + len(vocab))))
print("bigram mle", perplexity(lambda s, i: p_bigram(s[i - 1], s[i], 0)))
for k in [1, 0.1, 0.01]:
    print("bigram", k, perplexity(lambda s, i: p_bigram(s[i - 1], s[i], k)))
```

```text
unigram 97.77
bigram mle inf
bigram 1 7.01
bigram 0.1 4.18
bigram 0.01 3.79
```

- Unigram (sırayı hiç bilmeyen model) 97,8: her adımda yaklaşık 98 kelime
  arasında kararsız gibi.
- Bigram sayımla (MLE) sonsuz: tek bir görülmemiş çift yetiyor.
- Add-1 (Laplace) 7,01, add-0,01 3,79. `k = 1` fazla: görülmemiş çiftlere
  çok fazla olasılık dağıtıp görülenlerden çalıyor. `k` bir ayar; doğrulama
  verisiyle seçilir.

## Daha uzun geçmiş: trigram

```python
trigrams = Counter((a, b, c) for s in train for a, b, c in zip(s, s[1:], s[2:]))
pairs = Counter((a, b) for s in train for a, b in zip(s[:-1], s[1:-1]))


def p_trigram(s, i, k):
    if i == 1:
        return p_bigram(s[0], s[1], k)
    a, b, c = s[i - 2], s[i - 1], s[i]
    return (trigrams[a, b, c] + k) / (pairs[a, b] + k * len(vocab))


for k in [0.1, 0.01, 0.001]:
    print("trigram", k, perplexity(lambda s, i: p_trigram(s, i, k)))
```

```text
trigram 0.1 2.73
trigram 0.01 2.2
trigram 0.001 2.15
```

İki kelimelik geçmiş şaşkınlığı 3,79'dan 2,15'e indiriyor. Daha uzun geçmiş
daha iyi tahmin demek; ama n büyüdükçe görülmemiş n-gram sayısı patlar
(04'teki dağarcık patlaması) ve sayım tabloları devleşir. n-gram
modellerinin sınırı bu: geçmiş ancak birkaç kelime olabilir.

## Metin üretmek

Dil modeli olasılık verdiği gibi **örnekleme** de yapabilir: `<s>`'den başla,
sonraki kelimeyi olasılığıyla çek, `</s>` gelene kadar sürdür.

```python
import random
import textwrap

followers = {}
for (a, b, c), n in trigrams.items():
    followers.setdefault((a, b), []).append((c, n))
rng = random.Random(0)
for _ in range(3):
    history, out = ("<s>", rng.choice([b for (a, b) in pairs if a == "<s>"])), []
    out.append(history[1])
    while history[1] != "</s>" and len(out) < 25:
        words, weights = zip(*followers[history])
        nxt = rng.choices(words, weights=weights)[0]
        out.append(nxt)
        history = (history[1], nxt)
    text = " ".join(w for w in out if w != "</s>")
    print(textwrap.fill(text, 76, subsequent_indent="  "))
```

```text
my invoice for order ord ? why did my card .
please reset the password for hana example . com . my account . my order
  number is ord . this is urgent !
good morning can i change the delivery address for order ord ? i used the
  mobile app . please help .
```

Üretilen talepler kelime kelime akıcı ama bütün olarak tutarsız olabilir
("my invoice for order ord ? why did my card ."): model yalnızca son iki
kelimeye bakıyor. (Parçalayıcı yalnızca harfleri aldığı için sipariş
numaraları "ord", e-postalar "hana example . com" olmuş.) Bir cümlenin başında söyleneni
sonunda hatırlamaz. Uzun geçmişi taşıyabilen modeller için sinir ağlarına
geçeceğiz.

## Özet

- n-gram dil modeli sonraki kelimenin olasılığını önceki n − 1 kelimeden,
  sayımlarla tahmin eder.
- Görülmemiş n-gram MLE'de olasılığı 0 yapar; add-k düzgünleştirme bunu
  önler, `k` ayarlanır.
- Şaşkınlık, test verisindeki ortalama "kararsızlık"tır; unigram 97,8,
  bigram 3,79, trigram 2,15.
- n-gram modeli metin üretebilir ama yalnızca birkaç kelimelik geçmişi
  görür.
