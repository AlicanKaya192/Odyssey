# TF-IDF

Kelime torbasında "the" her yorumda birkaç kez geçtiği için en büyük
sayılara sahip; ama bir yorumu ötekinden ayırmak için hiçbir işe yaramıyor.
Tersine, yalnızca birkaç yorumda geçen "bluetooth" ya da "damaged" o
yorumlar hakkında çok şey söylüyor. **TF-IDF** bu sezgiyi sayıya döker: bir
kelimenin belgedeki sıklığını (TF), kaç belgede geçtiğinin tersiyle (IDF)
çarpar. Bu bölüm TF-IDF'i önce elle hesaplıyor, sonucu scikit-learn'le
birebir karşılaştırıyor ve gerçek yorumlarda neyi değiştirdiğini ölçüyor.

## IDF: kelime kaç belgede geçiyor?

**Belge sıklığı** (document frequency, df) bir kelimenin kaç farklı belgede
geçtiği. **Ters belge sıklığı** (inverse document frequency, IDF) bunun
tersi: az belgede geçen kelimeye büyük, her belgede geçene küçük değer.
scikit-learn'ün varsayılan formülü:

$$\text{idf}(w) = \ln\frac{1 + n}{1 + \text{df}(w)} + 1$$

Burada $n$ belge sayısı. Paydaki ve paydadaki +1, hiç görülmemiş bir
kelimede sıfıra bölmeyi önlüyor; sondaki +1 her belgede geçen kelimenin
ağırlığının tam sıfır olmamasını sağlıyor.

```python
import math

docs = ["the battery is great", "the battery died", "great price great sound"]
vocab = sorted({w for d in docs for w in d.split()})
n = len(docs)
df = {w: sum(w in d.split() for d in docs) for w in vocab}
idf = {w: math.log((1 + n) / (1 + df[w])) + 1 for w in vocab}
for w in vocab:
    print(w, df[w], round(idf[w], 3))
```

```text
battery 2 1.288
died 1 1.693
great 2 1.288
is 1 1.693
price 1 1.693
sound 1 1.693
the 2 1.288
```

İki belgede geçen "battery", "great" ve "the" 1,288; yalnızca bir belgede
geçenler 1,693 ağırlık aldı. Üç belgelik küçük örnekte fark küçük; büyük
derlemde çok açılacak.

## TF × IDF ve normalleştirme

Belgenin TF-IDF vektörü: her kelimenin belgedeki sayısı çarpı IDF'i. Sonra
vektör **birim uzunluğa** getirilir (L2 normalleştirme): her değer,
değerlerin karelerinin toplamının köküne bölünür.

```python
def tfidf(doc):
    words = doc.split()
    raw = [words.count(w) * idf[w] for w in vocab]
    norm = math.sqrt(sum(x * x for x in raw))
    return [round(x / norm, 3) for x in raw]


for d in docs:
    print(tfidf(d))
```

```text
[0.46, 0.0, 0.46, 0.605, 0.0, 0.0, 0.46]
[0.518, 0.681, 0.0, 0.0, 0.0, 0.0, 0.518]
[0.0, 0.0, 0.732, 0.0, 0.481, 0.481, 0.0]
```

- İlk belgede "is" (yalnızca orada geçiyor) 0,605 ile en büyük ağırlığı aldı;
  "battery", "great", "the" 0,46'da kaldı.
