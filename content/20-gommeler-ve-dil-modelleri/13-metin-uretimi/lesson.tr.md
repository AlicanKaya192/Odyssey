# Metin Üretimi

Bir dil modeli her adımda sonraki kelime için bir olasılık dağılımı verir.
Metin üretmek için bu dağılımdan **bir kelime seçmek** gerekir, sonra bir
sonrakini, sonra bir sonrakini. Hangi kelimenin seçileceğine **kod çözme**
(decoding) yöntemi karar verir ve aynı model, yöntem değişince çok farklı
metinler üretir. Bu bölümde destek taleplerinden bir trigram modeli kurup
başlıca yöntemleri deneyeceğiz: açgözlü seçim, ışın araması, sıcaklık,
en olası k kelime ve çekirdek örnekleme. Büyük dil modelleri de aynı
yöntemlerle metin üretir; yalnızca olasılıkları veren model daha güçlüdür.

## Model

06'daki trigram modelinin yumuşatmasız hâli: önceki iki kelimeden sonra
gelen kelimeleri sayıp olasılığa çeviriyoruz. Sayıları (`ORD-12345`,
`E401`) `#` ile değiştiriyoruz ki her numara ayrı bir kelime olmasın.

```python
import math
import re
from collections import Counter

from text_data import make_tickets

TOKEN = re.compile(r"[a-z#]+|[.!?,]")


def tokens(text):
    return TOKEN.findall(re.sub(r"\d+", "#", text.lower()))


train = [["<s>", "<s>"] + tokens(t["text"]) + ["</s>"]
         for t in make_tickets(5000, seed=1)]
followers = {}
for s in train:
    for a, b, c in zip(s, s[1:], s[2:]):
        followers.setdefault((a, b), Counter())[c] += 1


def next_probs(a, b):
    counts = followers[a, b]
    total = sum(counts.values())
    return {w: n / total for w, n in counts.items()}


print(len(followers), len(next_probs("<s>", "<s>")))
top = sorted(next_probs("my", "order").items(), key=lambda x: -x[1])[:3]
print([(w, round(p, 3)) for w, p in top])
```

```text
1062 23
[('number', 0.36), ('ord', 0.346), ('history', 0.291)]
```

1062 farklı iki kelimelik geçmiş; bir talebin ilk kelimesi için 23 seçenek.
"my order"dan sonra "number", "ord" ya da "history" geliyor.

## Açgözlü seçim

En basit yol: her adımda **en olası** kelimeyi seçmek (greedy decoding).
Üretilen cümlenin olasılığının logaritmasını da topluyoruz.

```python
def finished(seq, max_len=30):
    return seq[-1] == "</s>" or len(seq) > max_len


def greedy():
    seq, score = ["<s>", "<s>"], 0.0
    while not finished(seq):
        probs = next_probs(seq[-2], seq[-1])
        word = max(probs, key=probs.get)
        score += math.log(probs[word])
        seq.append(word)
    return round(score, 2), " ".join(seq[2:-1])


print(*greedy())
```

```text
-7.46 hey there , the app .
```

- Açgözlü seçim her seferinde **aynı** cümleyi üretir: rastgelelik yok.
- Cümle kısa ve genel. Her adımın en olası kelimesi, en olası **cümleyi**
  vermek zorunda değil: bugün en iyi görünen seçim yarın kötü bir yola
  sokabilir.

## Işın araması

**Işın araması** (beam search) her adımda tek bir yol yerine en iyi
`width` yolu birlikte yürütür: her yolu bütün olası kelimelerle uzatır,
toplam log olasılığa göre en iyi `width` tanesini tutar. Bitmiş yollar
havuzda kalır.

```python
import textwrap


def beam_search(width, alpha=0.0):
    beams = [(0.0, ["<s>", "<s>"])]
    while not all(finished(seq) for _, seq in beams):
        pool = []
        for score, seq in beams:
            if finished(seq):
                pool.append((score, seq))
                continue
            for w, p in next_probs(seq[-2], seq[-1]).items():
                pool.append((score + math.log(p), seq + [w]))
        pool.sort(key=lambda c: -c[0] / (len(c[1]) - 2) ** alpha)
        beams = pool[:width]
    score, seq = beams[0]
    return round(score, 2), " ".join(seq[2:-1])


for width in [1, 3, 10, 50]:
    score, text = beam_search(width)
    line = f"{width} {score} {text}"
    print(textwrap.fill(line, 76, subsequent_indent="    "))
```

```text
1 -7.46 hey there , the app .
3 -9.78 hey there , i get error e# when i log in on the app crashes every
    time i open the order page .
10 -9.11 hey there , i get error e# when i log in on the app .
50 -7.27 hello , the parcel arrived damaged and the box was open .
```

- Genişlik 1 açgözlü seçimin aynısı. Genişlik 50, açgözlüden daha olası
  (−7,27) bir cümle buldu.
- Ama ilerleme düzenli değil: genişlik 3 ve 10 açgözlüden **daha az olası**
  cümleler buldu. Dar bir ışın, açgözlü yolun başını bir adımda budayıp
  daha kötü bir yere sapabilir. Işın araması en olası cümleyi bulmayı
  **garanti etmez**, yalnızca daha geniş arar.
- Toplam log olasılık her kelimede biraz daha eksiye gider; bu yüzden ışın
  araması **kısa** cümleleri kayırır (`alpha`, birinci not).

## Örneklemek ve sıcaklık

