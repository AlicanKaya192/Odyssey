# Belge Gömmeleri ve Anlamsal Arama

NLP Temelleri'nin 07. bölümünde destek taleplerini yardım merkezi
makalelerine TF-IDF ile eşleştirmiştik ve bir sorunu açık bırakmıştık:
**kelime uyuşmazlığı**. Talep "package" diyor, makale "parcel"; ortak kelime
yoksa TF-IDF benzerliği 0. Bu bölümde kelime vektörlerinden **belge
vektörleri** kuracağız ve aramayı kelime örtüşmesinden **anlam
benzerliğine** taşıyacağız. Buna **anlamsal arama** (semantic search)
denir.

## Talep metinlerinden kelime vektörleri

Vektörleri bu kez destek taleplerinin kendi dilinden öğrenelim: değerlendirme
için kullanacağımız taleplerden **ayrı** 20 000 talep (farklı tohum) ve
makaleler. Yöntem 01'deki PPMI + SVD.

```python
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from text_data import make_articles, make_tickets

TOKEN = re.compile(r"[a-z]+")
articles = make_articles()
article_texts = [a["title"] + " " + a["text"] for a in articles]
train_texts = [t["text"] for t in make_tickets(20000, seed=1)] + article_texts
docs = [TOKEN.findall(t.lower()) for t in train_texts]
counts = Counter(w for d in docs for w in d)
vocab = sorted(w for w in counts if counts[w] >= 3)
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for d in docs:
    ids = [index.get(w) for w in d]
    for i, a in enumerate(ids):
        for j in range(max(0, i - 4), min(len(ids), i + 5)):
            if a is not None and j != i and ids[j] is not None:
                M[a, ids[j]] += 1
with np.errstate(divide="ignore", invalid="ignore"):
    P = np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))
P = np.nan_to_num(np.maximum(P, 0))
U, S, _ = np.linalg.svd(P)
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
print(len(vocab))
for word in ["parcel", "refund", "password"]:
    sims = E @ E[index[word]]
    print(word, [vocab[i] for i in np.argsort(-sims)[1:5]])
```

```text
454
parcel ['arrived', 'box', 'pracel', 'parecl']
refund ['rfeund', 'refnud', 'reufnd', 'insetad']
password ['paswsord', 'psasword', 'passwrod', 'reset']
```

- 454 kelime. "parcel"in komşuları "arrived", "box" ve iki yazım hatalı
  hâli: "pracel", "parecl".
- "refund"un ve "password"ün en yakın komşuları da yazım hataları. Hiç kimse
  "rfeund aslında refund demek" demedi; yazım hatalı kelime doğrusuyla
  **aynı bağlamlarda** geçtiği için vektörü yakın düştü. TF-IDF için
  "rfeund" ile "refund" iki alakasız sütundu.
- `nan_to_num`: hiç bağlamı kalmayan bir kelimenin satırı 0/0 = `nan` verir;
  onu 0 yapıyoruz.

## Belge vektörü: kelime vektörlerinin ortalaması

Bir belgenin vektörü için en basit yol, içindeki (durak olmayan, bilinen)
kelimelerin vektörlerinin ortalaması:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def embed(text):
    words = [w for w in TOKEN.findall(text.lower())
             if w in index and w not in ENGLISH_STOP_WORDS]
    if not words:
        return np.zeros(E.shape[1])
    v = np.mean([E[index[w]] for w in words], axis=0)
    return v / np.linalg.norm(v)


a = "Where is my order? It has not arrived yet."
b = "The parcel arrived damaged."
c = "The app crashes on my phone."
tfidf = TfidfVectorizer(stop_words="english").fit(article_texts)
for x, y in [(a, b), (a, c)]:
    vx, vy = tfidf.transform([x]), tfidf.transform([y])
    lexical = cosine_similarity(vx, vy)[0, 0]
    print(round(float(lexical), 3), round(float(embed(x) @ embed(y)), 3))
