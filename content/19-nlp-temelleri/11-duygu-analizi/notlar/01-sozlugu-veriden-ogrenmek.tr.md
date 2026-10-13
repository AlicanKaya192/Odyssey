Sözlüğü elle yazmak yerine etiketli veriden çıkarabilirsin: olumlu yorumlarda
olumsuzlara göre çok daha sık geçen kelime olumlu sayılır. Ölçü **log oran**
(log-odds): bir kelimenin olumlu yorumlarda geçme oranının olumsuz
yorumlardakine oranının logaritması. 08'deki gibi +1 ile yumuşatıyoruz.

```python
import math
import re
from collections import Counter

import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_reviews

TOKEN = re.compile(r"[a-z']+")
reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
counts = {"positive": Counter(), "negative": Counter()}
for text, label in zip(X_train, y_train):
    if label in counts:
        counts[label].update(set(TOKEN.findall(text.lower())))
sizes = {k: int((y_train == k).sum()) for k in counts}


def log_odds(word):
    pos = (counts["positive"][word] + 1) / (sizes["positive"] + 2)
    neg = (counts["negative"][word] + 1) / (sizes["negative"] + 2)
    return math.log(pos / neg)


common = counts["positive"] + counts["negative"]
frequent = sorted(w for w in common if common[w] >= 5)
ranked = sorted(frequent, key=log_odds)
print("negative:", " ".join(ranked[:10]))
print("positive:", " ".join(ranked[::-1][:10]))
```

```text
negative: terrible honest hate of worse waste box damaged late was
positive: works no expected well totally love too packed loves early
```

- Gerçek duygu kelimeleri var ("terrible", "hate", "waste", "love"), ama
  aralarında hiç duygu taşımayanlar da var: "of" ("waste of money"), "box"
  ("the box was damaged"), "wife" ("my wife loves it"), "honest" ("not good,
  to be honest"). Bunlar duygunun değil, **bu verideki kalıpların** izi.
- "no" olumlu çıktı: "I expected it to be bad, but no." kalıbı yalnızca
  olumlu yorumlarda geçiyor. Olumsuzlayıcı kelimeler sözlüğe girmemeli.
- Öğrenilen sözlük modelden farklı değil: bir modelin ağırlıklarının kaba
  bir hâli. Avantajı okunabilir olması; listeye bakıp yanlış kelimeleri elle
  atabilirsin.

## Kaç kelime?

Her yönden ilk k kelimeyi alıp dersteki olumsuzlama kuralıyla puanlayalım:

```python
NEGATORS = {"not", "can't", "never", "no", "don't", "didn't"}


def score(text, good, bad):
    total, left = 0, 0
    for word in re.findall(r"[a-z']+|[.,!?]", text.lower()):
        if word in ".,!?":
            left = 0
        elif word in NEGATORS:
            left = 3
        else:
            value = (word in good) - (word in bad)
            total += -value if left else value
            left = max(left - 1, 0)
    return total


for k in [10, 20, 40]:
    good, bad = set(ranked[::-1][:k]), set(ranked[:k])
    pred = ["positive" if s > 0 else "negative" if s < 0 else "neutral"
            for s in (score(t, good, bad) for t in X_test)]
    print(k, round(float(np.mean(np.array(pred) == y_test)), 3))
```

```text
10 0.612
20 0.754
40 0.708
```

- 20 kelimeyle %75,4: elle yazdığımız 38 kelimelik sözlükle aynı yer.
  10 kelime az kalıyor; 40'ta doğruluk yeniden düşüyor. Daha uzun liste her
  zaman daha iyi değil.
- Burada k'yi test verisine bakarak karşılaştırdık; gerçek işte bu
  sızıntıdır. k bir ayardır ve doğrulama verisiyle (ya da çapraz
  doğrulamayla) seçilir, test en sonda bir kez kullanılır.
