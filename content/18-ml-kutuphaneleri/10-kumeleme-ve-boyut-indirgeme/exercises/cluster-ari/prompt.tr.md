`cluster_ari(k)` ölçeklenmiş veride `KMeans(n_clusters=k, n_init=10,
random_state=0)` ile kümeliyor. Kümelemeyi gerçek etiketlerle (`y`)
karşılaştıran **ARI**'yi 3 basamakla döndürsün. Başlangıç kodu doğruluk
hesaplıyor; küme numaraları keyfi olduğu için doğruluk anlamsız.

**Beklenen çıktı:**

```
0.923
0.57
```
