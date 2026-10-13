# Genel Tekrar

Gömmeler ve Dil Modelleri modülünün sonuna geldin. Kelimelerin anlamını
birlikte geçtikleri kelimelerden öğrenmekle başladık, kelimeleri alt
parçalara böldük, sonraki kelimeyi tahmin eden modeller kurduk ve sinir
ağlarıyla RNN'den dikkat mekanizmasına, oradan transformer bloğuna kadar
gittik. Sonra ön eğitimin neyi kazandırdığını, metin üretmeyi ve üretilen
metni değerlendirmeyi ölçtük ve bir arama motoru kurduk. Bu bölüm yolu bir
kez daha yürüyor; sonunda parçaların birlikte çalıştığı küçük bir örnek var.

<figure class="fig">
  <div class="flow">
    <span class="node">Gömmeler<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Dil modeli<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Sinir ağı<br><small>08–11</small></span><span class="arrow">→</span>
    <span class="node">Kullanım<br><small>12–14</small></span><span class="arrow">→</span>
    <span class="node acc">Proje<br><small>15</small></span>
  </div>
  <figcaption>Modülün yolu: kelimeye anlam ver, sırayı modelle, sinir ağıyla öğren, ön eğitimi kullan ve ölç, bir ürün kur.</figcaption>
</figure>

## 1. Gömmeler (Bölüm 0–4)

| İş | Araç |
|---|---|
| Dağılımsal anlam | birlikte geçme sayımları, pencere, kosinüs benzerliği |
| Sayımdan vektöre | PPMI, `np.linalg.svd`, kesik SVD, `α = 0,75` yumuşatma |
| Tahminle öğrenmek | Word2Vec (skip-gram + negatif örnekleme), öğrenme oranı azaltma |
| Vektörlerle çalışmak | benzetme (`king − man + woman`), komşular, önyargı yönü |
| Belge vektörü | kelime vektörlerinin ortalaması, SIF, karma arama |

Gömmeler anlamı değil **kullanımı** öğrenir: zıt anlamlılar aynı bağlamlarda
geçtiği için yakın düşer, verideki önyargı vektörlere geçer.

## 2. Alt kelimeler ve dil modelleri (Bölüm 5–7)

| İş | Araç |
|---|---|
| Alt kelime | BPE birleştirmeleri, sözlük dışı kelime kalmaması |
| n-gram dil modeli | koşullu olasılık, karmaşıklık (perplexity), toplamalı yumuşatma, ara değer |
| Dizi etiketleme | HMM, geçiş ve yayılım olasılıkları, Viterbi |

Yumuşatmasız bir modelin karmaşıklığı sonsuzdur: hiç görülmemiş bir ikili
bütün metnin olasılığını sıfırlar.

## 3. Sinir ağları (Bölüm 8–11)

| İş | Araç |
|---|---|
| Sınıflandırma ağı | gömme katmanı, ReLU, softmax, çapraz entropi, türev denetimi |
| RNN | gizli durum, zamanda geri yayılım, türev kırpma, LSTM/GRU kapıları |
| Dikkat | sorgu, anahtar, değer; `√d` ile ölçekleme; softmax türevi |
| Transformer | kendi kendine dikkat, konum kodlaması, nedensel maske, çok başlı dikkat, katman normu, artık bağlantı |

Dikkat her kelimeye tek adımda bakar ve paralel hesaplanır; bedeli `n × n`
puan tablosu.

## 4. Kullanmak ve ölçmek (Bölüm 12–14)

| İş | Araç |
|---|---|
| Ön eğitim | etiketsiz metin, aktarım, az etiketle öğrenme eğrisi, sıfır atış |
| Metin üretimi | açgözlü seçim, ışın araması, sıcaklık, top-k, top-p, distinct-n |
| Değerlendirme | BLEU, ROUGE, Cohen'in kappa'sı |

Ön eğitim en çok etiket azken kazandırır ve doğru alandan gelmelidir;
otomatik ölçüler yüzeyi ölçer, anlamı değil.

## 5. Proje (Bölüm 15)

Dizin, karma puan, P@1 / MRR / R@3, "bilmiyorum" eşiği ve hata analizi.

## Hepsi birlikte

Etiketsiz taleplerden vektör öğrenen, yalnızca **100 etiketli** taleple
kategori tahmin eden ve aynı vektörlerle makale öneren küçük bir sistem:

```python
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from text_data import make_articles, make_tickets

TOKEN = re.compile(r"[a-z]+")
docs = [TOKEN.findall(t["text"].lower()) for t in make_tickets(20000, seed=1)]
counts = Counter(w for d in docs for w in d)
vocab = sorted(w for w in counts if counts[w] >= 3)
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for d in docs:
    ids = [index[w] for w in d if w in index]
    for i, a in enumerate(ids):
        for b in ids[max(0, i - 4):i] + ids[i + 1:i + 5]:
            M[a, b] += 1
with np.errstate(divide="ignore", invalid="ignore"):
    P = np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))
U, S, _ = np.linalg.svd(np.nan_to_num(np.maximum(P, 0)))
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)


def embed(text):
    ids = [index[w] for w in TOKEN.findall(text.lower())
           if w in index and w not in ENGLISH_STOP_WORDS]
    v = E[ids].mean(axis=0) if ids else np.zeros(E.shape[1])
    return v / (np.linalg.norm(v) or 1)


tickets = make_tickets(1100)
X = np.array([embed(t["text"]) for t in tickets])
y = np.array([t["category"] for t in tickets])
model = LogisticRegression(max_iter=1000, C=10).fit(X[:100], y[:100])
print(round(float(np.mean(model.predict(X[100:]) == y[100:])), 3))
articles = make_articles()
A = np.array([embed(a["title"] + " " + a["text"]) for a in articles])
question = embed("My parcel ORD-55120 arrived damaged, can I get a refund?")
best = articles[int((A @ question).argmax())]["title"]
print(model.predict([question])[0], "|", best)
```

```text
0.897
shipping | Lost, late or damaged parcels
```

- **Gömmeler:** 20 000 etiketsiz talepten PPMI + SVD ile 50 boyutlu
  vektörler (01).
- **Ön eğitim ve aktarım:** yalnızca 100 etiketle sınıflandırıcı; talep
  vektörü kelime vektörlerinin ortalaması (04, 12).
- **Arama:** aynı vektörlerle soru en yakın makaleye gidiyor (04, 15).
- 100 etiketle ayrı 1000 talepte %89,7 doğruluk: 12'deki öğrenme
  eğrisinde ön eğitimin en çok kazandırdığı bölge.

Sistem soruyu kargo olarak sınıflandırdı ve kargo makalesini önerdi. NLP
Temelleri'nin genel tekrarındaki TF-IDF sistemi aynı soruya "refund"
demişti. İkisi de haklı sayılır: soru hem hasarlı bir kargo ("arrived
damaged") hem bir iade isteği ("refund"). Tek bir etiket bu talebi tam
anlatmıyor; gerçek sistemler bu yüzden çoğu zaman birden çok etiket ya da
ilk üç öneriyi gösterir (15).

## Sonra

Bu modülde her şeyi NumPy ile, içini görerek kurduk. Gerçek dil modelleri
aynı parçalardan oluşur: alt kelime parçalayıcı, gömme tablosu, üst üste
transformer blokları, sonraki kelime kaybı ve bir kod çözme yöntemi. Fark
ölçekte: milyarlarca parametre, trilyonlarca kelime ve bunları çalıştıran
donanım. Notlarda modülün tek sayfalık özeti ve buradan nereye gidileceği
var.
