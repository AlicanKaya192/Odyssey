# Parçalama ve Vektör Arama

Halüsinasyona karşı en güçlü önlem, modele cevabı dayandıracağı metni
vermekti. Ama bir şirketin bütün belgelerini her çağrıda göndermek
mümkün değil: bağlam penceresine sığmaz ve her token ödenir (07). Çözüm,
belgeleri küçük **parçalara** (chunk) bölmek ve her soru için yalnızca
**ilgili** parçaları bulup göndermek. Bu bölüm bu düzeneğin arama yarısını
kuruyor; sonraki bölüm onu modele bağlayacak (RAG).

## Veri: bir mağazanın yardım makaleleri

Alıştırmalarda da kullanılacak `doc_data.py`, kurgusal bir outdoor
mağazasının 14 kısa yardım makalesini (kargo, iade, garanti, çadır
bakımı…) ve 27 soruyu içeriyor. Her sorunun cevabını hangi makalenin
verdiği ve doğru bir cevapta geçmesi gereken kısa bir ifade (`key`)
yazılı; son üç sorunun cevabı makalelerde **yok**.

```python
import re
import numpy as np
from doc_data import DOCS, QUESTIONS
from llm_client import count_tokens

print(len(DOCS), "articles,", len(QUESTIONS), "questions")
print(DOCS[0]["title"])
print(DOCS[0]["text"][:60], "...")
print(QUESTIONS[3])
```

```text
14 articles, 27 questions
Shipping costs and delivery times
Orders over 50 euros ship for free. Smaller orders pay a shi ...
{'q': 'How long do I have to send something back?', 'doc': 'returns', 'key': '30 days'}
```

## Parçalamanın üç yolu

```python
def by_article():
    return [(d["id"], d["title"] + ". " + d["text"]) for d in DOCS]


def by_sentence():
    return [(d["id"], s) for d in DOCS
            for s in re.split(r"(?<=\.) ", d["text"])]


def by_window(size, overlap, title=False):
    chunks = []
    for d in DOCS:
        words = d["text"].split()
        head = d["title"] + ": " if title else ""
        for i in range(0, max(len(words) - overlap, 1), size - overlap):
            chunks.append((d["id"], head + " ".join(words[i:i + size])))
    return chunks


for _, text in by_window(12, 4)[:3]:
    print(text)
```

```text
Orders over 50 euros ship for free. Smaller orders pay a shipping
orders pay a shipping fee of 4.90 euros. Standard delivery takes 3
Standard delivery takes 3 to 5 working days. Express delivery costs 9.90
```

- **Makale başına bir parça:** anlam bütün kalır ama parçalar büyük.
- **Cümle başına bir parça:** küçük ve net, ama bir cümle bazen tek
  başına anlaşılmaz.
- **Sabit pencere:** her parça belli sayıda kelime; ardışık parçalar
  birkaç kelime **örtüşür** (overlap) ki sınırda bölünen bir bilgi en az
  bir parçada bütün kalsın. Yukarıda 12 kelimelik pencereler 4 kelime
  örtüşüyor: her parça bir öncekinin son dört kelimesiyle başlıyor.
  `title=True` her parçanın başına makalenin başlığını ekliyor.

## Vektör arama

Her parçayı bir **vektöre** çeviriyoruz: NLP patikasından tanıdığın TF-IDF.
Bir sorunun vektörü ile parçaların vektörleri arasındaki **kosinüs
benzerliği** en yüksek olan parçalar en ilgili sayılıyor. TF-IDF
vektörlerinin boyu zaten 1 olduğu için kosinüs, iki vektörün iç çarpımı.

```python
from sklearn.feature_extraction.text import TfidfVectorizer


class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        texts = [text for _, text in chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query, k=3):
        q = self.vectorizer.transform([query])
        scores = (self.matrix @ q.T).toarray().ravel()
        best = np.argsort(-scores)[:k]
        return [(self.chunks[i], round(float(scores[i]), 3)) for i in best]


index = Index(by_sentence())
for (doc, text), score in index.search("Do gift cards expire?"):
    print(score, doc)
    print("  " + text)
```

```text
0.383 giftcards
  Gift cards are available for 25, 50 and 100 euros and are valid for 3 years.
0.284 refunds
  Purchases paid with a gift card are refunded as a new gift card.
0.26 loyalty
  Points expire if you make no purchase for 12 months.
```

En ilgili parça, sorudaki "gift cards" kelimelerini taşıyan ve cevabı
("valid for 3 years") veren cümle. Gerçek sistemlerde vektörler genellikle
büyük metinlerle eğitilmiş bir **gömme modelinden** (embedding model)
gelir (NLP patikasında belge gömmeleri) ve milyonlarca parça için
**vektör veritabanları** yaklaşık en yakın komşu (approximate nearest
neighbour) aramasıyla çalışır. Fikir aynı: soruya en yakın vektörler.

