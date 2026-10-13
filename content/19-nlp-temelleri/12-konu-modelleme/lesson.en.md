# Topic Modelling

You have thousands of unlabelled support tickets and you ask "what do people
write about most?". **Topic modelling** finds groups of words that appear
together in documents: each group is a **topic**, and each document is a
mixture of these topics. No labels are needed; it is an unsupervised method.
In this section we try two common methods, NMF and LDA, on the tickets. We
know the tickets' real categories but will not give them to the model; only
at the end will we check how well the topics found match the categories.

## Topics with NMF

**NMF** (non-negative matrix factorization) splits the document-word matrix
into the product of two small matrices: document-topic (`W`) and topic-word
(`H`). Neither has negative values, so a document can be read as a **sum** of
topics.

```python
import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from text_data import make_tickets

tickets = make_tickets(2000)
texts = [t["text"] for t in tickets]
categories = np.array([t["category"] for t in tickets])
EXTRA_STOP = {"ord", "com", "example", "hi", "hello", "thanks", "thank",
              "dear", "support", "regards", "help"}
tfidf = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS | EXTRA_STOP),
                        token_pattern=r"[a-z]{2,}", min_df=5)
X = tfidf.fit_transform(texts)
words = tfidf.get_feature_names_out()


def show_topics(components, k=6):
    for i, row in enumerate(components):
        print(i, " ".join(words[row.argsort()[::-1][:k]]))


nmf = NMF(n_components=5, random_state=0, max_iter=500)
W = nmf.fit_transform(X)
print(X.shape, W.shape, nmf.components_.shape)
show_topics(nmf.components_)
```

```text
(2000, 142) (2000, 5) (5, 142)
0 does number card order work long
1 account email address change access locked
2 app page error time crashes screen
3 arrived box parcel damaged open order
4 delivered got says order address wrong
```

- Preprocessing is critical in topic modelling. Besides the English stop
  words we added ones specific to this data: "ord" (order numbers
  `ORD-12345`), "com" and "example" (email addresses), greetings.
  `token_pattern` takes only letters, so numbers are left out. The first note
  shows what happens without stop words.
- `W` is 2000 × 5: the weight of each ticket in each topic. `H`
  (`components_`) is 5 × 142: the weight of each topic on each word. **You**
  name a topic by looking at its heaviest words; the model gives no names.
- The topics read well: 1 account, 2 app errors, 3 damaged parcels, 4 wrong
  delivery. 0 is mixed: "number card order work long".

## Do the topics match the categories?

Let us give each ticket its heaviest topic and cross-tabulate with the real
categories. **Purity**: the share of tickets that land right when each
topic's largest category is counted as correct.

```python
topic = W.argmax(axis=1)


def purity(topic):
    table = pd.crosstab(pd.Series(topic, name="topic"),
                        pd.Series(categories, name="category"))
    print(table)
    return round(table.max(axis=1).sum() / len(categories), 3)


print(purity(topic))
```

```text
category  account  billing  refund  shipping  technical
topic                                                  
0              16       53     113       143         40
1             376      150      22        14         11
2              13       43      18         9        438
3               3        2      23       165          0
4               2       70       8       262          6
0.692
```

- The account (1) and app (2) topics match their categories well.
- Shipping was split into two topics: damaged parcels (3) and wrong
  delivery (4).
- **Billing and refund did not find their own topics.** Both use the same
  words ("card", "charged", "money", "order"); billing tickets scattered into
  the account topic (150) and refund tickets into the mixed topic (113).
- The lesson: a topic model does not find **your categories**; it finds
  **words that appear together**. Categories are a business decision (a
  billing team, a refunds team); words do not know that.

## The number of topics

You choose the number of topics. Let us try 8:

```python
nmf8 = NMF(n_components=8, random_state=0, max_iter=500)
W8 = nmf8.fit_transform(X)
show_topics(nmf8.components_)
print(purity(W8.argmax(axis=1)))
```

