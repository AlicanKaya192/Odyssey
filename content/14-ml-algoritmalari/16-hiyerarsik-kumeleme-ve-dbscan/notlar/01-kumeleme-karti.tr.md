## Dört yöntem yan yana

| | K-Means | GMM | Hiyerarşik | DBSCAN |
|---|---|---|---|---|
| Küme tanımı | merkeze yakınlık | olasılık dağılımı | birleştirme ağacı | yoğun bölge |
| `k` gerekir mi? | evet | evet (BIC) | hayır, ağaç kesilir | hayır |
| Şekil | yuvarlak | elips | bağlantıya göre | serbest |
| Gürültü | her nokta bir kümede | her nokta bir kümede | single zincirlenir | `−1` etiketi |
| Büyük veri | hızlı | orta | yavaş (`n²` bellek) | orta |

## Hiyerarşik: bağlantılar

| Bağlantı | İki küme arası uzaklık | Eğilim |
|---|---|---|
| `single` | en yakın iki nokta | uzun, zincir şekiller; gürültüye duyarlı |
| `complete` | en uzak iki nokta | sıkı, eşit çaplı kümeler |
| `average` | bütün çiftlerin ortalaması | ikisinin arası |
| `ward` | küme içi kare toplamındaki artış | K-Means'e benzer, yuvarlak |

SciPy: `linkage(X, yöntem)`, `fcluster(Z, t, criterion="distance")` ağacı
`t` yüksekliğinden keser, `dendrogram(Z)` çizer. scikit-learn:
`AgglomerativeClustering(n_clusters, linkage=...)`.

## DBSCAN

- Çekirdek: `eps` içinde (kendisi dahil) en az `min_samples` nokta.
- Sınır: çekirdeğin komşusu ama kendisi çekirdek değil.
- Gürültü: etiketi `−1`.
- `min_samples` için başlangıç: özellik sayısının iki katı; `eps` k-uzaklık
  grafiğinden.

## Sık hatalar

- Ölçeklememek: `eps` tek bir uzaklık, birimler farklıysa anlamsız.
- DBSCAN'de gürültüyü (`−1`) bir küme sanmak.
- Hiyerarşik kümelemeyi yüz binlerce satıra uygulamak: uzaklık matrisi
  `n²` bellek ister.
- Single bağlantıyı gürültülü veride kullanmak.