```

```text
0.0 0.723
0.0 0.129
```

- TF-IDF makalelerin dağarcığıyla kuruldu; "arrived" o dağarcıkta yok
  (makalede "arrives" geçiyor). İki kargo talebinin TF-IDF benzerliği bu
  yüzden 0. Gömmelerle 0,723; kargo ile uygulama hatası ise 0,129.
- Ortalama gömme cümle düzeyinde gürültülüdür: alakasız iki talep bile 0,1–0,5
  benzerlik alabilir. Tek tek değerlere değil, sıralamaya bakmak gerekir;
  aramada da zaten sıralama kullanılır.
- Ortalama kelime sırasını bilmez; yine bir "torba". Ama torbadaki
  kelimeler artık anlam taşıyan vektörler.

## Aramayı ölçmek

NLP Temelleri'ndeki gibi: 2000 talep, 15 makale; ilk sonuçtaki makalenin
kategorisi talebinkiyle aynıysa isabet (precision@1).

```python
tickets = make_tickets(2000)
labels = np.array([t["category"] for t in tickets])
categories = np.array([a["category"] for a in articles])
queries = [t["text"] for t in tickets]
lexical = cosine_similarity(tfidf.transform(queries),
                            tfidf.transform(article_texts))
A = np.array([embed(t) for t in article_texts])
semantic = np.array([embed(q) for q in queries]) @ A.T
for name, scores in [("tfidf", lexical), ("embedding", semantic)]:
    hits = categories[scores.argmax(axis=1)] == labels
    print(name, round(float(hits.mean()), 3))
zero = lexical.max(axis=1) == 0
hits = categories[semantic.argmax(axis=1)] == labels
print(int(zero.sum()), round(float(hits[zero].mean()), 3))
```

```text
tfidf 0.804
embedding 0.819
5 1.0
```

- Gömmelerle arama %81,9, TF-IDF %80,4. Fark küçük; çoğu talepte ortak
  kelimeler zaten yeterli.
- 5 talebin makalelerle **hiç** ortak kelimesi yok; TF-IDF onlar için kör
  (bütün puanlar 0). Gömmeler beşini de doğru makaleye gönderdi.

## İkisini birleştirmek

İki yöntem farklı şeyleri iyi yapıyor: TF-IDF tam kelime eşleşmesini
(sipariş numarası, ürün adı), gömmeler anlamı. **Karma arama** (hybrid
search) iki puanı ağırlıklı toplar:

```python
for alpha in [0.0, 0.3, 0.5, 0.7, 1.0]:
    mixed = alpha * lexical + (1 - alpha) * semantic
    accuracy = (categories[mixed.argmax(axis=1)] == labels).mean()
    print(alpha, round(float(accuracy), 3))
```

```text
0.0 0.819
0.3 0.839
0.5 0.832
0.7 0.826
1.0 0.804
```

- `alpha = 0` yalnızca gömme, `1` yalnızca TF-IDF. Karışım ikisinden de
  iyi: 0,3'te %83,9.
- Gerçek arama sistemlerinde de en yaygın kurulum bu: hızlı bir kelime
  araması (BM25 gibi) ile bir anlamsal aramanın puanlarını birleştirmek.
  `alpha`'yı burada test verisinde seçtik; gerçek işte doğrulama verisiyle
  seçilir.

## Özet

- Talep metinlerinden öğrenilen vektörlerde yazım hataları doğru biçimin
  komşusu oldu: "rfeund" ≈ "refund".
- Belge vektörü için en basit yol kelime vektörlerinin ortalaması; ortak
  kelimesi olmayan iki talep bile benzer çıkabiliyor.
- Anlamsal arama TF-IDF'i biraz geçti (%81,9'a %80,4) ve ortak kelimesi
  olmayan talepleri de buldu.
- Karma arama ikisinin gücünü birleştirdi: %83,9.
