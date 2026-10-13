# Dağılımsal Anlam

NLP Temelleri'nde her kelime ayrı bir sütundu. "car" ile "automobile" iki
sütun, aralarında hiçbir bağ yok; "cat" ile "dog" da "cat" ile "bread" kadar
uzak. Bu modülde kelimelere **anlamı taşıyan vektörler** vereceğiz. Hepsinin
çıkış noktası tek bir fikir: **bir kelimenin anlamı, çevresinde geçen
kelimelerden** anlaşılır. Dilbilimci J. R. Firth bunu 1957'de şöyle özetledi:
"You shall know a word by the company it keeps." Buna **dağılımsal hipotez**
(distributional hypothesis) denir. Bu bölümde fikri sayılarla göreceğiz:
bir kelimenin çevresini sayacak, bu sayılardan vektör kuracak ve benzer
kelimelerin benzer vektörler aldığını ölçeceğiz.

## Tek sıcak vektörlerde uzaklık yok

Kelime torbasında her kelime kendi sütunundaydı. Tek bir kelimeyi böyle
yazınca **tek sıcak** (one-hot) vektör çıkar: kendi sütununda 1, başka
her yerde 0.

```python
import numpy as np

vocab = ["bread", "cat", "dog"]
one_hot = np.eye(len(vocab))
cat, dog, bread = one_hot[1], one_hot[2], one_hot[0]


def cosine(a, b):
    return float(a @ b / np.linalg.norm(a) / np.linalg.norm(b))


print(one_hot)
print(cosine(cat, dog), cosine(cat, bread))
```

```text
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
0.0 0.0
```

İki farklı kelimenin tek sıcak vektörleri her zaman dik: kosinüs 0. Bu
temsilde "cat" "dog"a "bread"den daha yakın değil. Bir model "cat" hakkında
öğrendiğini "dog"a taşıyamaz; her kelimeyi sıfırdan öğrenmek zorunda kalır.

## Küçük bir dünya

Bu modülün verisi `corpus_data.py`: hayvanlar, yiyecekler, taşıtlar, şehirler
ve ülkeler, kişiler (erkek/kadın, kraliyet/genç/aile) üzerine kurulmuş
basit İngilizce cümleler. Aynı sınıftaki kelimeler aynı tür cümlelerde
geçiyor; anlamın bağlamdan öğrenilip öğrenilemeyeceğini burada
deneyeceğiz.

```python
from collections import Counter

from corpus_data import make_corpus

for sentence in make_corpus(4):
    print(sentence)
sentences = [s.split() for s in make_corpus(20000)]
counts = Counter(w for s in sentences for w in s)
print(len(counts), sum(counts.values()))
print(counts.most_common(5))
```

```text
we ate apple for dinner
we flew to dublin in ireland
the people of madrid love spain
the people of dublin love ireland
166 110308
[('the', 22493), ('in', 3730), ('is', 3528), ('a', 3263), ('and', 2158)]
```

20 000 cümlede 166 farklı kelime ve 110 308 token var. Gerçek bir dil
yüz binlerce kelime içerir; burada fikri temiz görmek için dünyayı küçük
tuttuk. En sık kelime yine "the".

## Bir kelimenin çevresi

Bir kelimenin **bağlamı** (context), çevresindeki belli sayıda kelime:
**pencere** (window) 2 ise solundaki iki ve sağındaki iki kelime.

```python
def contexts(word, window=2):
    found = Counter()
    for s in sentences:
        for i, w in enumerate(s):
            if w == word:
                left, right = max(0, i - window), min(len(s), i + window + 1)
                found.update(s[j] for j in range(left, right) if j != i)
    return found


for word in ["cat", "dog", "bread"]:
    print(word, contexts(word).most_common(5))
```

```text
cat [('the', 662), ('in', 164), ('and', 160), ('chased', 154), ('a', 94)]
dog [('the', 760), ('and', 211), ('in', 190), ('chased', 164), ('sleep', 95)]
bread [('the', 265), ('and', 191), ('she', 96), ('cooked', 96), ('i', 94)]
```

- "cat" ve "dog" aynı kelimelerle geçiyor: "chased", "the", "and", "in".
  Biri ötekinin yerine konsa cümleler yine anlamlı olurdu.
- "bread"in çevresi farklı: "cooked", "she", "i". Yiyeceklerin
  bağlamı hayvanlarınkinden ayrı.
