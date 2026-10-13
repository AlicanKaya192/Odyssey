# Benzerlik ve Arama

Metni sayılara çevirince her belge bir **vektör**, yani çok boyutlu bir
uzayda bir nokta oluyor. Bu bize yeni bir soru sorma imkânı veriyor: iki
belge birbirine ne kadar **benziyor**? Arama motorları, "buna benzer
ürünler", yinelenen destek taleplerini bulmak ve ikinci modüldeki anlamsal
arama bu soruya dayanır. Bu bölüm iki benzerlik ölçüsünü karşılaştırıyor,
yardım makaleleri üzerinde küçük bir arama motoru kuruyor, aramanın ne kadar
iyi olduğunu ölçüyor ve arama motorlarının klasik formülü BM25'i sıfırdan
yazıyor.

## Uzaklık mı, açı mı?

Dağarcığı 05'teki gibi yedi kelime olan üç belge düşünelim: "the battery is
great", aynı cümlenin üç kez tekrarı ve "great price great sound".

```python
import numpy as np

a = np.array([1, 0, 1, 1, 0, 0, 1])
b = 3 * a
c = np.array([0, 0, 2, 0, 1, 1, 0])


def cosine(x, y):
    return x @ y / (np.linalg.norm(x) * np.linalg.norm(y))


print(np.linalg.norm(a - b).round(3), cosine(a, b).round(3))
print(np.linalg.norm(a - c).round(3), cosine(a, c).round(3))
```

```text
4.0 1.0
2.449 0.408
```

- **Öklid uzaklığı** (`np.linalg.norm(a - b)`) iki noktanın arasındaki düz
  çizginin boyu. Aynı cümlenin üç kez tekrarına (b) uzaklık 4; konusu başka
  olan c'ye 2,449. Öklide göre a, c'ye daha yakın: yanlış.
- **Kosinüs benzerliği** iki vektörün arasındaki açının kosinüsü: nokta
  çarpımı, uzunlukların çarpımına bölünür. Yön aynıysa 1, hiç ortak kelime
  yoksa 0. a ile b aynı yönü gösteriyor: 1. a ile c yalnızca "great"i
  paylaşıyor: 0,408.
- Metinde uzunluk bir anlam taşımaz, yön taşır. Bu yüzden metin benzerliği
  neredeyse her zaman kosinüsle ölçülür.

## TF-IDF ile kosinüs

06'da gördük: TF-IDF satırları birim uzunlukta. Birim vektörlerde
kosinüs **nokta çarpımın ta kendisi**; paydaya gerek yok.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = ["the battery is great", "the battery died", "great price great sound"]
X = TfidfVectorizer().fit_transform(docs)
print((X @ X.T).toarray().round(3).tolist())
print(np.allclose((X @ X.T).toarray(), cosine_similarity(X)))
```

```text
[[1.0, 0.476, 0.337], [0.476, 1.0, 0.0], [0.337, 0.0, 1.0]]
True
```

`X @ X.T` her belgenin her belgeyle benzerliğini veren bir tablo: köşegen 1
(her belge kendisine tam benzer), birinci ve ikinci belge "the battery"
ortaklığıyla 0,476, birinci ve üçüncü "great" ile 0,337; üçüncü belge
ikinciyle hiçbir kelime paylaşmıyor: 0.
`cosine_similarity` aynı tabloyu verir ve normalleştirilmemiş vektörlerde de
çalışır.

## Bir arama motoru

`text_data.py`'deki `make_articles()` bir yardım merkezinin 15 makalesini
veriyor; her destek kategorisinden üç makale. Bir soruyu makalelerle
karşılaştıralım:

```python
from text_data import make_articles

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]
vectorizer = TfidfVectorizer().fit(texts)
A = vectorizer.transform(texts)


def search(query, k=3):
    scores = cosine_similarity(vectorizer.transform([query]), A).ravel()
    best = np.argsort(scores)[::-1][:k]
    return [(articles[i]["title"], round(float(scores[i]), 3)) for i in best]


for title, score in search("I forgot my password"):
    print(score, title)
```

```text
0.338 Resetting your password
0.106 Locked accounts and login problems
0.0 Refund or replacement for a damaged item
```

- Vektörleştirici makalelerle `fit` ediliyor: dağarcık ve IDF aranan
  belgelerden geliyor. Sorgu yalnızca `transform` ediliyor.
- İlk sonuç doğru makale. Puanlar düşük görünse de (0,338) önemli olan
  **sıralama**: kosinüs puanının mutlak değeri belge ve sorgu uzunluğuna
  göre değişir.
- Üçüncü sonucun puanı **0**: sorguyla hiçbir kelime paylaşmıyor, yalnızca
  listeyi doldurmak için orada. Gerçek bir arama motoru 0 puanlı sonucu
  göstermez.

## Kelime uyuşmazlığı

```python
for title, score in search("money back for broken item", k=2):
    print(score, title)
