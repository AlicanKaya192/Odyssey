This module gave you the toolbox of classic NLP. From here the road opens in
several directions.

## Next in this path

The **Embeddings and Language Models** module fills the two gaps this module
leaves:

- **Meaning.** In a bag of words "car" and "automobile" are two separate
  columns with nothing in common. Embeddings turn words into vectors by
  looking at the words they appear with; words with similar meanings land
  close together. We will build them from scratch, from PPMI and SVD to
  Word2Vec.
- **Order.** A bag of words forgets order. Language models predict the next
  word: from the n-gram model to HMMs, from RNNs to the attention mechanism
  and the transformer.

The methods of this module are used there too:

| In this module | In the next module |
|---|---|
| Tokeniser (02) | subword splitting with BPE |
| n-gram counts (04) | the n-gram language model, smoothing |
| PMI (04) | the PPMI matrix and word vectors |
| Cosine and search (07) | semantic search with document embeddings |
| BIO labelling (14) | sequence labelling with HMMs and Viterbi |
| Error analysis (15) | evaluating language models |

## Links to other paths

| Path / module | Which part of this module |
|---|---|
| Machine Learning | linear models, measures, cross-validation |
| ML Libraries | `Pipeline`, `GridSearchCV`, leakage |
| ML Algorithms | the inside of Naive Bayes, logistic regression, K-Means |
| Algorithm Techniques | string algorithms, probabilistic data structures (Bloom filter, MinHash) |
| Big Data | counting piece by piece in very large text collections, MapReduce |

## Exploring on your own

- The text feature extraction section of the scikit-learn guide
  (`sklearn.feature_extraction.text`) contains settings not covered here.
- Work with your own data: your emails, your notes, the messages of a forum.
  Go through this module's checklist (the second note of 15) in order.
- Try Turkish text: see with your own eyes why stemming and tokenising are
  hard in an agglutinative language (02, 03).

## A short list of common mistakes

| Mistake | In this module |
|---|---|
| Building the vectoriser on all the data | Bag of Words, Pipelines for Text |
| Dropping "not" as a stop word | Normalisation, Sentiment Analysis |
| Looking only at accuracy on imbalanced data | Linear Models and Evaluation |
| Taking `best_score_` for the real result | Pipelines for Text |
| Taking topics for categories | Topic Modelling |
| Widening a rule without measuring | Information Extraction |
