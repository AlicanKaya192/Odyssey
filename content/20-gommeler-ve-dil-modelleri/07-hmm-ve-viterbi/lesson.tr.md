# HMM ile Sözcük Türü Etiketleme

NLP Temelleri'nin 14. bölümünde bilgi çıkarmanın bir **sıra etiketleme**
(sequence labelling) problemine dönüştüğünü görmüştük: her token'a bir
etiket. Bu bölümde klasik bir sıra etiketleme görevini, **sözcük türü
etiketlemeyi** (part-of-speech tagging) çözeceğiz: her kelimenin isim mi,
fiil mi, sıfat mı olduğunu bulmak. Zorluk şu: "book" bir isim ("the book")
ya da fiil ("I book a table") olabilir; karar **komşulara** bağlı. Bunun
için **gizli Markov modeli** (hidden Markov model, HMM) kuracak ve en olası
etiket dizisini **Viterbi** algoritmasıyla bulacağız.

## Veri: etiketli cümleler

`make_tagged` her kelimesi etiketli cümleler üretiyor. Etiketler: DET
(belirteç: the, a), NOUN (isim), VERB (fiil), ADJ (sıfat), ADP (edat), PRON
(zamir), ADV (zarf).

```python
import math
from collections import Counter

import numpy as np
from corpus_data import make_tagged

train = make_tagged(3000)
test = make_tagged(1000, seed=14)
print(" ".join(f"{w}/{t}" for w, t in train[0]))
tags = sorted({t for s in train for _, t in s})
pairs = Counter((w, t) for s in train for w, t in s)
options = {}
for w, t in pairs:
    options.setdefault(w, set()).add(t)
print(tags)
for w, ts in sorted(options.items()):
    if len(ts) > 1:
        print(w, sorted(ts))
```

```text
you/PRON today/ADV light/VERB a/DET quiet/ADJ park/NOUN
['ADJ', 'ADP', 'ADV', 'DET', 'NOUN', 'PRON', 'VERB']
book ['NOUN', 'VERB']
light ['ADJ', 'NOUN', 'VERB']
park ['NOUN', 'VERB']
run ['NOUN', 'VERB']
train ['NOUN', 'VERB']
watch ['NOUN', 'VERB']
```

