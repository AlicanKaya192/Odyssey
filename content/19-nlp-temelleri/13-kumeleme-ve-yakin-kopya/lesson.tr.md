# Kümeleme ve Yakın Kopya

Bu bölümde etiketsiz metinlerle iki iş daha yapacağız. Önce **kümeleme**
(clustering): benzer belgeleri gruplara ayırmak. Konu modellemeden farkı her
belgenin tek bir kümeye düşmesi. Sonra **yakın kopya** (near duplicate)
bulmak: aynı metnin küçük farklarla tekrar eden hâlleri. Yorum sitelerinde,
haber akışlarında ve eğitim verisi toplarken bu kopyalar sonucu bozar. Bütün
çiftleri karşılaştırmak büyük veride imkânsızlaşır; bunun için **MinHash** ve
**LSH** (locality-sensitive hashing, konuma duyarlı özetleme) adlı iki fikri
sıfırdan kuracağız.

## K-Means ile talepleri kümelemek

ML Algoritmaları'nda gördüğün K-Means'i TF-IDF vektörlerine uygulayalım.
Ön işleme 12'dekiyle aynı:

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
categories = np.array([t["category"] for t in tickets])
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
tfidf = TfidfVectorizer(stop_words=stop, token_pattern=r"[a-z]{2,}", min_df=5)
X = tfidf.fit_transform(texts)
words = tfidf.get_feature_names_out()
kmeans = KMeans(n_clusters=5, n_init=10, random_state=0).fit(X)
for i, center in enumerate(kmeans.cluster_centers_):
    size = (kmeans.labels_ == i).sum()
    print(i, size, " ".join(words[center.argsort()[::-1][:5]]))
table = pd.crosstab(pd.Series(kmeans.labels_, name="cluster"),
                    pd.Series(categories, name="category"))
print(table)
print(round(table.max(axis=1).sum() / len(categories), 3))
```

```text
0 415 account email address log access
1 547 order card refund invoice money
2 122 arrived box parcel damaged open
3 419 delivered order address does got
4 497 app error page order history
category  account  billing  refund  shipping  technical
cluster                                                
0             347       48       1         9         10
1              52      259     174        53          9
2               2        1       0       119          0
3               2        2       7       401          7
4               7        8       2        11        469
0.798
```

- Bir kümenin **merkezi** (`cluster_centers_`) kümedeki belgelerin ortalama
  TF-IDF vektörü. En büyük değerli kelimeleri kümeyi anlatıyor.
- Saflık 0,798: aynı veride NMF'in en ağır konusuyla 0,692 almıştık. Her
  talep tek kümeye düştüğü için kısa, tek konulu metinlerde kümeleme daha
  doğal.
- Fatura ve iade yine **tek bir para kümesinde** (1) birleşti: 259 fatura,
  174 iade. Kümeleme de kelimelere bakıyor; aynı kelimeleri kullanan iki
  kategori ayrılmıyor.
- `TfidfVectorizer` satırları birim uzunluğa getirdiği için (`norm="l2"`)
  öklit uzaklığı burada kosinüs benzerliğiyle aynı sıralamayı veriyor;
  K-Means'i metinde bu yüzden doğrudan kullanabiliyoruz.

## Tam kopyalar

Yorumlara geçelim. Önce birebir aynı olanlar: harfleri küçültüp boşlukları
teke indirince aynı kalan metinler.

```python
from collections import Counter

from text_data import make_reviews

reviews = [r["text"] for r in make_reviews(1000)]


def normalize(text):
    return " ".join(text.lower().split())


groups = Counter(normalize(t) for t in reviews)
repeated = {t: n for t, n in groups.items() if n > 1}
print(len(repeated), sum(repeated.values()))
print(groups.most_common(2))
```

```text
9 26
[('exactly what i needed.', 6), ('my brother loves it too.', 3)]
```

Tam kopyayı bulmak kolay ve hızlı: bir sözlük (ya da özet tablosu) yeter,
her metin bir kez işlenir. Ama "Exactly what I needed." ile "Exactly what I
needed!!" farklı metinler sayılıyor.

## Jaccard benzerliği

İki metni **parçalarının kümesi** olarak düşünelim. Parça olarak harf
5-gram'ları (shingle, kiremit) alıyoruz. **Jaccard benzerliği** iki kümenin
kesişiminin birleşimine oranı: 1 aynı, 0 ortak parça yok.

```python
from itertools import combinations


def shingles(text, n=5):
    text = normalize(text)
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    return len(a & b) / len(a | b)


print(round(jaccard(shingles("Exactly what I needed."),
                    shingles("Exactly what I needed!!")), 2))
