Hata analizinde en öğretici örnekler, modelin **en emin olduğu** hatalardır:
ya model bir şeyi kökten yanlış öğrenmiştir ya da etiket şüphelidir.

```python
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from text_data import make_reviews

reviews = make_reviews(2000)
texts = [r["text"] for r in reviews]
labels = np.array([r["label"] for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.25, random_state=0, stratify=labels)
vectorizer = TfidfVectorizer().fit(X_train)
model = LogisticRegression(max_iter=1000)
model.fit(vectorizer.transform(X_train), y_train)
proba = model.predict_proba(vectorizer.transform(X_test))
pred = model.classes_[proba.argmax(axis=1)]
wrong = np.flatnonzero(pred != y_test)
sure = wrong[np.argsort(proba[wrong].max(axis=1))[::-1][:4]]
for i in sure:
    print(y_test[i], "->", pred[i], round(float(proba[i].max()), 2))
    print("  ", X_test[i][:60])
```

```text
negative -> positive 0.94
   The lid is awful. But arrived early and well packed.
neutral -> positive 0.88
   NOTHING SPECIAL ABOUT THE BUTTONS. MY HUSBAND LOVES IT TOO.
negative -> positive 0.87
   the seat is not sturdy at all. but totally worth the money.
neutral -> positive 0.81
   Delivery took 11 days. My friend loves it too.
```

- `wrong` yanlış tahmin edilen test örneklerinin indeksleri;
  `proba[wrong].max(axis=1)` her biri için modelin güveni. En güvenli dört
  hatayı yazdırıyoruz.
- **Karışık yorumlar:** "The lid is awful. But arrived early and well
  packed." Yıldızı düşük (olumsuz), ama metnin yarısı olumlu ve model "But
  arrived early"ye güvendi. İnsan da kararsız kalırdı.
- "the seat is not sturdy at all. but totally worth the money." Olumsuz
  etiketli, ama son cümle güçlü biçimde olumlu.
- Nötr yorumlar olumlu bir cümleyle bitince ("My husband loves it too")
  model olumluya kayıyor.

## Ne öğrendik?

Bu hatalar modelden çok **görevin** sınırını gösteriyor: bir yorumun
yıldızı, metninin bütün tonunu anlatmıyor. Gerçek veride de etiketler
gürültülüdür. Böyle örnekler sık çıkarsa:

- Etiketleri yeniden gözden geçir (etiket gürültüsü),
- görevi yeniden tanımla (cümle düzeyinde duygu, ya da "karışık" sınıfı),
- ya da modelin bu durumlarda emin olmamasını kabul et ve eşikle yönet.
