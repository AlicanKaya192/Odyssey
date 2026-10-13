## Metni hazırlamak

| Yazım | Ne |
|---|---|
| `unicodedata.normalize("NFKC", s)` | aynı görünen dizeleri birleştir |
| `html.unescape(s)`, `re.sub(r"<[^>]+>", " ", s)` | HTML artıkları |
| `" ".join(s.split())` | boşlukları teke indir |
| `re.findall(r"[a-z']+", s.lower())` | basit parçalayıcı |
| `re.sub(r"\bORD-\d+\b", " ordernum ", s)` | değişken bilgiyi maskele |
| `Counter(zip(t, t[1:]))` | kelime çiftlerini say |

## Vektörler

| Yazım | Ne |
|---|---|
| `CountVectorizer(ngram_range=(1, 2), min_df=2)` | kelime torbası |
| `TfidfVectorizer(sublinear_tf=True, stop_words=...)` | TF-IDF |
| `vec.fit_transform(eğitim)`, `vec.transform(yeni)` | yalnızca eğitimle kur |
| `vec.get_feature_names_out()` | sütun adları |
| `cosine_similarity(q, X).argmax()` | en benzer belge |

## Sınıflandırma ve ölçü

| Yazım | Ne |
|---|---|
| `MultinomialNB()`, `LogisticRegression()`, `LinearSVC()` | modeller |
| `Pipeline([("tfidf", ...), ("model", ...)])` | vektör + model |
| `cross_val_score(pipe, X, y, cv=5, scoring="f1_macro")` | çapraz doğrulama |
| `GridSearchCV(pipe, {"model__C": [1, 10]})` | ayar arama |
| `classification_report(y, p, digits=3)` | sınıf sınıf ölçü |
| `confusion_matrix(y, p, labels=...)` | satır gerçek, sütun tahmin |
| `class_weight="balanced"` | az örnekli sınıfa ağırlık |

## Etiketsiz metin

| Yazım | Ne |
|---|---|
| `NMF(n_components=5).fit_transform(X)` | konular (TF-IDF) |
| `LatentDirichletAllocation(n_components=5)` | konular (sayımlar) |
| `KMeans(n_clusters=5, n_init=10)` | kümeler |
| <code>len(a &amp; b) / len(a &#124; b)</code> | Jaccard |
| `zlib.crc32(f"{seed}:{x}".encode())` | kararlı özet (MinHash) |

## On kural

1. Önce metne bak: rastgele örnekleri oku.
2. Temizliği göreve göre seç; "not" duygu için atılmaz.
3. Vektörleştiriciyi yalnızca eğitim verisiyle kur; Pipeline bunu garantiler.
4. Önce taban çizgisi: en sık sınıf, basit bir kural.
5. Dengesiz sınıflarda macro F1.
6. Kelime çiftleri olumsuzlamayı yakalar.
7. `best_score_` iyimserdir; son ölçüm testte bir kez.
8. Konu ve küme sayısını okunurluğa göre seç; konular kategori değildir.
9. Kuralı küçük bir altın standartta ölç.
10. Hataları oku: model mi yanlış, etiket mi, görevin kendisi mi?
