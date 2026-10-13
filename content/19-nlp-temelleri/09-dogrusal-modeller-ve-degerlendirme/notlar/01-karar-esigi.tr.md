Model "olumsuz" kararını bir olasılıktan verir: olasılık 0,5'i geçince.
Bu **eşik** (threshold) değiştirilebilir ve kesinlik ile duyarlılık arasındaki
ödünleşimi doğrudan ayarlar. Görevi ikiye indirelim: yorum olumsuz mu?

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
is_negative = labels == "negative"
X_train, X_test, y_train, y_test = train_test_split(
    texts, is_negative, test_size=0.25, random_state=0, stratify=is_negative)
vectorizer = TfidfVectorizer().fit(X_train)
model = LogisticRegression(max_iter=1000)
model.fit(vectorizer.transform(X_train), y_train)
proba = model.predict_proba(vectorizer.transform(X_test))[:, 1]
for threshold in [0.2, 0.3, 0.5, 0.7]:
    pred = proba >= threshold
    p = precision_score(y_test, pred)
    r = recall_score(y_test, pred)
    print(threshold, round(p, 3), round(r, 3), int(pred.sum()))
```

```text
0.2 0.723 0.878 119
0.3 0.851 0.816 94
0.5 0.985 0.684 68
0.7 1.0 0.459 45
```

Sütunlar: eşik, kesinlik, duyarlılık, "olumsuz" denen yorum sayısı.

- Varsayılan eşik 0,5: kesinlik 0,985 (neredeyse hiç yanlış alarm yok) ama
  olumsuzların yalnızca %68,4'ü yakalanıyor.
- Eşiği 0,2'ye indirince olumsuzların %87,8'i yakalanıyor, ama "olumsuz"
  denenlerin %27,7'si aslında olumsuz değil.
- Eşik 0,7: yalnızca çok emin olunanlar; kesinlik 1,0, duyarlılık 0,459.

## Eşiği nasıl seçmeli?

Hataların bedeline bak. Olumsuz yorumları bir insana inceletiyorsan ve
birini kaçırmak pahalıysa düşük eşik (yüksek duyarlılık) seç; insanın zamanı
sınırlıysa yüksek eşik (yüksek kesinlik). Eşiği **doğrulama verisinde**
seç, test verisinde değil. ML Kütüphaneleri'ndeki
`TunedThresholdClassifierCV` bunu çapraz doğrulamayla yapar.