S = [shingles(t) for t in reviews]
all_pairs = list(combinations(range(len(S)), 2))
near = {(i, j) for i, j in all_pairs if jaccard(S[i], S[j]) >= 0.8}
exact = [(i, j) for i, j in near if normalize(reviews[i]) == normalize(reviews[j])]
print(len(all_pairs), len(near), len(near) - len(exact))
```

```text
0.85
499500 46 15
```

- İki "Exactly what I needed" yorumunun benzerliği 0,85: ünlemler birkaç
  parçayı değiştiriyor, gerisi aynı.
- 1000 yorum 499 500 çift demek. Eşiği (0,8) geçen 46 çiftin 15'i tam
  kopya değil: cümleleri yer değiştirmiş, büyük harfle yazılmış ya da sonuna
  ünlem eklenmiş yorumlar.
- Sorun ölçek: çift sayısı n²/2 büyüyor. Bu bilgisayarda 1000 yorumun
  çiftleri birkaç saniye sürüyor; 2000 yorum dört katı, bir milyon yorum
  500 milyar çift. Her çifti karşılaştırmadan benzerleri bulmak gerekiyor.

## MinHash: kümeyi kısa bir imzaya sıkıştırmak

**MinHash** fikri: bir özet fonksiyonuyla kümenin her parçasına bir sayı ver
ve **en küçüğünü** al. İki kümenin en küçük değerinin aynı çıkma olasılığı
tam olarak Jaccard benzerlikleri kadar. 64 farklı özet fonksiyonuyla 64
sayılık bir **imza** kurarsan, aynı çıkan sayıların oranı Jaccard'ı tahmin
eder.

```python
import zlib

NUM = 64


def minhash(shingle_set):
    return [min(zlib.crc32(f"{seed}:{s}".encode()) for s in shingle_set)
            for seed in range(NUM)]


def estimate(sig_a, sig_b):
    return sum(a == b for a, b in zip(sig_a, sig_b)) / NUM


pairs = [("Exactly what I needed.", "Exactly what I needed!!"),
         ("The strap is great.", "The strap is weak."),
         ("Waste of money.", "Arrived early and well packed.")]
for a, b in pairs:
    sa, sb = shingles(a), shingles(b)
    print(round(jaccard(sa, sb), 2), round(estimate(minhash(sa), minhash(sb)), 2))
signatures = [minhash(s) for s in S]
```

```text
0.85 0.92
0.45 0.42
0.0 0.0
```

- Soldaki gerçek Jaccard, sağdaki 64 sayılık imzadan tahmin. Tahmin yakın
  ama kesin değil: 64 sayıyla tahminin standart sapması en fazla 0,06
  (benzerlik 0,5 iken); ilk çiftte 0,07 sapma var. Sayı artınca daralır.
- Özet fonksiyonu olarak `zlib.crc32` kullanıyoruz, tohumu (`seed`) metnin
  başına ekleyerek 64 farklı fonksiyon elde ediyoruz. Python'un kendi
  `hash()`'i neden kullanılmıyor, ikinci not anlatıyor.
- İmza bir kümeden çok daha küçük ve **her yorum için bir kez** hesaplanıyor.
  Ama imzaları çift çift karşılaştırmak hâlâ n² iş.

## LSH: yalnızca aday çiftleri karşılaştırmak

**LSH** imzayı **bantlara** böler: 64 sayı = 8 bant × 8 sayı. İki yorumun
herhangi bir bandı birebir aynıysa onlar **aday çift** olur. Aynı bantlar
aynı kovaya düşer; yalnızca aynı kovadakiler karşılaştırılır.

```python
from collections import defaultdict

BANDS, ROWS = 8, 8
buckets = defaultdict(list)
for idx, sig in enumerate(signatures):
    for b in range(BANDS):
        buckets[(b, tuple(sig[b * ROWS:(b + 1) * ROWS]))].append(idx)
candidates = set()
for members in buckets.values():
    candidates.update(combinations(members, 2))
found = {(i, j) for i, j in candidates if jaccard(S[i], S[j]) >= 0.8}
print(len(candidates), len(found), round(len(found) / len(near), 3))
for s in [0.5, 0.7, 0.8, 0.9]:
    print(s, round(1 - (1 - s ** ROWS) ** BANDS, 3))
```

```text
77 44 0.957
0.5 0.031
0.7 0.378
0.8 0.77
0.9 0.989
```

- 499 500 çift yerine yalnızca 77 aday çifti gerçek Jaccard ile
  karşılaştırdık ve eşiği geçen 46 çiftin 44'ünü (%95,7) bulduk. Kaçan iki
  çift imzada şanssız kalanlar.
- Alttaki tablo kuramsal: Jaccard'ı s olan bir çiftin aday olma olasılığı
  `1 - (1 - s^r)^b`. 0,5 benzerlikteki çiftler neredeyse hiç aday olmuyor,
  0,9'dakiler neredeyse hep. Bant ve satır sayısıyla bu S eğrisinin keskin
  geçişini istediğin eşiğe kaydırırsın: daha çok bant daha çok aday (daha az
  kaçırma, daha çok iş).
- Arama motorları, eğitim verisi temizleme ve intihal denetimi milyonlarca
  belgede yakın kopyaları bu fikirle bulur.

## Özet

- K-Means her belgeyi tek kümeye koyar; kısa talepler için konu modelinden
  daha saf gruplar verdi (0,798). Kategorileri yine bilmez.
- Tam kopya için normalleştirme + sözlük yeter.
- Yakın kopya için Jaccard benzerliği: harf n-gram kümelerinin kesişimi /
  birleşimi. Bütün çiftleri karşılaştırmak n² büyür.
- MinHash bir kümeyi kısa bir imzaya sıkıştırır; eşit sayıların oranı
  Jaccard'ı tahmin eder.
- LSH imzayı bantlara böler ve yalnızca bir bandı tutan aday çiftleri
  karşılaştırır; çok az işle benzerlerin neredeyse hepsini bulur.