```text
0 change address delivery order email account
1 account access locked attempts data delete
2 app page error time crashes order
3 arrived box parcel damaged open order
4 delivered got says order wrong package
5 card paid credit refund charged did
6 update working push notifications stopped phone
7 does number work tracking long shipping
category  account  billing  refund  shipping  technical
topic                                                  
0              16        1       3        54          1
1             334      101      13         6         14
2               9       28       3         2        253
3               3        2       6       164          0
4               2       17       3       171          6
5              32      144     150        28         27
6               5       22       1         3        152
7               9        3       5       165         42
0.722
```

- More topics, finer splits: shipping split into four topics (address
  change, damage, wrong delivery, tracking number) and app errors into two
  (crashes, notifications).
- Billing and refund merged again into **a single money topic** (5): 144
  billing, 150 refund. More topics did not separate them.
- Purity rose a little, but purity rises with the number of topics anyway:
  give each document its own topic and purity is 1. Do not choose the number
  of topics by purity; check whether the topics are readable and useful.

## LDA

**LDA** (latent Dirichlet allocation) is a probabilistic model: it assumes
each document has a topic distribution and each topic a word distribution,
and sets up a process that writes the document. It needs raw **counts**, not
TF-IDF.

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

counter = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS | EXTRA_STOP),
                          token_pattern=r"[a-z]{2,}", min_df=5)
C = counter.fit_transform(texts)
words = counter.get_feature_names_out()
lda = LatentDirichletAllocation(n_components=5, random_state=0)
D = lda.fit_transform(C)
show_topics(lda.components_)
print(purity(D.argmax(axis=1)))
print(D[1].round(2).tolist(), categories[1])
```

```text
0 account log error login shows screen
1 address account change email order number
2 arrived long does shipping damaged box
3 app time order happens second page
4 order card paid refund credit got
category  account  billing  refund  shipping  technical
topic                                                  
0             155       91      14        11        174
1             178       47       5       210         80
2               5        1      18       230          2
3              54       11       8        16        221
4              18      168     139       126         18
0.501
[0.34, 0.02, 0.02, 0.59, 0.02] account
```

- LDA's topics are blurrier on this data and purity is lower (0.501 against
  0.692). LDA estimates probabilities from word counts; in short texts (one-
  or two-sentence tickets) there are few counts and the estimate weakens. NMF
  often gives more readable topics on short texts.
- Each row of `D` is a distribution summing to 1: how much of each topic a
  ticket is made of. This is LDA's real strength: being able to say "this
  document is 60% economy, 40% politics" for long documents (articles,
  books).
- The last line shows the problem with short text: only 34% of the ticket
  "I cannot log in to my acconut... reset the password" is in the account
  topic (0), 59% is in topic 3. "account" is misspelled and a few words
  decide the whole distribution.

## A new document

A trained topic model gives topic weights to a new document:

```python
new = ["My parcel arrived damaged and the box was open.",
       "I was charged twice, please refund the extra money."]
for weights in nmf.transform(tfidf.transform(new)):
    print(weights.round(2).tolist())
```

```text
[0.0, 0.0, 0.0, 0.36, 0.0]
[0.03, 0.03, 0.0, 0.0, 0.0]
```

The first ticket is almost only in the damage topic (3). The second one's
weight is spread out and small: "charged", "refund", "money" fit none of the
five topics well, because the model never found a separate money topic. A
topic model cannot make a distinction in a new document that it did not see.

## Summary

- Topic modelling finds groups of words that appear together in unlabelled
  documents. You name the topics by looking at their heaviest words.
- NMF splits the TF-IDF matrix into document-topic and topic-word matrices;
  on short texts it is often more readable than LDA.
- LDA is a probabilistic model working on raw counts; it gives each document
  a topic distribution and is strong on long documents.
- Topics are not your categories: billing and refund, which use the same
  words, did not separate. Choose the number of topics by readability and
  usefulness.
- Preprocessing (stop words, numbers) decides the quality of the topics.
