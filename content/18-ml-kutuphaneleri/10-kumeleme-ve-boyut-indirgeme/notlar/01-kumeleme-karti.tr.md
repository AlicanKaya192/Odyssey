## Kümeleme

| Sınıf | Küme şekli | Önemli ayar | `predict` |
|---|---|---|---|
| `KMeans(n_clusters, n_init=10)` | yuvarlak, benzer boy | `n_clusters` | var |
| `MiniBatchKMeans(n_clusters)` | aynı, çok büyük veri | `batch_size` | var |
| `GaussianMixture(n_components)` | elips, olasılıklı | `covariance_type` | var |
| `AgglomerativeClustering(n_clusters, linkage)` | bağlantıya göre | `linkage` | yok |
| `DBSCAN(eps, min_samples)` | her şekil, tek yoğunluk | `eps` | yok |
| `HDBSCAN(min_cluster_size)` | her şekil, farklı yoğunluk | `min_cluster_size` | yok |

## Ölçüler

| Fonksiyon | Ne zaman |
|---|---|
| `adjusted_rand_score(y, labels)` | gerçek etiket varsa; numaralara bakmaz |
| `normalized_mutual_info_score(y, labels)` | aynı amaç, başka ölçü |
| `silhouette_score(X, labels)` | etiket yoksa; kümelemenin yapıldığı uzayda |
| `model.inertia_` | KMeans; `k` arttıkça hep düşer |
| `GaussianMixture.bic(X)` | bileşen sayısı; küçük iyi |

## Boyut indirgeme

| Sınıf | Ne | `transform` |
|---|---|---|
| `PCA(n_components=10)` | doğrusal, sabit sayıda bileşen | var |
| `PCA(n_components=0.95)` | varyansın %95'i | var |
| `TruncatedSVD(n_components)` | seyrek matris (metin) | var |
| `TSNE(n_components=2)` | yalnızca çizim | yok |

## Kurallar

- Mesafeye dayalı her yöntemden önce ölçekle (`StandardScaler`).
- Küme numarası keyfidir; karşılaştırmada ARI.
- `-1` etiketi (DBSCAN/HDBSCAN) gürültüdür, küme değildir.
- PCA ve t-SNE'den çıkan eksenlerin birimi yoktur.
