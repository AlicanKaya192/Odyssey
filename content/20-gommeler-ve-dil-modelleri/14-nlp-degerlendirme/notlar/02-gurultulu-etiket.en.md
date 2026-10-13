The labels of a test set come from people too. If the labels are noisy,
what happens to a model's measured accuracy? Let us train a TF-IDF +
logistic regression model on 3000 separate reviews and measure it on the
lesson's 1000 reviews, both against the true labels and against the first
annotator's labels (20% careless):

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

- The model scores 91.2% against the true labels and 80.3% against the noisy
  labels. The model is the same; only the ruler changed.
- Even a **perfect** model (the true labels themselves) scores only 87.8%
  against the noisy labels: this is the highest accuracy that can be
  measured. The two annotators agree with each other only 77.2%.
- In real life there are no "true labels"; we only have people's labels. So
  as a model approaches the agreement between people, measuring further
  improvement gets hard. Important test sets are labelled by several people,
  and disagreements are resolved by discussion.
