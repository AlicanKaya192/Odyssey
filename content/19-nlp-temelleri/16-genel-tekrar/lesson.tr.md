# Genel Tekrar

NLP Temelleri modülünün sonuna geldin. Ham ve kirli metni temizlemekten
kelimeleri saymaya, belgeleri vektöre çevirmekten sınıflandırmaya, etiketsiz
metinde konu ve küme bulmaktan metnin içinden bilgi çekmeye kadar klasik
NLP'nin bütün araç kutusunu gördün ve bir destek sistemi kurdun. Bu bölüm
yolu bir kez daha yürüyor; sonunda modülün parçalarının birlikte çalıştığı
küçük bir örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">Metin<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Vektör<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Sınıflandırma<br><small>08–11</small></span><span class="arrow">→</span>
    <span class="node">Etiketsiz<br><small>12–13</small></span><span class="arrow">→</span>
    <span class="node acc">Çıkarma<br><small>14–15</small></span>
  </div>
  <figcaption>Modülün yolu: metni hazırla, sayılara çevir, sınıflandır, etiketsiz metni grupla, içinden bilgi çek.</figcaption>
</figure>

## 1. Metni hazırlamak (Bölüm 0–4)

| İş | Araç |
|---|---|
| Kodlama ve temizlik | bayt ve kod noktası, `unicodedata.normalize("NFKC")`, `html.unescape`, Türkçe büyük-küçük harf |
| Parçalamak | `re.findall`, kendi desenin, cümlelere bölmek, Türkçede kesme işareti |
| Normalleştirmek | durak kelimeler, kök bulma, sözlük biçimi, yer tutucu |
| Saymak | n-gram, harf n-gram'ları, PMI, Zipf yasası |

Önce metne bak; temizlik görevine göre seçilir. "not" bir durak kelime
listesinde olabilir ama duygu analizinde anlamı taşır.

## 2. Metinden vektöre (Bölüm 5–7)

| İş | Araç |
|---|---|
| Kelime torbası | `CountVectorizer`, seyrek matris, dağarcık dışı kelime, sayı ya da var-yok |
| Ağırlık | `TfidfVectorizer`: IDF, satır başına `l2`, uzunluk etkisi |
| Benzerlik ve arama | kosinüs benzerliği, precision@1, BM25 |

Vektörleştirici **yalnızca eğitim verisiyle** kurulur; yeni metin
`transform` ile gelir.

## 3. Sınıflandırma (Bölüm 8–11)

| İş | Araç |
|---|---|
| Olasılıksal | `MultinomialNB`, Laplace yumuşatması |
| Doğrusal | `LogisticRegression`, `LinearSVC`, `coef_`, `class_weight` |
| Ölçü | karışıklık matrisi, kesinlik, duyarlılık, F1, macro F1, karar eşiği |
| Düzen | `Pipeline`, `cross_val_score`, `GridSearchCV` (`adım__parametre`) |
| Duygu | sözlük + olumsuzlama, görüş yönü bazında duygu |

Kelime çiftleri olumsuzlamayı yakalar; `best_score_` iyimserdir; etiketli
veri varsa model sözlüğü açık ara geçer.

## 4. Etiketsiz metin (Bölüm 12–13)

| İş | Araç |
|---|---|
| Konu | `NMF` (TF-IDF), `LatentDirichletAllocation` (sayımlar) |
| Küme | `KMeans`, siluet skoru, saflık |
| Yakın kopya | harf n-gram kümeleri, Jaccard, MinHash, LSH |

Konular senin kategorilerin değildir; konu ve küme sayısını okunurluğa göre
seç; kalıcı özet için kararlı bir özet fonksiyonu kullan.

## 5. Bilgi çıkarma ve proje (Bölüm 14–15)

| İş | Araç |
|---|---|
| Biçimli alan | düzenli ifade, `\b`, `(?:...)`, adlı grup, altın standart |
| Ad listesi | sözlük (gazetteer), belirsizlik |
| Proje | taban çizgisi, maskeleme, hata analizi, "emin değilim" kapısı |

## Hepsi birlikte

Bir talebi alıp kategorisini tahmin eden, sipariş numarasını çeken ve
yardım merkezinden en uygun makaleyi öneren küçük bir sistem:

```python
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_articles, make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])


def mask(text):
    text = re.sub(r"\bORD-\d+\b", " ordernum ", text)
    return " ".join(text.lower().split())


vectorizer = TfidfVectorizer(preprocessor=mask, ngram_range=(1, 2))
pipe = Pipeline([("tfidf", vectorizer), ("model", LinearSVC())])
scores = cross_val_score(pipe, texts, labels, cv=5, scoring="f1_macro")
print(round(scores.mean(), 3))
pipe.fit(texts, labels)
articles = make_articles()
search = TfidfVectorizer(stop_words="english")
A = search.fit_transform([a["title"] + " " + a["text"] for a in articles])
question = "My parcel ORD-55120 arrived damaged, can I get a refund?"
best = cosine_similarity(search.transform([question]), A).argmax()
print(pipe.predict([question])[0], re.findall(r"\bORD-\d{5}\b", question))
print(articles[best]["title"])
```

```text
0.962
refund ['ORD-55120']
Lost, late or damaged parcels
```

- **Hazırlık:** maskeleme sipariş numaralarını tek bir yer tutucuya
  çevirdi ve küçük harfe indirdi (01, 15).
- **Sınıflandırma:** TF-IDF + kelime çiftleri + doğrusal SVM bir
  Pipeline'da; ölçü 5 katlı çapraz doğrulamayla macro F1 (09, 10).
- **Arama:** makaleler TF-IDF vektörleri, soru en yakın makaleye kosinüs
  benzerliğiyle gidiyor (07).
- **Çıkarma:** sipariş numarası düzenli ifadeyle (14).

Sistem talebi iade olarak sınıflandırdı, sipariş numarasını çekti ve
"kayıp, geç ya da hasarlı paketler" makalesini önerdi. "Hasarlı ürün için
iade ya da değişim" makalesi belki daha uygundu; ama arama yalnızca kelime
örtüşmesine bakıyor ve "parcel" yalnızca seçilen makalede geçiyor.
Her parça bu modülde tek tek kuruldu; birlikte gerçek bir iş görüyorlar,
sınırlarıyla birlikte.

## Sonra

Bu modülde metni **kelime sayımlarıyla** temsil ettik. Bu temsilin bildiğin
sınırları var: "car" ile "automobile" iki ayrı sütun, hiç ortak noktaları
yok; kelimelerin sırası kayboluyor. **Gömmeler ve Dil Modelleri**
modülünde kelimelerin anlamını yakalayan vektörler, sırayı modelleyen dil
modelleri ve dikkat mekanizmasıyla transformer'a kadar gideceğiz. Notlarda
bütün modülün tek sayfalık özeti ve buradan nereye gidileceği var.
