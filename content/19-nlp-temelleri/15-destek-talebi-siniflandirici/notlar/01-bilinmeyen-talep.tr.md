Model beş kategoriyi biliyor. Peki bir müşteri hiçbirine uymayan bir şey
sorarsa? Sınıflandırıcı "bilmiyorum" diyemez; her talebi beş kategoriden
birine koymak zorunda. Bunu görelim ve modelin **ne kadar emin** olduğuna
bakarak bir "emin değilim" kapısı kuralım:

```python
import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from text_data import make_tickets

MASKS = [(r"\bORD-\d+\b", " ordernum "), (r"\$[\d,]+(?:\.\d{2})?", " amount "),
         (r"\S+@\S+", " email "), (r"\b\d{4}-\d{2}-\d{2}\b", " date "),
         (r"\bE\d{3,4}\b", " errcode ")]


def mask(text):
    for pattern, placeholder in MASKS:
        text = re.sub(pattern, placeholder, text)
    return " ".join(text.lower().split())


tickets = make_tickets(4000)
texts = [t["text"] for t in tickets]
labels = np.array([t["category"] for t in tickets])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer(preprocessor=mask, ngram_range=(1, 2))
pipe = Pipeline([("tfidf", vectorizer), ("model", LinearSVC(C=3))])
pipe.fit(X_train, y_train)
limit = np.percentile(pipe.decision_function(X_test).max(axis=1), 5)
print(round(limit, 2))
new = ["Do you sell gift cards?", "What are your opening hours?",
       "Is this jacket waterproof?", "My order ORD-12345 has not arrived."]
scores = pipe.decision_function(new).max(axis=1)
for text, label, score in zip(new, pipe.predict(new), scores):
    print(f"{label:<10} {score:6.2f} {'unsure' if score < limit else 'ok'}")
```

```text
0.37
account     -0.21 unsure
account     -0.34 unsure
account     -0.37 unsure
shipping     0.69 ok
```

- `decision_function` her kategori için bir puan veriyor; en büyüğü
  tahmin edilen kategori. Puan ne kadar büyükse model o kadar emin.
- Sınırı bilinen taleplerden koyduk: test taleplerinin %95'inin puanı
  0,37'nin üstünde. Puanı bundan düşük olan yeni talep "emin değilim"
  sayılıyor. (Kısa tutmak için sınırı test verisinden aldık; gerçek işte
  bu da bir ayardır ve ayrı bir doğrulama kümesinden seçilir.)
- Kapsam dışı üç soru yine bir kategoriye kondu, ama puanları sınırın
  altında: sistem onları insana yönlendirebilir. Gerçek kargo talebi rahatça
  geçiyor.
- Bu bir eşik, bir garanti değil: kapsam dışı bir talep tesadüfen bir
  kategorinin güçlü kelimelerini içerirse ("card", "order") yüksek puan
  alabilir. Sınırın yeri bir ödünleşim: yükseltirsen insana daha çok talep
  gider, düşürürsen daha çok yanlış yönlendirme olur.
