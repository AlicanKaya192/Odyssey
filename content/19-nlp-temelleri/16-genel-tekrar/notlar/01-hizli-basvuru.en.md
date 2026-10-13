## Preparing text

| Code | What |
|---|---|
| `unicodedata.normalize("NFKC", s)` | unify strings that look the same |
| `html.unescape(s)`, `re.sub(r"<[^>]+>", " ", s)` | HTML leftovers |
| `" ".join(s.split())` | collapse spaces |
| `re.findall(r"[a-z']+", s.lower())` | a simple tokeniser |
| `re.sub(r"\bORD-\d+\b", " ordernum ", s)` | mask variable information |
| `Counter(zip(t, t[1:]))` | count word pairs |

## Vectors

| Code | What |
|---|---|
| `CountVectorizer(ngram_range=(1, 2), min_df=2)` | bag of words |
| `TfidfVectorizer(sublinear_tf=True, stop_words=...)` | TF-IDF |
| `vec.fit_transform(train)`, `vec.transform(new)` | build with training only |
| `vec.get_feature_names_out()` | column names |
| `cosine_similarity(q, X).argmax()` | the most similar document |

## Classification and measuring

| Code | What |
|---|---|
| `MultinomialNB()`, `LogisticRegression()`, `LinearSVC()` | models |
| `Pipeline([("tfidf", ...), ("model", ...)])` | vectoriser + model |
| `cross_val_score(pipe, X, y, cv=5, scoring="f1_macro")` | cross-validation |
| `GridSearchCV(pipe, {"model__C": [1, 10]})` | settings search |
| `classification_report(y, p, digits=3)` | per-class measures |
| `confusion_matrix(y, p, labels=...)` | row true, column predicted |
| `class_weight="balanced"` | weight for small classes |

## Unlabelled text

| Code | What |
|---|---|
| `NMF(n_components=5).fit_transform(X)` | topics (TF-IDF) |
| `LatentDirichletAllocation(n_components=5)` | topics (counts) |
| `KMeans(n_clusters=5, n_init=10)` | clusters |
| <code>len(a &amp; b) / len(a &#124; b)</code> | Jaccard |
| `zlib.crc32(f"{seed}:{x}".encode())` | a stable hash (MinHash) |

## Ten rules

1. Look at the text first: read random examples.
2. Choose cleaning for the task; "not" is not dropped for sentiment.
3. Build the vectoriser with training data only; a Pipeline guarantees it.
4. Baseline first: the most common class, a simple rule.
5. Macro F1 for imbalanced classes.
6. Word pairs catch negation.
7. `best_score_` is optimistic; the final measurement is once, on the test.
8. Choose the number of topics and clusters by readability; topics are not
   categories.
9. Measure a rule on a small gold standard.
10. Read the errors: is the model wrong, the label, or the task itself?
