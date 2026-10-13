Sınav kümesinin etiketleri de insanlardan gelir. Etiketler gürültülüyse
modelin ölçülen doğruluğu ne olur? Gerçek etiketlerden ayrı 3000 yorumla bir
TF-IDF + lojistik regresyon modeli eğitip dersteki 1000 yorumda hem gerçek
etiketlerle hem de birinci etiketleyicinin (%20 dikkatsiz) etiketleriyle
ölçelim:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

training = make_reviews(3000, seed=3)
train_texts = [r["text"] for r in training]
tfidf = TfidfVectorizer().fit(train_texts)
model = LogisticRegression(max_iter=1000)
model.fit(tfidf.transform(train_texts), [r["label"] for r in training])
pred = list(model.predict(tfidf.transform([r["text"] for r in reviews])))


def accuracy(a, b):
    return round(sum(x == y for x, y in zip(a, b)) / len(a), 3)


print(accuracy(pred, gold), accuracy(pred, ann_a))
print(accuracy(gold, ann_a), accuracy(ann_a, ann_b))
```

```text
0.912 0.803
0.878 0.772
```

- Model gerçek etiketlere göre %91,2, gürültülü etiketlere göre %80,3. Model
  aynı, yalnızca cetvel değişti.
- **Kusursuz** bir model bile (gerçek etiketlerin kendisi) gürültülü
  etiketlere göre ancak %87,8 alır: ölçülebilecek en yüksek doğruluk bu.
  İki etiketleyici birbiriyle yalnızca %77,2 anlaşıyor.
- Gerçek hayatta "gerçek etiketler" yoktur; elimizde yalnızca insanların
  etiketleri vardır. Bu yüzden bir model insanların kendi aralarındaki
  uyuşmaya yaklaştığında daha fazla iyileşmeyi ölçmek zorlaşır. Önemli sınav
  kümeleri birden çok kişiyle etiketlenir ve anlaşmazlıklar tartışılarak
  çözülür.
