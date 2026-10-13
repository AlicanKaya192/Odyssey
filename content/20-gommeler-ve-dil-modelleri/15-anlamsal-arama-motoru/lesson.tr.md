# Bitirme Projesi: Anlamsal Arama Motoru

Bu bölümde modülün parçalarını birleştirip küçük ama eksiksiz bir ürün
kuracağız: bir müşteri destek talebini okuyup ona en uygun yardım merkezi
makalesini öneren bir **arama motoru**. Kullanacaklarımız:

- etiketsiz taleplerden öğrenilen kelime vektörleri (01, 04, 12),
- TF-IDF ile kelime eşleşmesi ve gömmelerle anlam benzerliğini birleştiren
  **karma arama** (04),
- sıralamayı ölçen değerlendirme (14),
- ve gerçek bir ürünün olmazsa olmazı: emin olmadığında **"bilmiyorum"**
  diyebilmek.

## 1. Kelime vektörleri

04'teki gibi: 20 000 etiketsiz talep ve 15 makaleden PPMI + SVD ile 50
boyutlu vektörler.

```python
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_articles, make_tickets

TOKEN = re.compile(r"[a-z]+")
articles = make_articles()
article_texts = [a["title"] + " " + a["text"] for a in articles]
corpus = [t["text"] for t in make_tickets(20000, seed=1)] + article_texts
docs = [TOKEN.findall(t.lower()) for t in corpus]
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
U, S, _ = np.linalg.svd(np.nan_to_num(np.maximum(P, 0)))
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)
print(len(articles), len(vocab))
```

```text
15 454
```

## 2. Motor

Motoru bir sınıf olarak yazıyoruz: kurulurken makalelerin TF-IDF ve gömme
vektörlerini **bir kez** hesaplıyor (dizin), sorguda yalnızca sorgunun
vektörlerini hesaplayıp karşılaştırıyor. Puan, iki benzerliğin ağırlıklı
toplamı: `alpha` kelime eşleşmesinin payı.

```python
class SearchEngine:
    def __init__(self, texts, alpha=0.3):
        self.alpha = alpha
        self.tfidf = TfidfVectorizer(stop_words="english").fit(texts)
        self.lexical = self.tfidf.transform(texts)
        self.semantic = np.array([self.embed(t) for t in texts])

    @staticmethod
    def embed(text):
        words = [w for w in TOKEN.findall(text.lower())
                 if w in index and w not in ENGLISH_STOP_WORDS]
        if not words:
            return np.zeros(E.shape[1])
        v = np.mean([E[index[w]] for w in words], axis=0)
        return v / np.linalg.norm(v)

    def scores(self, queries):
        lexical = (self.tfidf.transform(queries) @ self.lexical.T).toarray()
        semantic = np.array([self.embed(q) for q in queries]) @ self.semantic.T
        return self.alpha * lexical + (1 - self.alpha) * semantic


engine = SearchEngine(article_texts)
scores = engine.scores(["my pakage never arrived"])[0]
for i in np.argsort(-scores)[:3]:
    print(round(float(scores[i]), 3), articles[i]["title"])
```

```text
0.56 Lost, late or damaged parcels
0.364 Refund or replacement for a damaged item
0.275 Partial refunds
```

Yazım hatalı "pakage" ve makalelerde geçmeyen "never" ile yazılmış sorgu,
kargo makalesini en üste getiriyor.

## 3. Ölçmek

2000 talep, her birinin kategorisi biliniyor. Bir makale, talebin
kategorisindeyse doğru sayılıyor (her kategoride 3 makale var). Üç ölçü:

- **P@1**: ilk sonuç doğru mu?
- **MRR** (mean reciprocal rank): ilk doğru sonucun sırasının tersinin
  ortalaması. İlk sırada 1, ikincide 0,5, üçüncüde 0,33.
- **R@3**: ilk üç sonuçta en az bir doğru var mı?