Altı kelimenin birden çok etiketi var: "book", "park", "run", "train",
"watch" isim ya da fiil; "light" üçünden biri bile olabilir ("a light
bag", "the light", "we light the fire").

## Taban çizgisi: en sık etiket

En basit etiketleyici her kelimeye eğitimde en sık aldığı etiketi verir:

```python
best = {w: max(ts, key=lambda t: pairs[w, t]) for w, ts in options.items()}
words = [(w, t) for s in test for w, t in s]
hits = [best[w] == t for w, t in words]
ambiguous = [best[w] == t for w, t in words if len(options[w]) > 1]
print(round(sum(hits) / len(hits), 3), round(sum(ambiguous) / len(ambiguous), 3))
```

```text
0.914 0.619
```

- Genel doğruluk %91,4 ama çok anlamlı kelimelerde yalnızca %61,9: "book"
  her yerde aynı etiketi alıyor.
- Çok anlamlı kelimenin doğru etiketi çevresinden anlaşılır: "the"den sonra
  isim, "i"den sonra fiil gelir. Model bunu bilmeli.

## Gizli Markov modeli

HMM iki şey bilir:

- **Geçiş olasılıkları** `P(etiket | önceki etiket)`: DET'ten sonra çoğunlukla
  ADJ ya da NOUN, PRON'dan sonra VERB gelir. Etiketler bir Markov zinciri.
- **Yayım olasılıkları** `P(kelime | etiket)`: NOUN etiketi "book"u ne sıklıkla
  "üretir"?

Etiketler **gizli**, yalnızca kelimeleri görüyoruz; model "önce bir etiket
seçilir, sonra o etiket bir kelime üretir" diye düşünür. İkisini de
sayımlardan, düzgünleştirerek tahmin edelim:

```python
START = len(tags)
index = {t: i for i, t in enumerate(tags)}
transition = np.ones((len(tags) + 1, len(tags)))
emission = {t: Counter() for t in tags}
for s in train:
    prev = START
    for w, t in s:
        transition[prev, index[t]] += 1
        emission[t][w] += 1
        prev = index[t]
transition = np.log(transition / transition.sum(axis=1, keepdims=True))
V = len(options) + 1


def log_emit(t, w):
    total = sum(emission[t].values())
    return math.log((emission[t][w] + 0.01) / (total + 0.01 * V))


for a, b in [("DET", "NOUN"), ("DET", "VERB"), ("PRON", "VERB")]:
    print(a, b, round(math.exp(transition[index[a], index[b]]), 3))
for t in ["NOUN", "VERB"]:
    print(t, round(math.exp(log_emit(t, "book")), 3))
```

```text
DET NOUN 0.665
DET VERB 0.0
PRON VERB 0.667
NOUN 0.109
VERB 0.056
```

- DET'ten sonra NOUN gelme olasılığı yüksek, VERB neredeyse hiç. PRON'dan
  sonra çoğunlukla VERB.
- "book" hem NOUN hem VERB etiketinden yayılıyor. Hangisinin seçileceğine
  geçiş olasılıkları karar verecek.
- `START` satırı cümlenin ilk etiketinin olasılıklarını tutuyor. Geçişlerde
  +1 (Laplace), yayımda +0,01 düzgünleştirme var; görülmemiş kelimeler de
  küçük bir olasılık alıyor.

## Viterbi: en olası etiket dizisi

7 etiket ve 6 kelimelik bir cümlede `7^6 = 117 649` olası etiket dizisi
var; hepsini denemek uzun cümlelerde imkânsızlaşır. **Viterbi** algoritması
dinamik programlamayla (Algoritma Teknikleri modülü) her adımda, her etiket
için o etikete ulaşan **en iyi** yolu tutar; geri kalanını atar.

```python
def viterbi(sentence):
    n, T = len(sentence), len(tags)
    score = np.full((n, T), -np.inf)
    back = np.zeros((n, T), dtype=int)
    for j, t in enumerate(tags):
        score[0, j] = transition[START, j] + log_emit(t, sentence[0])
    for i in range(1, n):
        for j, t in enumerate(tags):
            candidates = score[i - 1] + transition[:T, j]
            back[i, j] = int(np.argmax(candidates))
            score[i, j] = candidates[back[i, j]] + log_emit(t, sentence[i])
    path = [int(np.argmax(score[-1]))]
    for i in range(n - 1, 0, -1):
        path.append(int(back[i, path[-1]]))
    return [tags[j] for j in reversed(path)]


for text in ["i book a table", "the book was long", "we light the old watch"]:
    print(text, viterbi(text.split()))
```

```text
i book a table ['PRON', 'VERB', 'DET', 'NOUN']
the book was long ['DET', 'NOUN', 'VERB', 'ADJ']
we light the old watch ['PRON', 'VERB', 'DET', 'ADJ', 'NOUN']
```

- "i book a table": "book" fiil; "the book was long": isim. Aynı kelime,
  komşulara göre iki farklı etiket.
- "we light the old watch": "light" fiil, "watch" isim. Her adımda yalnızca
  T × T karşılaştırma yapılıyor: toplam iş `n · T²`, `T^n` değil.
- `back` tablosu her hücrede "buraya hangi etiketten gelindi" bilgisini
  tutuyor; sondan başa doğru izleyince en iyi yol çıkıyor.

## Ölçmek

```python
correct = ambiguous_correct = ambiguous_total = 0
for s in test:
    predicted = viterbi([w for w, _ in s])
    for (w, t), p in zip(s, predicted):
        correct += p == t
        if len(options[w]) > 1:
            ambiguous_total += 1
            ambiguous_correct += p == t
print(round(correct / len(words), 3), round(ambiguous_correct / ambiguous_total, 3))
```

```text
0.995 0.976
```

Çok anlamlı kelimelerde doğruluk %61,9'dan %97,6'ya, genelde %91,4'ten
%99,5'e çıktı. Kelimenin kendisi yetmiyordu; etiketlerin **dizilişi** (geçiş
olasılıkları) eksik bilgiyi tamamladı.

## Özet

- Sözcük türü etiketleme bir sıra etiketleme görevi; çok anlamlı kelimenin
  etiketi komşulara bağlı.
- HMM etiketleri gizli bir Markov zinciri sayar: geçiş `P(etiket | önceki)`,
  yayım `P(kelime | etiket)`. İkisi de sayımlardan.
- Viterbi en olası etiket dizisini dinamik programlamayla `n · T²` işte
  bulur.
- En sık etiket taban çizgisi %91,4, HMM %99,5; çok anlamlılarda %61,9'dan
  %97,6'ya.