## Hangi parçalama daha iyi?

Ölçü olarak, cevaplanabilir 24 sorunun kaçında doğru cevap ifadesinin
(`key`) ilk `k` parçadan birinde geçtiğine bakıyoruz. Yanında, bu `k`
parçanın modele götüreceği ortalama token sayısı:

```python
answerable = [q for q in QUESTIONS if q["doc"]]


def evaluate(chunks, k=3):
    index = Index(chunks)
    hits, tokens = 0, 0
    for q in answerable:
        found = index.search(q["q"], k)
        hits += any(q["key"] in text for (_, text), _ in found)
        tokens += sum(count_tokens(text) for (_, text), _ in found)
    return round(hits / len(answerable), 2), round(tokens / len(answerable))


for name, chunks in [("article", by_article()),
                     ("sentence", by_sentence()),
                     ("window 12", by_window(12, 0)),
                     ("window 12/4", by_window(12, 4)),
                     ("window 12/4+title", by_window(12, 4, True)),
                     ("window 24/8", by_window(24, 8)),
                     ("window 24/8+title", by_window(24, 8, True))]:
    print(f"{name:18} chunks {len(chunks):2}  key@3 {evaluate(chunks)}")
```

```text
article            chunks 14  key@3 (1.0, 225)
sentence           chunks 52  key@3 (0.71, 50)
window 12          chunks 53  key@3 (0.42, 54)
window 12/4        chunks 69  key@3 (0.5, 56)
window 12/4+title  chunks 69  key@3 (0.58, 75)
window 24/8        chunks 33  key@3 (0.88, 106)
window 24/8+title  chunks 33  key@3 (0.88, 125)
```

Makalenin tamamı anahtarı her zaman getiriyor (1,0) ama soru başına 225
token götürüyor. Cümleler dört kat ucuz (50 token) ama 0,71'de kalıyor.
12 kelimelik pencere bilgiyi parçaların arasında bölüyor (0,42); 4 kelime
örtüşme 0,50'ye, başlık eklemek 0,58'e çıkarıyor. 24 kelimelik pencere ve
8 kelime örtüşme, makalelerin yarısı kadar token'la 0,88'e ulaşıyor; orada
başlık bir şey katmıyor, yalnızca token'ı artırıyor. Bu makaleler kısa
olduğu için makalenin tamamını göndermek de iyi bir seçenek; birkaç sayfalık
belgelerde öyle olmaz. En iyi ayar veriye göre değişir ve ölçmeden
seçilmez.

## Arama neyi kaçırıyor?

```python
index = Index(by_window(24, 8, True))
for q in answerable:
    found = index.search(q["q"], 3)
    if not any(q["key"] in text for (_, text), _ in found):
        print(q["q"], "->", found[0][0][0])
```

```text
How much does shipping cost for a 30 euro order? -> payment
How long do I have to send something back? -> warranty
When will I get my money back? -> shipping
```

En iyi ayarla bile üç soru kaçıyor ve üçü de aynı türden: soru,
makaledekinden başka kelimeler kullanıyor. "Send something back" iade
(return) makalesini, "money back" geri ödeme (refund) makalesini
bulamıyor; "30 euro order" ise "orders over 300 euros" geçen ödeme
makalesine gidiyor. TF-IDF yalnızca aynı kelimeleri eşleştirir; "cost" ile
"costs"u bile ayrı sayar. Gömme modelleri anlamca yakın kelimeleri yakın
vektörlere koyduğu için bu tür soruları daha iyi bulur; pratikte kelime
araması ile gömme araması çoğu zaman birlikte kullanılır (**karma arama**,
hybrid search).

## Özet

- Belgeler parçalara bölünür, her soru için yalnızca ilgili parçalar
  bulunup modele gönderilir.
- Parçalar vektöre çevrilir; soruya kosinüs benzerliği en yüksek olanlar
  seçilir. Gerçek sistemlerde vektörler bir gömme modelinden gelir.
- Parça boyu bir ödünleşim: büyük parça bilgiyi bütün tutar ama çok token
  götürür; küçük parça ucuzdur ama bilgiyi bölebilir. Örtüşme ve başlık
  eklemek bölünmeyi azaltır.
- Kelime eşleşmesine dayanan arama, aynı şeyi başka kelimelerle soran
  soruları kaçırır.
- Parçalama ve arama, gerçek sorularla **ölçülerek** seçilir.
