K-Means'te küme sayısını sen veriyorsun. Sık kullanılan bir ölçü **siluet
skoru** (silhouette): her belge için "kendi kümesine ne kadar yakın, en yakın
başka kümeye ne kadar uzak" farkı, −1 ile 1 arasında. 1'e yakın değer
birbirinden net ayrılmış kümeler demek.

```python
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import silhouette_score
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
stop = list(ENGLISH_STOP_WORDS | {"ord", "com", "example", "hi", "hello",
                                  "thanks", "thank", "dear", "support",
                                  "regards", "help"})
X = TfidfVectorizer(stop_words=stop, token_pattern=r"[a-z]{2,}",
                    min_df=5).fit_transform(texts)
for k in [3, 5, 8, 10]:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    score = silhouette_score(X, kmeans.labels_, metric="cosine")
    print(k, round(score, 3), round(kmeans.inertia_))
```

```text
3 0.07 1715
5 0.123 1599
8 0.152 1484
10 0.195 1398
```

- Siluet skorları çok düşük (0,07–0,20): talepler net ayrılmış kümeler
  oluşturmuyor. Metin verisinde bu yaygın; belgeler birçok ortak kelime
  paylaşır, kümeler iç içe geçer.
- Skor k ile birlikte artıyor ve ortada bir zirve yok. Kümelerin içindeki
  uzaklık toplamı (`inertia_`) da her zaman düşüyor. İkisi de bu veride
  "doğru" k'yi göstermiyor.
- Pratikte k'yi kullanıma göre seç: destek ekibinde beş grup varsa 5, daha
  ince bir döküm isteniyorsa 10. Her kümenin kelimelerine ve birkaç
  örneğine bakıp anlamlı olup olmadığına karar ver.