```python
tickets = make_tickets(2000)
queries = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
categories = np.array([a["category"] for a in articles])


def evaluate(scores):
    order = np.argsort(-scores, axis=1)
    hits = categories[order] == labels[:, None]
    first = hits.argmax(axis=1)
    return (round(float(hits[:, 0].mean()), 3),
            round(float(np.mean(1 / (first + 1))), 3),
            round(float(hits[:, :3].any(axis=1).mean()), 3))


for alpha in [1.0, 0.0, 0.3]:
    engine.alpha = alpha
    print(alpha, *evaluate(engine.scores(queries)))
engine.alpha = 0.3
```

```text
1.0 0.804 0.875 0.93
0.0 0.819 0.89 0.956
0.3 0.839 0.901 0.956
```

- Yalnızca TF-IDF (`alpha = 1`) P@1 %80,4, yalnızca gömmeler %81,9, karma
  arama %83,9. MRR ve R@3'te de karma önde.
- R@3 %95,6: ilk üç sonuçta neredeyse her zaman doğru bir makale var. Bir
  ürün tek sonuç yerine üç öneri gösterirse kullanıcının işi büyük ölçüde
  görülür.

## 4. "Bilmiyorum" demek

Gerçek bir arama kutusuna her şey yazılır. Motor şu an her sorguya bir
makale öneriyor; destekle ilgisi olmayan bir cümleye de. Basit bir çare:
en yüksek puan bir **eşiğin** altındaysa makale önermemek. Eşiği, gerçek
taleplerin yalnızca %5'ini reddedecek şekilde seçelim ve iki tür ilgisiz
metinle sınayalım: ürün yorumları ve küçük dünya cümleleri.

```python
from corpus_data import make_corpus
from text_data import make_reviews

threshold = float(np.quantile(engine.scores(queries).max(axis=1), 0.05))
reviews = [r["text"] for r in make_reviews(500)]
world = make_corpus(500)
print(round(threshold, 3))
for name, texts in [("reviews", reviews), ("world", world)]:
    top = engine.scores(texts).max(axis=1)
    print(name, round(float((top < threshold).mean()), 3))


def answer(query):
    scores = engine.scores([query])[0]
    if scores.max() < threshold:
        return "no matching article"
    return articles[int(scores.argmax())]["title"]


for text in ["i was charged twice", "we flew to dublin in ireland",
             "the parcel arrived on time , great service"]:
    print(answer(text))
```

```text
0.408
reviews 0.552
world 0.952
Double charges and pending payments
no matching article
Lost, late or damaged parcels
```

- Küçük dünya cümlelerinin %95,2'si reddediliyor: kelimeleri desteğin
  diline uzak.
- Ürün yorumlarının ise yalnızca %55,2'si. Teslimattan söz eden yorumlar
  ("Delivery took 18 days") kargo taleplerinin kelimelerini kullanıyor;
  son örnekte memnun bir müşteri kayıp kargo makalesine yönlendiriliyor.
  Alana **yakın** ilgisiz metni ayırmak, uzak metni ayırmaktan çok daha
  zor.
- Eşiği yükseltmek daha çok ilgisiz metni reddeder ama gerçek talepleri de
  kaçırır (birinci not). Hangi hatanın daha pahalı olduğuna ürün karar
  verir: yanlış makale mi, cevapsız kalan müşteri mi?

## Özet

- Arama motoru = dizin (makalelerin vektörleri bir kez) + sorgu anında
  benzerlik + sıralama.
- Karma arama, kelime eşleşmesini ve anlam benzerliğini birleştirerek her
  ikisinden iyi sonuç verdi: P@1 %83,9, MRR 0,901, R@3 %95,6.
- Bir eşikle "bilmiyorum" demek mümkün, ama alana yakın ilgisiz metin
  (ürün yorumları) eşiği kolayca geçiyor.
- Sonraki adımlar: hataların nerede toplandığına bakmak (ikinci not), daha
  güçlü ön eğitimli vektörler (12) ve ilk sonuçları daha pahalı bir modelle
  yeniden sıralamak.
