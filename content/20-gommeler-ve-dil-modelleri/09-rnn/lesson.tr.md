# Tekrarlayan Sinir Ağları

08'deki ağ bir metnin kelime gömmelerinin ortalamasını alıyordu; kelimelerin
sırası kayboluyordu ve "not bad" ile "bad not" aynı görünüyordu. 06'daki
n-gram dil modeli sırayı görüyordu ama yalnızca son bir iki kelimeyi.
**Tekrarlayan sinir ağı** (recurrent neural network, RNN) ikisinin
arasındaki boşluğu doldurur: metni soldan sağa okur ve her kelimede bir
**gizli durumu** (hidden state) günceller. Gizli durum, o ana kadar
okunanların sabit boyutlu bir özeti gibidir:

$$h_t = \tanh(x_t W_x + h_{t-1} W_h + b)$$

Her adımda **aynı** ağırlıklar kullanılır; ağ bu yüzden her uzunlukta metni
okuyabilir. Bu bölümde NumPy ile bir RNN dil modeli kurup sonraki kelimeyi
tahmin ettireceğiz ve n-gram modelinin göremediği bir şeyi görüp
görmediğine bakacağız.

## Veri

Küçük dünya cümleleri; her cümlenin başına `<s>`, sonuna `</s>` ekliyoruz.

```python
import numpy as np
from corpus_data import make_corpus

sentences = [["<s>"] + s.split() + ["</s>"] for s in make_corpus(20000)]
vocab = sorted({w for s in sentences for w in s})
index = {w: i for i, w in enumerate(vocab)}
seqs = [[index[w] for w in s] for s in sentences]
print(len(vocab), len(seqs), max(len(s) for s in seqs))
print(" ".join(sentences[0]))
```

```text
168 20000 11
<s> we ate apple for dinner </s>
```

168 kelime, 20 000 cümle; en uzun cümle 11 kelime (işaretler dahil).

## Bir adım, bir cümle

Her adımda kelimenin gömmesi (`E`) ve önceki gizli durum birleşip yeni
gizli durumu verir; gizli durumdan bütün sözlük üzerinde bir softmax ile
sonraki kelimenin olasılıkları çıkar.

```python
rng = np.random.default_rng(0)
V, D, H = len(vocab), 16, 32
P = {"E": rng.normal(0, 0.1, (V, D)), "Wx": rng.normal(0, 0.1, (D, H)),
     "Wh": rng.normal(0, 0.1, (H, H)), "bh": np.zeros(H),
     "Wo": rng.normal(0, 0.1, (H, V)), "bo": np.zeros(V)}


def forward(seq):
    hs, ps = [np.zeros(H)], []
    for t in range(len(seq) - 1):
        h = np.tanh(P["E"][seq[t]] @ P["Wx"] + hs[-1] @ P["Wh"] + P["bh"])
        z = h @ P["Wo"] + P["bo"]
        p = np.exp(z - z.max())
        hs.append(h)
        ps.append(p / p.sum())
    return hs, ps


hs, ps = forward(seqs[0])
loss = -np.mean([np.log(p[y]) for p, y in zip(ps, seqs[0][1:])])
print(len(hs), hs[1].shape, round(float(ps[0].sum()), 3))
print(round(float(loss), 3), round(float(np.log(V)), 3))
```

```text
7 (32,) 1.0
5.12 5.124
```

- 7 kelimelik cümlede 6 tahmin yapılır; `hs` başlangıçtaki sıfır durumla
  birlikte 7 durum tutar. Her gizli durum 32 sayı.
- Eğitilmemiş ağın kaybı 5,12, yani `log 168`'e çok yakın: her kelimeye
  aşağı yukarı eşit şans veriyor.

## Zamanda geri yayılım

Türev hesabı 08'deki gibi, tek farkla: bir gizli durum hem o adımın
tahminini hem de **sonraki** adımları etkiler. Bu yüzden türevi sondan başa
doğru yürütürüz ve her adımda bir sonrakinden gelen türevi (`dh_next`)
ekleriz. Buna **zamanda geri yayılım** (backpropagation through time, BPTT)
denir.

```python
def backward(seq):
    hs, ps = forward(seq)
    G = {k: np.zeros_like(v) for k, v in P.items()}
    loss, dh_next = 0.0, np.zeros(H)
    for t in reversed(range(len(seq) - 1)):
        dz = ps[t].copy()
        loss -= np.log(dz[seq[t + 1]])
        dz[seq[t + 1]] -= 1
        G["Wo"] += np.outer(hs[t + 1], dz)
        G["bo"] += dz
        draw = (1 - hs[t + 1] ** 2) * (P["Wo"] @ dz + dh_next)
        G["bh"] += draw
        G["Wx"] += np.outer(P["E"][seq[t]], draw)
        G["Wh"] += np.outer(hs[t], draw)
        G["E"][seq[t]] += P["Wx"] @ draw
        dh_next = P["Wh"] @ draw
    n = len(seq) - 1
    return loss / n, {k: g / n for k, g in G.items()}


for epoch in range(2):
    total = 0.0
    for i in rng.permutation(len(seqs)):
        loss, G = backward(seqs[i])
        total += loss
        norm = np.sqrt(sum((g ** 2).sum() for g in G.values()))
        for k in P:
            P[k] -= 0.2 * min(1.0, 5.0 / norm) * G[k]
    print(epoch, round(total / len(seqs), 3))
```