- Üçüncü belgede "great" iki kez geçtiği için 0,732.
- Normalleştirme sayesinde her satırın uzunluğu 1: uzun ve kısa belgeler
  artık aynı ölçekte (05'in son başlığındaki sorun).

## scikit-learn ile karşılaştır

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
print(vectorizer.idf_.round(3).tolist())
mine = np.array([tfidf(d) for d in docs])
print(np.allclose(X.toarray(), mine, atol=1e-3))
```

```text
[1.288, 1.693, 1.288, 1.693, 1.693, 1.693, 1.288]
True
```

`TfidfVectorizer` = `CountVectorizer` + IDF ağırlığı + L2 normalleştirme.
`idf_` niteliği öğrenilen IDF değerleri; bizim elle hesapladıklarımızla
aynı. `np.allclose` iki tablonun bütün değerlerinin (binde bir payla) eşit
olduğunu doğruluyor. Elle yazdığın bir hesabı kütüphaneyle böyle karşılaştır:
formülü gerçekten anladığını gösterir.

## Yorumlarda IDF

```python
from text_data import make_reviews

texts = [r["text"] for r in make_reviews(2000)]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
words = vectorizer.get_feature_names_out()
idf = vectorizer.idf_
order = np.argsort(idf)


def show(indices):
    return [(str(words[i]), round(float(idf[i]), 2)) for i in indices]


print("low ", show(order[:4]))
print("high", show(order[-3:]))
```

```text
low  [('the', 1.12), ('is', 1.54), ('for', 2.25), ('it', 2.33)]
high [('wosre', 7.91), ('wsate', 7.91), ('zpiper', 7.91)]
```

- En düşük IDF'ler "the", "is", "for", "it": neredeyse her yorumda geçen
  kelimeler. TF-IDF onları durak listesine gerek kalmadan bastırıyor.
- En yüksek IDF'ler "wosre", "wsate", "zpiper": **yazım hataları**. Yalnızca
  bir kez geçen her kelime en yüksek IDF'yi alır ve bunların çoğu hata ya da
  tek seferlik numaralardır. TF-IDF nadirliği ödüllendirir; nadirliğin bilgi
  mi gürültü mü olduğunu bilmez. Bu yüzden `min_df` (04) TF-IDF ile çok sık
  birlikte kullanılır.

## Bir yorumun öne çıkan kelimeleri

Aynı yorumda sayımla ve TF-IDF ile en ağır kelimeler:

```python
import textwrap

from sklearn.feature_extraction.text import CountVectorizer

counts = CountVectorizer().fit(texts)
C = counts.transform(texts)
doc = 7
print(textwrap.fill(texts[doc], 60))
row_c = C[doc].toarray().ravel()
row_t = X[doc].toarray().ravel()
print("count", [str(words[i]) for i in np.argsort(row_c)[::-1][:4]])
print("tfidf", [str(words[i]) for i in np.argsort(row_t)[::-1][:4]])
```

```text
Totally worth the money. The colour is not loud at all. I
love the buttons. I love the colour.
count ['the', 'love', 'colour', 'not']
tfidf ['colour', 'love', 'the', 'buttons']
```

Sayımda "the" (dört kez) birinci; TF-IDF'te "colour" ve "love" öne geçti,
"buttons" listeye girdi. "the" üçüncüye düştü ama listeden çıkmadı: IDF'i
küçük olsa da dört kez geçmesi onu hâlâ yukarıda tutuyor. Notlarda bunu
yumuşatan `sublinear_tf` ayarını göreceksin.

## Uzunluk etkisi gitti mi?

```python
lengths = np.asarray(C.sum(axis=1)).ravel()
norms = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel())
print(lengths.min(), lengths.max())
print(norms.min().round(3), norms.max().round(3))
```

```text
3 38
1.0 1.0
```

Yorumlar 3 ile 38 kelime arasında, ama TF-IDF satırlarının hepsinin
uzunluğu 1. `X.multiply(X)` her değerin karesi; satır toplamının kökü
satırın uzunluğu. Bir sonraki bölümde benzerliği ölçerken bu önemli olacak:
iki birim vektörün nokta çarpımı doğrudan aralarındaki açının kosinüsü.

## Özet

- TF bir kelimenin belgedeki sıklığı, IDF kaç belgede geçtiğinin tersi;
  TF-IDF ikisinin çarpımı. Her yerde geçen kelimeler bastırılır, ayırt edici
  olanlar öne çıkar.
- scikit-learn'ün IDF'i $\ln\frac{1+n}{1+\text{df}} + 1$; sonra her satır
  L2 ile birim uzunluğa getirilir. Elle hesap ile `TfidfVectorizer` birebir
  aynı.
- En düşük IDF'ler durak kelimeleri, en yüksekler tek seferlik kelimeler (çoğu
  zaman yazım hatası). Nadirlik bilgi de olabilir gürültü de: `min_df`.
- Normalleştirme uzunluk etkisini kaldırır; bütün satırların uzunluğu 1.
