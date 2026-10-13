Do pretrained vectors help everywhere? Let us repeat the experiment, this
time learning the vectors from **product reviews** and using them on support
tickets:

```python
from text_data import make_reviews

reviews = [r["text"] for r in make_reviews(20000, seed=1)]
index, E = pretrain(reviews)
words = [w for t in test_texts for w in TOKEN.findall(t.lower())
         if w not in ENGLISH_STOP_WORDS]
print(len(index), round(sum(w in index for w in words) / len(words), 3))
D = np.array([embed(t) for t in texts])
print(curve_point(20), curve_point(50))
```

```text
425 0.134
(0.623, 0.4) (0.749, 0.517)
```

- The 425 words learned from reviews know only 13.4% of the words in the
  tickets: "refund", "password", "invoice" never appear in reviews.
- Accuracy is 40% with 20 labels and 51.7% with 50 labels. With ticket
  vectors it was 74.8% and 86.6%; this is **behind even TF-IDF** (62.3%,
  74.9%). Pretraining from the wrong domain does not just fail to help, it
  hurts.
- Real pretrained models are trained on very broad text (the web, books,
  code), so they work in most domains; still, in special domains such as
  law, medicine or code, **continuing pretraining** on that domain's text
  (domain-adaptive pretraining) brings a clear gain.
- The lesson: before choosing a pretrained model, check how many of your
  text's words it knows.