Sohbet eden modeller çoğunlukla açgözlü seçimle değil **örnekleyerek**
üretir:
sonraki kelime olasılıklara göre rastgele çekilir. **Sıcaklık**
(temperature) dağılımı keskinleştirir ya da düzleştirir: olasılıklar
`p^(1/T)` ile yeniden ağırlıklanır. `T < 1` en olası kelimeleri güçlendirir,
`T > 1` az olası kelimelere şans verir.

Rastgeleliği sınırlamanın iki yolu daha var:

- **En olası k** (top-k): yalnızca en olası `k` kelime arasından seçilir.
- **Çekirdek** (top-p, nucleus): olasılıkları büyükten küçüğe toplayıp
  toplam `p`'ye ulaşan en küçük kelime kümesinden seçilir. Model eminse
  küme küçük, kararsızsa büyük olur.

```python
import random


def sample(rng, temperature=1.0, top_k=None, top_p=None):
    seq, score = ["<s>", "<s>"], 0.0
    while not finished(seq):
        probs = next_probs(seq[-2], seq[-1])
        items = sorted(probs.items(), key=lambda x: -x[1])
        if top_k:
            items = items[:top_k]
        if top_p:
            mass = 0.0
            for i, (w, p) in enumerate(items):
                mass += p
                if mass >= top_p:
                    items = items[:i + 1]
                    break
        words = [w for w, _ in items]
        weights = [p ** (1 / temperature) for _, p in items]
        word = rng.choices(words, weights=weights)[0]
        score += math.log(probs[word])
        seq.append(word)
    return score, " ".join(seq[2:]).replace(" </s>", "")


rng = random.Random(0)
for t in [0.5, 1.0, 2.0]:
    line = f"{t} {sample(rng, temperature=t)[1]}"
    print(textwrap.fill(line, 76, subsequent_indent="    "))
```

```text
0.5 dear support , the parcel arrived damaged and the box was open . how
    long does shipping to prague take ? my package was delivered to the
    wrong amount
1.0 push notifications stopped working after the update . the tracking
    number for ord # ? it has not arrived yet . how long does shipping to
    dublin take ?
2.0 how do i change the email address on my account was locked after too
    many login attempts . regards , gus
```

- Örneklemeyle her çalıştırma farklı bir talep üretiyor ve metinler çok
  daha canlı: şehir adları, isimler, birden çok cümle.
- Ama trigram modeli yalnızca iki kelime geriye bakıyor: "my package was
  delivered to the wrong amount" cümlesinde "wrong"dan sonra adres yerine
  "amount" geldi; iki ayrı talep kalıbı birbirine dikiş yerinden bağlandı.
  Daha güçlü bir model bu tutarlılığı uzun mesafede korur.

## Çeşitlilik ve olasılık

Her ayarla 300 talep üretip iki şeyi ölçelim: **çeşitlilik** (distinct-2:
farklı kelime ikililerinin bütün ikililere oranı) ve modelin ürettiği
metne verdiği **kelime başına log olasılık** (yüksek = model için daha
"doğal").

```python
def distinct(texts, n):
    grams = [tuple(t.split()[i:i + n]) for t in texts
             for i in range(len(t.split()) - n + 1)]
    return round(len(set(grams)) / len(grams), 3)


settings = {"t=0.5": {"temperature": 0.5}, "t=1.0": {},
            "t=2.0": {"temperature": 2.0}, "k=3": {"top_k": 3},
            "p=0.9": {"top_p": 0.9}}
for name, options in settings.items():
    rng = random.Random(1)
    runs = [sample(rng, **options) for _ in range(300)]
    texts = [text for _, text in runs]
    per_word = sum(s for s, _ in runs) / sum(len(t.split()) + 1 for t in texts)
    print(name, len(set(texts)), distinct(texts, 2), round(per_word, 3))
```

```text
t=0.5 286 0.064 -0.588
t=1.0 298 0.09 -0.666
t=2.0 300 0.131 -0.861
k=3 266 0.051 -0.585
p=0.9 297 0.067 -0.626
```

Sütunlar: ayar, 300 metnin kaçı farklı, distinct-2, kelime başına log
olasılık.

- Sıcaklık arttıkça çeşitlilik artıyor (0,064 → 0,131), olasılık düşüyor
  (−0,588 → −0,861). Bu bir **ödünleşim**: çeşitli metin, modelin daha az
  emin olduğu kelimeleri de içerir; çok sıcak metin tutarsızlaşır.
- En olası 3 kelime en dar seçenek: 300 talebin yalnızca 266'sı farklı,
  çeşitlilik en düşük.
- Çekirdek örnekleme (p = 0,9) iki ucun arasında: dağılımın kuyruğunu
  kesip makul kelimeler arasında çeşitliliği koruyor. Büyük dil
  modellerinde sıcaklık ve çekirdek örnekleme çoğunlukla birlikte
  ayarlanır.

## Özet

- Kod çözme yöntemi, modelin olasılıklarından metni nasıl seçtiğimizdir;
  aynı model farklı yöntemlerle çok farklı metinler üretir.
- Açgözlü seçim belirlenimci, kısa ve genel. Işın araması daha olası
  cümleler arar ama bunu garanti etmez ve kısa cümleleri kayırır.
- Örnekleme çeşitlilik getirir. Sıcaklık, top-k ve top-p bu çeşitliliği
  ayarlar: daha çeşitli metin, model için daha az olası metindir.
- Çeviri ve özet gibi tek doğru cevaba yakın işlerde ışın araması, serbest
  metin üretiminde örnekleme tercih edilir.