```

```text
0.294 Refund or replacement for a damaged item
0.109 How refunds work
```

Doğru makale ("Refund or replacement for a damaged item") bulundu, ama
yalnızca "item" ve "for" kelimeleri sayesinde: sorgu "money back" ve
"broken" diyor, makale "refund" ve "damaged". Kelime torbası ve TF-IDF
yalnızca **aynı kelimeleri** eşleştirir; eş anlamlıları bilmez. Buna
**kelime uyuşmazlığı** (vocabulary mismatch) denir. İkinci modüldeki
gömmeler bu sorunu çözmek için var.

## Aramayı ölçmek

Bir arama motorunun iyi olup olmadığını tek tek sorguya bakarak anlayamayız.
1000 destek talebini sorgu olarak kullanalım: ilk sıradaki makalenin
kategorisi talebin kategorisiyle aynıysa isabet. Bu ölçünün adı
**precision@1** (ilk sonuçta isabet oranı).

```python
from sklearn.feature_extraction.text import CountVectorizer
from text_data import make_tickets

tickets = make_tickets(1000)
queries = [t["text"] for t in tickets]
truth = np.array([t["category"] for t in tickets])
cats = np.array([a["category"] for a in articles])


def precision_at_1(vec):
    vec.fit(texts)
    scores = cosine_similarity(vec.transform(queries), vec.transform(texts))
    return round(float((cats[scores.argmax(axis=1)] == truth).mean()), 3)


print("count", precision_at_1(CountVectorizer()))
print("tfidf", precision_at_1(TfidfVectorizer()))
print("tfidf+stop", precision_at_1(TfidfVectorizer(stop_words="english")))
```

```text
count 0.678
tfidf 0.784
tfidf+stop 0.809
```

- Sayımla %67,8; TF-IDF %78,4. IDF, "the", "my", "I" gibi her yerde geçen
  kelimelerin puanı şişirmesini engelledi.
- Durak listesi bu görevde biraz daha iyi (%80,9): burada olumsuzlama önemli
  değil, konu önemli (03'teki kural: göreve göre).
- %100 değil, çünkü taleplerin bir kısmı başka kategoriden cümle de içeriyor
  ve bazı talepler makalelerde hiç geçmeyen kelimelerle yazılmış.

## BM25

Arama motorlarının on yıllardır kullandığı klasik formül **BM25**. TF-IDF'e
benzer, iki farkla: bir kelimenin tekrarı belli bir noktadan sonra puanı çok
artırmaz (doyma, `k1`) ve uzun belgeler ortalama uzunluğa göre cezalandırılır
(`b`).

```python
import math
from collections import Counter

analyze = CountVectorizer().build_analyzer()
tokens = [analyze(t) for t in texts]
avg_len = sum(len(t) for t in tokens) / len(tokens)
df = Counter(w for t in tokens for w in set(t))
N = len(tokens)


def bm25(query, k1=1.5, b=0.75):
    scores = []
    for doc in tokens:
        tf = Counter(doc)
        norm = k1 * (1 - b + b * len(doc) / avg_len)
        score = 0.0
        for w in analyze(query):
            if w in tf:
                idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
                score += idf * tf[w] * (k1 + 1) / (tf[w] + norm)
        scores.append(score)
    return scores


S = np.array([bm25(q) for q in queries])
print("bm25", round(float((cats[S.argmax(axis=1)] == truth).mean()), 3))
```

```text
bm25 0.755
```

- `tf[w] * (k1 + 1) / (tf[w] + norm)` kelimenin belgedeki sayısı arttıkça
  `k1 + 1`'e yaklaşır ama onu geçmez: bir kelimenin 10 kez geçmesi 1 kez geçmesinden en fazla 2,5
  kat değerlidir.
- `norm` belge uzunluğunu hesaba katar; `b = 0.75` bu etkinin gücü: uzun
  belgede aynı sayı daha az değerlidir.
- Bu veride BM25 (%75,5) TF-IDF'i (%78,4) geçemedi. Makaleler kısa ve
  uzunlukları birbirine yakın; BM25'in uzunluk düzeltmesi burada bir şey
  kazandırmıyor. Uzunlukları çok farklı belgelerde (web sayfaları, kitaplar)
  BM25 genellikle öne geçer. Hangi yöntemin daha iyi olduğunu her zaman
  **kendi verinde ölç**; "en iyi yöntem" diye bilinen bir formül her veride
  en iyi değildir.

## Özet

- Belgeler vektördür; metin benzerliği uzaklıkla değil **kosinüsle** ölçülür
  (uzunluk değil yön önemli).
- TF-IDF satırları birim uzunlukta: kosinüs = nokta çarpımı, `X @ X.T`.
- Arama: belgeleri `fit` + `transform`, sorguyu yalnızca `transform`,
  kosinüse göre sırala.
- Kelime torbası eş anlamlıları bilmez (broken / damaged): kelime
  uyuşmazlığı.
- Aramayı precision@1 gibi bir ölçüyle, gerçek sorgularla değerlendir. Bu
  veride TF-IDF %78,4, durak listesiyle %80,9, BM25 %75,5.
