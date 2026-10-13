# Overall Review

You have reached the end of the Embeddings and Language Models module. We
started by learning the meaning of words from the words they appear with,
split words into subword pieces, built models that predict the next word,
and went with neural networks from the RNN to the attention mechanism and on
to the transformer block. Then we measured what pretraining gains,
generated text, evaluated generated text, and built a search engine. This
section walks the road once more; at the end there is a small example where
the pieces work together.

<figure class="fig">
  <div class="flow">
    <span class="node">Embeddings<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Language model<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Neural net<br><small>08–11</small></span><span class="arrow">→</span>
    <span class="node">Using<br><small>12–14</small></span><span class="arrow">→</span>
    <span class="node acc">Project<br><small>15</small></span>
  </div>
  <figcaption>The module's road: give words meaning, model order, learn with neural networks, use and measure pretraining, build a product.</figcaption>
</figure>

## 1. Embeddings (Sections 0–4)

| Task | Tool |
|---|---|
| Distributional meaning | co-occurrence counts, window, cosine similarity |
| From counts to vectors | PPMI, `np.linalg.svd`, truncated SVD, `α = 0.75` smoothing |
| Learning by prediction | Word2Vec (skip-gram + negative sampling), learning rate decay |
| Working with vectors | analogy (`king − man + woman`), neighbours, the bias direction |
| Document vectors | the average of word vectors, SIF, hybrid search |

Embeddings learn **usage**, not meaning: antonyms appear in the same contexts
so they land close, and the bias in the data passes into the vectors.

## 2. Subwords and language models (Sections 5–7)

| Task | Tool |
|---|---|
| Subwords | BPE merges, no out-of-vocabulary words left |
| n-gram language model | conditional probability, perplexity, additive smoothing, interpolation |
| Sequence tagging | HMM, transition and emission probabilities, Viterbi |

An unsmoothed model's perplexity is infinite: a single unseen pair zeroes the
whole text's probability.

## 3. Neural networks (Sections 8–11)

| Task | Tool |
|---|---|
| Classification network | embedding layer, ReLU, softmax, cross-entropy, gradient check |
| RNN | hidden state, backpropagation through time, gradient clipping, LSTM/GRU gates |
| Attention | query, key, value; scaling by `√d`; the softmax derivative |
| Transformer | self-attention, positional encoding, causal mask, multi-head attention, layer normalisation, residual connection |

Attention looks at every word in a single step and is computed in parallel;
its price is the `n × n` score table.

## 4. Using and measuring (Sections 12–14)

| Task | Tool |
|---|---|
| Pretraining | unlabelled text, transfer, a learning curve with few labels, zero-shot |
| Text generation | greedy choice, beam search, temperature, top-k, top-p, distinct-n |
| Evaluation | BLEU, ROUGE, Cohen's kappa |

Pretraining gains the most when labels are few and must come from the right
domain; automatic measures measure the surface, not the meaning.

## 5. The project (Section 15)

The index, the hybrid score, P@1 / MRR / R@3, the "I don't know" threshold
and error analysis.

## All together

A small system that learns vectors from unlabelled tickets, predicts the
category with only **100 labelled** tickets, and suggests an article with the
same vectors:

```python
import re
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from text_data import make_articles, make_tickets

TOKEN = re.compile(r"[a-z]+")
docs = [TOKEN.findall(t["text"].lower()) for t in make_tickets(20000, seed=1)]
counts = Counter(w for d in docs for w in d)
vocab = sorted(w for w in counts if counts[w] >= 3)
index = {w: i for i, w in enumerate(vocab)}
M = np.zeros((len(vocab), len(vocab)))
for d in docs:
    ids = [index[w] for w in d if w in index]
    for i, a in enumerate(ids):
        for b in ids[max(0, i - 4):i] + ids[i + 1:i + 5]:
            M[a, b] += 1
with np.errstate(divide="ignore", invalid="ignore"):
    P = np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))
U, S, _ = np.linalg.svd(np.nan_to_num(np.maximum(P, 0)))
E = U[:, :50] * S[:50]
E = E / np.linalg.norm(E, axis=1, keepdims=True)


def embed(text):
    ids = [index[w] for w in TOKEN.findall(text.lower())
           if w in index and w not in ENGLISH_STOP_WORDS]
    v = E[ids].mean(axis=0) if ids else np.zeros(E.shape[1])
    return v / (np.linalg.norm(v) or 1)


tickets = make_tickets(1100)
X = np.array([embed(t["text"]) for t in tickets])
y = np.array([t["category"] for t in tickets])
model = LogisticRegression(max_iter=1000, C=10).fit(X[:100], y[:100])
print(round(float(np.mean(model.predict(X[100:]) == y[100:])), 3))
articles = make_articles()
A = np.array([embed(a["title"] + " " + a["text"]) for a in articles])
question = embed("My parcel ORD-55120 arrived damaged, can I get a refund?")
best = articles[int((A @ question).argmax())]["title"]
print(model.predict([question])[0], "|", best)
```

```text
0.897
shipping | Lost, late or damaged parcels
```

- **Embeddings:** 50-dimensional vectors with PPMI + SVD from 20,000
  unlabelled tickets (01).
- **Pretraining and transfer:** a classifier with only 100 labels; the
  ticket vector is the average of its word vectors (04, 12).
- **Search:** with the same vectors the question goes to the closest
  article (04, 15).
- 89.7% accuracy on a separate 1000 tickets with 100 labels: the region of
  12's learning curve where pretraining gains the most.

The system classified the question as shipping and suggested the parcel
article. The TF-IDF system in the NLP Fundamentals review said "refund" to
the same question. Both can be counted right: the question is both a damaged
parcel ("arrived damaged") and a refund request ("refund"). A single label
does not fully describe this ticket; that is why real systems often show
several labels or the first three suggestions (15).

## Next

In this module we built everything with NumPy, seeing inside. Real language
models are made of the same parts: a subword tokeniser, an embedding table,
stacked transformer blocks, a next-word loss and a decoding method. The
difference is scale: billions of parameters, trillions of words, and the
hardware that runs them. The notes have a one-page summary of the module and
where to go from here.
