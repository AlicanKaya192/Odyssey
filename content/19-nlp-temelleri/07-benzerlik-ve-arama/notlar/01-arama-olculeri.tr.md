Derste yalnızca ilk sonuca baktık. Kullanıcı çoğu zaman ilk birkaç sonucu
okur; bu yüzden arama birkaç ölçüyle değerlendirilir.

| Ölçü | Sorusu |
|---|---|
| precision@k | İlk k sonucun içinde doğru bir sonuç var mı? (oran) |
| MRR (mean reciprocal rank) | İlk doğru sonuç kaçıncı sırada? 1/sıra'nın ortalaması |
| recall@k | Doğru sonuçların ne kadarı ilk k'da? (birden çok doğru varsa) |

## Ölçelim

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_data import make_articles, make_tickets

articles = make_articles()
texts = [a["title"] + ". " + a["text"] for a in articles]
cats = np.array([a["category"] for a in articles])
tickets = make_tickets(1000)
truth = np.array([t["category"] for t in tickets])
vec = TfidfVectorizer().fit(texts)
queries = vec.transform([t["text"] for t in tickets])
S = cosine_similarity(queries, vec.transform(texts))
ranked = np.argsort(S, axis=1)[:, ::-1]
for k in [1, 3, 5]:
    hit = (cats[ranked[:, :k]] == truth[:, None]).any(axis=1)
    print(k, round(float(hit.mean()), 3))
first = (cats[ranked] == truth[:, None]).argmax(axis=1) + 1
print(round(float((1 / first).mean()), 3))
```

```text
1 0.784
3 0.908
5 0.962
0.858
```

- `ranked` her sorgu için makalelerin puana göre sırası. `cats[ranked[:, :k]]`
  ilk k makalenin kategorileri; `truth[:, None]` her sorgunun doğru
  kategorisini o k sütuna yayıyor (yayınlama, broadcasting).
- İlk sonuçta %78,4, ilk üçte %90,8, ilk beşte %96,2. Ekranda üç sonuç
  gösteren bir yardım merkezi, taleplerin %90'ında doğru makaleyi gösteriyor.
- `first` ilk doğru makalenin sırası; **MRR** 1/sıra'nın ortalaması: 0,858.
  İlk sırada bulmak 1, ikinci sırada 0,5 puan. Tek bir sayıyla "doğru sonuç
  ne kadar yukarıda" sorusunu cevaplar.

## Hangisini kullanmalı?

- Kullanıcı yalnızca ilk sonuca bakıyorsa (otomatik yanıt, "Bunu mu
  demek istediniz?") precision@1.
- Kullanıcı bir liste görüyorsa precision@3 ya da @5 ve MRR.
- Değerlendirme sorguları **gerçek** sorgulara benzemeli. Elle yazılmış
  "kolay" sorgularla ölçülen bir arama motoru gerçekte çok daha kötü olabilir.