- "the" her üçünün de başında. Çok sık kelimeler her kelimenin çevresinde
  var ve bir şey ayırt etmiyor; buna aşağıda yeniden döneceğiz.

## Birlikte geçme matrisi

Bütün kelimeler için aynı sayımı bir tabloya yazalım: satır kelime, sütun
bağlam kelimesi, hücre birlikte geçme sayısı. Her satır o kelimenin
**vektörü** olur.

```python
vocab = sorted(counts)
index = {w: i for i, w in enumerate(vocab)}


def cooccurrence(window):
    M = np.zeros((len(vocab), len(vocab)))
    for s in sentences:
        for i, w in enumerate(s):
            left, right = max(0, i - window), min(len(s), i + window + 1)
            for j in range(left, right):
                if j != i:
                    M[index[w], index[s[j]]] += 1
    return M


def neighbours(M, word, k=5):
    unit = M / np.linalg.norm(M, axis=1, keepdims=True)
    sims = unit @ unit[index[word]]
    return [vocab[i] for i in np.argsort(-sims)[1:k + 1]]


M = cooccurrence(2)
print(M.shape)
for a, b in [("cat", "dog"), ("cat", "bread"), ("cat", "the")]:
    print(a, b, round(cosine(M[index[a]], M[index[b]]), 3))
for word in ["cat", "bread", "car", "paris"]:
    print(word, neighbours(M, word))
```

```text
(166, 166)
cat dog 0.998
cat bread 0.612
cat the 0.193
cat ['cow', 'mouse', 'rabbit', 'dog', 'horse']
bread ['cheese', 'salad', 'cake', 'rice', 'soup']
car ['tram', 'bus', 'truck', 'boat', 'train']
paris ['rome', 'athens', 'lisbon', 'vienna', 'dublin']
```

- Hiç kimse "cat bir hayvandır" demedi; yalnızca saydık. Yine de "cat"in
  en yakın komşuları başka hayvanlar, "bread"inkiler yiyecekler, "car"ınkiler
  taşıtlar, "paris"inkiler başka başkentler.
- "cat" ile "dog" 0,998 benzer; ama "cat" ile "bread" de 0,612. Sayımların
  büyük kısmı "the", "and", "in" gibi her yerde geçen kelimelerden geliyor ve
  vektörleri birbirine benzetiyor. Bir sonraki bölümde **PPMI** bu
  kelimelerin ağırlığını düşürecek.

## Pencere boyu

Pencere küçükse yalnızca hemen yandaki kelimeler sayılır, büyükse cümlenin
konusu da girer. Üç pencereyi karşılaştıralım:

```python
for window in [1, 2, 5]:
    M = cooccurrence(window)
    cat_the = cosine(M[index["cat"]], M[index["the"]])
    print(window, round(cat_the, 3), neighbours(M, "king", 4))
```

```text
1 0.051 ['queen', 'princess', 'uncle', 'man']
2 0.193 ['uncle', 'prince', 'man', 'brother']
5 0.899 ['prince', 'queen', 'uncle', 'man']
```

- Pencere büyüdükçe "the" her şeye benziyor: "cat" ile benzerliği 0,051'den
  0,899'a çıkıyor. Geniş pencerede sık kelimelerin etkisi büyür.
- "king"in komşuları her pencerede kişiler, ama sıraları değişiyor. Küçük
  pencere daha çok **sözdizimsel** benzerlik yakalar (aynı yerde
  kullanılabilen kelimeler), büyük pencere daha çok **konu** benzerliği.
  Gerçek uygulamalarda pencere 2 ile 10 arasında seçilir ve göreve göre
  denenir.

## Özet

- Tek sıcak vektörlerde iki farklı kelime arasındaki kosinüs hep 0;
  kelimeler arasında benzerlik yok.
- Dağılımsal hipotez: benzer bağlamda geçen kelimelerin anlamı benzerdir.
- Birlikte geçme matrisinin her satırı bir kelime vektörü. Ham sayımlar bile
  anlam sınıflarını ayırıyor.
- Sık kelimeler ("the") ham sayımlara hâkim olup her şeyi birbirine
  benzetiyor; pencere büyüdükçe bu etki artıyor. Bir sonraki bölüm bunu
  PPMI ile düzeltip vektörleri SVD ile kısaltıyor.
