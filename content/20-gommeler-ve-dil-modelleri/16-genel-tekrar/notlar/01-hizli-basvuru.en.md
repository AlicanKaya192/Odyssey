## Embeddings

| Code | What |
|---|---|
| `M[a, b] += 1` within the window | co-occurrence count |
| `np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0)))` | PMI |
| `np.maximum(P, 0)` | PPMI |
| `U, S, _ = np.linalg.svd(P)`; `U[:, :k] * S[:k]` | vectors by truncated SVD |
| `E / np.linalg.norm(E, axis=1, keepdims=True)` | unit vectors; dot product = cosine |
| `E[a] - E[b] + E[c]` | analogy |
| `np.mean(E[ids], axis=0)` | document vector |

## Subwords and language models

| Code | What |
|---|---|
| merge the most frequent adjacent pair | one step of BPE |
| `(count(a, b) + k) / (count(a) + k · V)` | additive smoothing |
| `exp(−mean log p)` | perplexity |
| `λ · p_trigram + (1 − λ) · p_bigram` | interpolation |
| `score[t, j] = max_i(score[t-1, i] + log transition) + log emission` | Viterbi |

## Neural networks

| Code | What |
|---|---|
| `np.exp(z - z.max())` and divide by the row sum | stable softmax |
| `p − y` | the derivative of softmax + cross-entropy |
| `(loss(w + ε) − loss(w − ε)) / 2ε` | gradient check |
| `h = tanh(x Wx + h Wh + b)` | an RNN step |
| `min(1, limit / norm)` | gradient clipping |
| `softmax(Q @ K.T / √d) @ V` | scaled dot-product attention |
| `a · (da − a · da)` | the softmax backward pass |
| `np.tril(np.ones((n, n), dtype=bool))` | causal mask |
| `X + f(norm(X))` | residual connection (norm at the input) |

## Using and measuring

| Code | What |
|---|---|
| pretrained vectors + a small classifier | feature extraction |
| similarity to category descriptions | zero-shot classification |
| `p ** (1 / T)` | temperature |
| the k most likely; the set whose total reaches p | top-k, top-p |
| clipped n-gram precision × brevity penalty | BLEU |
| recall of the reference's n-grams; LCS | ROUGE-N, ROUGE-L |
| `(p_o − p_e) / (1 − p_e)` | Cohen's kappa |
| mean of `1 / first right rank` | MRR |

## Common mistakes

| Mistake | In this module |
|---|---|
| Building vectors from raw counts | Word Vectors with PPMI and SVD |
| Choosing a large learning rate (`nan`) | Word2Vec |
| Ignoring the bias in embeddings | Working with Embeddings |
| An unsmoothed language model | The n-gram Language Model |
| Initialising weights with zeros | Text Classification with a Neural Network |
| Taking attention weights as an explanation | The Attention Mechanism |
| Pretraining from the wrong domain | Pretrained Models |
| Taking BLEU as a measure of meaning | Evaluation in NLP |
| Choosing the threshold on the test set | Capstone: A Semantic Search Engine |
