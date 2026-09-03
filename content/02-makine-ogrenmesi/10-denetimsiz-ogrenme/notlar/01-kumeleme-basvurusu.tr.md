## K-ortalamalar

```python
from sklearn.cluster import KMeans

model = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = model.fit_predict(X_scaled)
```

| Parametre | Ne yapıyor | Varsayılan |
|---|---|---|
| `n_clusters` | Kaç küme aranacak | 8 |
| `n_init` | Kaç farklı başlangıçtan denenecek | `auto` |
| `random_state` | Başlangıç merkezlerinin tohumu | `None` |
| `max_iter` | En fazla kaç tur | 300 |
| `init` | Başlangıç seçimi (`k-means++` akıllı) | `k-means++` |

**`n_init` neden var:** başlangıç merkezleri rastgele; kötü bir başlangıç
kötü bir sonuçta takılıyor. Model `n_init` kez baştan çalışıyor ve
eylemsizliği en düşük olanı tutuyor.

Eğitilmiş modelin verdikleri:

```python
model.labels_           # her kaydin kume numarasi
model.cluster_centers_  # merkezler (OLCEKLI uzayda)
model.inertia_          # merkeze uzakliklarin kareler toplami
model.predict(yeni)     # yeni kayitlari en yakin merkeze atar
```

**`cluster_centers_` ölçekli uzayda.** Orijinal birimlerde okumak için:

```python
print(scaler.inverse_transform(model.cluster_centers_).round(1))
```

## Ölçekleme

Zorunlu — k-ortalamalar uzaklığa dayanıyor.

```python
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)
```

Ölçüldü: ölçekli silüet 0.517, ölçeksiz 0.202. Ölçeksiz model iki gerçek
grubu tek bir 175 kişilik yığına koyuyor.

Burada `fit_transform` bütün veriye uygulanıyor; **bölüm 04'ün sızıntı
kuralı burada geçerli değil**, çünkü tahmin edilecek bir hedef ve
karşılaştırılacak bir test kümesi yok.

## Küme profili okumak

Bölümün asıl çıktısı bu tablo:

```python
df["cluster"] = labels
print(df.groupby("cluster").mean().round(1))
print(df["cluster"].value_counts().sort_index())
```

Küme numaraları anlamsız; anlamlı olan ortalamalar ve boyutlar.

## `k` seçimi

```python
for k in range(2, 9):
    m = KMeans(n_clusters=k, random_state=42, n_init=10).fit(X_scaled)
    print(k, round(float(m.inertia_), 1),
          round(float(silhouette_score(X_scaled, m.labels_)), 3))
```

| Araç | Ne söylüyor | Sınırı |
|---|---|---|
| Eylemsizlik (dirsek) | Eğrinin büküldüğü yer | `k` arttıkça hep düşüyor |
| Silüet | Kümeler ne kadar derli toplu | Gürültüde de pozitif |

Ölçülen: dirsek 3-4 arası, silüet en yüksek `k=3` (0.525), veri gerçekte
dört gruptan üretildi. **İki araç aralığı daraltıyor, kararı vermiyor.**

## Silüet

```python
from sklearn.metrics import silhouette_score
print(round(float(silhouette_score(X_scaled, labels)), 3))
```

−1 ile +1 arası. Kaba bir okuma:

| Değer | Anlamı |
|---|---|
| 0.7 üstü | Çok belirgin kümeler (gerçek veride nadir) |
| 0.5 - 0.7 | Makul yapı |
| 0.25 - 0.5 | Zayıf; dikkatli bakılmalı |
| 0.25 altı | Yapı yok sayılır |

**Referanssız okunmaz:** rastgele gürültüde bile 0.18 çıkıyor. Kendi
verinin gürültü karşılığını ölçüp karşılaştırmak gerekiyor.

## İki kümelemeyi karşılaştırmak

```python
from sklearn.metrics import adjusted_rand_score
print(round(float(adjusted_rand_score(labels_a, labels_b)), 3))
```

Küme numaraları tohuma göre değişiyor; etiketler doğrudan
karşılaştırılamıyor. ARI "aynı iki kayıt aynı kümede mi" sorusuna bakıyor.

| ARI | Anlamı |
|---|---|
| 1.0 | Birebir aynı gruplama |
| 0.6 civarı | Kısmen örtüşüyor |
| 0 civarı | Rastgele kadar benzer |

## PCA

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
Z = pca.fit_transform(X_scaled)

print(pca.explained_variance_ratio_)   # [0.662 0.223]
print(pca.components_)                 # her bilesenin agirliklari
```

| Parametre | Ne yapıyor |
|---|---|
| `n_components` | Kaç bileşen tutulacak |
| `n_components=0.9` | Varyansın %90'ını taşıyacak kadar bileşen |
| `random_state` | Rastgele çözücü kullanılıyorsa tohum |

**PCA'dan önce ölçekleme zorunlu.** Varyansa baktığı için ölçeklenmemiş
veride en büyük birimli sütun bütün bileşenleri ele geçiriyor.

Kaç bileşen tutulacağı:

```python
import numpy as np
print(np.cumsum(pca.explained_variance_ratio_).round(3))
# [0.662 0.885 0.973 1.   ]
```

%85-95 arası yaygın bir eşik.

**Bileşenler orijinal sütun değil, karışım.** `PC1` "genel hareketlilik",
`PC2` "çok geliyor ama az alıyor" çıktı — ama bu yorum ağırlık tablosuna
bakılarak elle yapıldı, PCA böyle bir ad vermiyor.

## Sık yapılan hatalar

- **Ölçeklememek.** Hem k-ortalamalarda hem PCA'da sonucu bozuyor.
- **`n_clusters`'ı hiperparametre sanmak.** Model kaç grup olduğunu
  bilmiyor; sen söylüyorsun.
- **Küme numaralarına anlam yüklemek.** Tohum değişince yer değiştiriyor.
- **Silüeti maksimize etmek.** Gürültüde de artıyor; tek başına ölçüt
  değil.
- **Küme döndürmesini yapı kanıtı saymak.** Algoritma her veriyi bölüyor.
- **Farklı boyutlu uzayların silüetlerini karşılaştırmak.** PCA sonrası
  0.652, tam uzayda 0.517 — kümeler aynı, ölçüm uzayı farklı.
- **Etiket varken kümelemek.** Etiket varsa sınıflandırma her zaman daha
  güçlü.
- **`random_state` vermemek.** Sonuç her çalıştırmada değişiyor.
