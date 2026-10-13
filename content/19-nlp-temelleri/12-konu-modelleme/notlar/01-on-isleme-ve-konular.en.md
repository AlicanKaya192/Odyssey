The topics in the lesson were readable because we first removed stop words
and noise specific to the data. Let us run the same NMF with no
preprocessing:

```python
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from text_data import make_tickets

texts = [t["text"] for t in make_tickets(2000)]
for name, vectorizer in [
    ("raw", TfidfVectorizer(min_df=5)),
    ("stop", TfidfVectorizer(min_df=5, stop_words="english")),
]:
    X = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names_out()
    nmf = NMF(n_components=5, random_state=0, max_iter=500).fit(X)
    print(name)
    for row in nmf.components_:
        print(" ", " ".join(words[row.argsort()[::-1][:5]]))
```

```text
raw
  account my to email how
  it ord order got yet
  the app this is page
  box parcel was open damaged
  for ord can of order
stop
  ord order delivered got says
  account address change locked attempts
  app page time history error
  arrived box parcel damaged open
  example com received verification email
```

- In the **raw** form the topics are full of words such as "my", "to", "the",
  "it". TF-IDF pushes these words down a little but does not remove them;
  they are so frequent that they leak into every topic.
- **With the ready-made stop list** the topics become readable, but pieces
  specific to this data, such as "ord" (order numbers), "com" and "example"
  (email addresses), rise to the top of topics. They are in no general list;
  you only notice them by looking at the topics.

In topic modelling preprocessing is not done once and left: look at the
topics, add meaningless words to the stop list, run again. It is a loop. But
careful: dropping words based on the topics can also mean pushing the result
towards the topics you want. Write down what you dropped and why.