```text
0 1.352
1 1.156
```

- `1 - h²`, `tanh`'ın türevi.
- `min(1.0, 5.0 / norm)` **türev kırpma** (gradient clipping): türevlerin
  toplam büyüklüğü 5'i aşarsa küçültülür. RNN'de türev adımlar boyunca
  çarpılarak büyüyebilir (birinci not); kırpma tek bir kötü adımın
  ağırlıkları bozmasını önler.
- İki tur bu bilgisayarda yaklaşık 15 saniye sürüyor: her cümle ayrı ayrı,
  kelime kelime işleniyor. Bu sıralılık RNN'in en büyük zayıflığı.

## Zamiri hatırlıyor mu?

"the queen smiled and ___" cümlesinde sonraki kelime "she" olmalı. Cevap üç
kelime geride; model bu bilgiyi gizli durumda taşıyabildi mi?

```python
from collections import Counter
from corpus_data import GENDER_PAIRS


def next_word_probs(words):
    seq = [index[w] for w in ["<s>"] + words] + [0]
    return forward(seq)[1][-1]


correct = 0
for male, female in GENDER_PAIRS:
    for word, pronoun in [(male, "he"), (female, "she")]:
        p = next_word_probs(["the", word, "smiled", "and"])
        guess = "he" if p[index["he"]] > p[index["she"]] else "she"
        correct += guess == pronoun
print(correct, 2 * len(GENDER_PAIRS))
trigrams = Counter(t for s in sentences for t in zip(s, s[1:], s[2:]))
print(trigrams["smiled", "and", "he"], trigrams["smiled", "and", "she"])
for word in ["queen", "king"]:
    p = next_word_probs(["the", word, "smiled", "and"])
    print(word, round(float(p[index["he"]]), 3), round(float(p[index["she"]]), 3))
```

```text
16 16
316 338
queen 0.029 0.947
king 0.965 0.013
```

- RNN 16 kişi kelimesinin 16'sında doğru zamiri seçiyor. "queen"den sonra
  "she"ye 0,947, "king"den sonra "he"ye 0,965 olasılık veriyor.
- Trigram modeli yalnızca "smiled and"i görür: orada "she" 338, "he" 316 kez
  geçmiş. Hep "she" der ve 16'nın yalnızca 8'ini bilir. Üç kelime gerideki
  özneyi göremez.
- RNN öğretilmeden öğrendi: "queen" bilgisini gizli durumda iki adım
  boyunca taşıdı.

## Metin üretmek

Dil modeli olasılık verdiğine göre ondan örnek de çekebiliriz: `<s>` ile
başla, olasılıklara göre bir kelime seç, onu girdi yap, `</s>` gelene kadar
devam et.

```python
def generate(seed):
    gen = np.random.default_rng(seed)
    h, word, out = np.zeros(H), index["<s>"], []
    while len(out) < 15:
        h = np.tanh(P["E"][word] @ P["Wx"] + h @ P["Wh"] + P["bh"])
        z = h @ P["Wo"] + P["bo"]
        p = np.exp(z - z.max())
        word = gen.choice(V, p=p / p.sum())
        if vocab[word] == "</s>":
            break
        out.append(vocab[word])
    return " ".join(out)


for seed in range(5):
    print(generate(seed))
```

```text
the daughter lives in a small house
the uncle lives in a small house
the dog chased the horse
she is a daughter
we took the bike to berlin
```

Cümlelerin hepsi küçük dünyanın dilbilgisine uyuyor. Gerçek metinde RNN
bunu bu kadar iyi yapamaz; burada dünya küçük ve kurallı. Üretim yöntemleri
(açgözlü seçim, sıcaklık, en olası k kelime) 13. bölümde.

## Özet

- RNN metni soldan sağa okur; her adımda aynı ağırlıklarla bir gizli durumu
  günceller. Gizli durum okunanların özeti.
- Eğitim zamanda geri yayılımla: türev sondan başa yürür, her adım bir
  sonrakinden gelen türevi ekler. Türev kırpma patlayan türevi önler.
- Küçük RNN dil modeli üç kelime gerideki özneye göre zamiri 16/16 doğru
  seçti; yalnızca son iki kelimeyi gören trigram 8/16'da kaldı.
- RNN'in zayıflığı sıralılık: her adım bir öncekini bekler ve uzun
  mesafede türev kaybolabilir (birinci not). Sonraki bölümün dikkat
  mekanizması her kelimeye tek adımda bakar.
