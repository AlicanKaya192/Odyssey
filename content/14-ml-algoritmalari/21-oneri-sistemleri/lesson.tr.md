# Öneri Sistemleri

Film, müzik ya da ürün öneren bir sistemin elinde bir **derecelendirme
matrisi** vardır: satırlar kullanıcılar, sütunlar ürünler, hücreler puanlar.
Matrisin çoğu **boştur**: kimse her filmi izlemedi. Öneri sisteminin işi boş
hücreleri tahmin etmek ve kişiye en yüksek tahmini, henüz görmediği ürünleri
önermek. Bu bölümde basit taban çizgilerinden başlayıp **işbirlikçi
filtreleme** (collaborative filtering) ve **matris ayrıştırma** (matrix
factorization) yöntemlerini sıfırdan yazıyoruz.

## Derecelendirme matrisi ve taban çizgileri

Veriyi gizli bir yapıyla üretiyoruz: her kullanıcının ve her ürünün 2
boyutlu gizli bir "zevk" vektörü var; puan, ikisinin uyumuna, ürünün genel
beğenilirliğine ve kullanıcının cömertliğine bağlı. 200 kullanıcı, 100 ürün;
her kullanıcı ürünlerin yaklaşık beşte birini puanlamış. Puanların %80'i
eğitim, %20'si test.

```python
import numpy as np

rng = np.random.default_rng(21)
n_users, n_items = 200, 100
U_true = rng.normal(0, 1, (n_users, 2))          # gizli zevkler (2 boyut)
V_true = rng.normal(0, 1, (n_items, 2))
item_bias = rng.normal(0, 0.7, n_items)
user_bias = rng.normal(0, 0.5, n_users)
signal = U_true @ V_true.T * 0.7 + item_bias + user_bias[:, None]
true = np.clip(3 + signal, 1, 5)
seen = rng.random((n_users, n_items)) < 0.2
noisy = np.clip(np.round(true + rng.normal(0, 0.4, true.shape)), 1, 5)
R = np.where(seen, noisy, 0)                     # 0 = puan yok

obs = np.argwhere(R > 0)
rng.shuffle(obs)
cut = int(len(obs) * 0.8)
train, test = obs[:cut], obs[cut:]
Rtr = np.zeros_like(R)
Rtr[train[:, 0], train[:, 1]] = R[train[:, 0], train[:, 1]]
mask = Rtr > 0


def rmse(pred):
    errors = [(R[u, i] - pred(u, i)) ** 2 for u, i in test]
    return round(float(np.sqrt(np.mean(errors))), 3)


mu = Rtr[mask].mean()
item_mean = np.array([Rtr[mask[:, i], i].mean() for i in range(n_items)])
bu, bi = np.zeros(n_users), np.zeros(n_items)
for _ in range(20):                              # kullanıcı ve ürün sapmaları
    bi = ((Rtr - mu - bu[:, None]) * mask).sum(axis=0) / (mask.sum(axis=0) + 5)
    bu = ((Rtr - mu - bi) * mask).sum(axis=1) / (mask.sum(axis=1) + 5)
print(len(obs), round(len(obs) / R.size, 3), len(train), len(test))
print(round(mu, 3), rmse(lambda u, i: mu), rmse(lambda u, i: item_mean[i]))
print(rmse(lambda u, i: mu + bu[u] + bi[i]))
```

```text
3928 0.196 3142 786
3.08 1.156 1.003
0.93
```

20 000 hücrenin yalnızca 3928'i dolu (%19,6). Ölçü **RMSE**: test
puanlarındaki tahmin hatasının karelerinin ortalamasının kökü. Herkese
ortalamayı (3,08) söylemek 1,156 hata veriyor. Ürünün ortalaması 1,003.
Kullanıcı ve ürün **sapmalarını** (bias) birlikte öğrenen taban çizgisi
0,93: kimi kullanıcı herkese yüksek puan veriyor, kimi ürünü herkes seviyor.
Az puanı olan ürün ve kullanıcılarda sapmalar aşırı uymasın diye paydaya
5 eklendi (düzenlileştirme).

## Kullanıcı tabanlı işbirlikçi filtreleme

Fikir: zevki bana benzeyen kullanıcılar bu ürüne ne puan verdi? İki kullanıcının
benzerliği, kendi ortalamalarından **sapmalarının** kosinüs benzerliği.
Tahmin: kendi ortalamam + en benzer `k` komşunun (bu ürünü puanlamış)
sapmalarının benzerlikle ağırlıklı ortalaması.

```python
means = np.array([Rtr[u, mask[u]].mean() for u in range(n_users)])
C = np.where(mask, Rtr - means[:, None], 0)      # ortalamadan sapmalar
norms = np.linalg.norm(C, axis=1)
norms[norms == 0] = 1
S = C @ C.T / np.outer(norms, norms)             # kosinüs benzerliği
np.fill_diagonal(S, 0)


def user_cf(u, i, k):
    raters = np.where(mask[:, i])[0]
    top = raters[np.argsort(-S[u, raters])[:k]]  # en benzer k komşu
    w = S[u, top]
    if np.abs(w).sum() == 0:
        return means[u]
    return np.clip(means[u] + (w * C[top, i]).sum() / np.abs(w).sum(), 1, 5)


for k in (5, 10, 20):
    print(k, rmse(lambda u, i: user_cf(u, i, k)))
```

```text
5 0.816
10 0.803
20 0.817
```

10 komşuyla hata 0,803: sapma taban çizgisinden belirgin iyi. Az komşu
gürültülü, çok komşu benzemeyenleri de katıyor; `k` yine çapraz doğrulamayla
seçilir.

## Matris ayrıştırma

Veriyi üretirken her kullanıcıya ve ürüne gizli bir vektör vermiştik.
**Matris ayrıştırma** bunu tersinden yapar: puan matrisini iki ince matrisin
çarpımı olarak yazar, `R ≈ μ + b_u + b_i + P Qᵀ`. `P`'nin her satırı bir
kullanıcının, `Q`'nun her satırı bir ürünün `k` boyutlu gizli vektörü. Yalnızca
**dolu** hücreler üzerinden, her puanda hatayı küçültecek yönde küçük adımlar
atılır (stokastik gradyan inişi):

```python
def factorize(k, epochs, lr=0.02, reg=0.05, seed=0):
    r = np.random.default_rng(seed)
    P = r.normal(0, 0.1, (n_users, k))
    Q = r.normal(0, 0.1, (n_items, k))
    bu, bi = np.zeros(n_users), np.zeros(n_items)
    for _ in range(epochs):
        for u, i in r.permutation(train):
            err = R[u, i] - (mu + bu[u] + bi[i] + P[u] @ Q[i])
            bu[u] += lr * (err - reg * bu[u])
            bi[i] += lr * (err - reg * bi[i])
            P[u], Q[i] = (P[u] + lr * (err * Q[i] - reg * P[u]),
                          Q[i] + lr * (err * P[u] - reg * Q[i]))
    return lambda u, i: mu + bu[u] + bi[i] + P[u] @ Q[i]


models = {}
for k in (1, 2, 5, 20):
    models[k] = factorize(k, 50)
    fit = np.sqrt(np.mean([(R[u, i] - models[k](u, i)) ** 2 for u, i in train]))
    print(k, round(float(fit), 3), rmse(models[k]))
```

```text
1 0.624 0.762
2 0.454 0.628
5 0.374 0.648
20 0.241 0.666
```

`k = 2` ile test hatası 0,628: bütün yöntemlerin en iyisi. Bu tesadüf değil;
veri 2 boyutlu gizli zevklerle üretilmişti ve ayrıştırma o yapıyı buldu.
`k = 1` yapıyı yakalamaya yetmiyor (0,762). `k` büyüdükçe eğitim hatası
düşmeye devam ediyor (20'de 0,241) ama test hatası yeniden yükseliyor
(0,666): fazla boyut, gürültüyü ezberliyor.

<figure class="fig">
<svg viewBox="0 0 500 210" width="500" xmlns="http://www.w3.org/2000/svg"><text class="ink" x="180" y="36" font-size="12" text-anchor="end">genel ortalama</text><rect class="dot2" x="190" y="24" width="265.9" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="463.9" y="37" font-size="12">1.156</text><text class="ink" x="180" y="70" font-size="12" text-anchor="end">ürün ortalaması</text><rect class="dot2" x="190" y="58" width="230.7" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="428.7" y="71" font-size="12">1.003</text><text class="ink" x="180" y="104" font-size="12" text-anchor="end">sapmalar</text><rect class="dot2" x="190" y="92" width="213.9" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="411.9" y="105" font-size="12">0.93</text><text class="ink" x="180" y="138" font-size="12" text-anchor="end">kullanıcı CF (k=10)</text><rect class="dot2" x="190" y="126" width="184.7" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="382.7" y="139" font-size="12">0.803</text><text class="ink" x="180" y="172" font-size="12" text-anchor="end">matris ayrıştırma (k=2)</text><rect class="dot" x="190" y="160" width="144.4" height="18" rx="3" fill-opacity=".85"/><text class="dim" x="342.4" y="173" font-size="12">0.628</text></svg>
<figcaption>Beş yöntemin test hatası (RMSE, küçük iyi). Her adım bir önceki fikrin üstüne bir şey ekliyor: sapmalar, benzer kullanıcılar, gizli zevkler.</figcaption>
</figure>

## Öneri listesi

Asıl iş puanı tahmin etmek değil, **ne önereceğini** seçmek. Her kullanıcı
için henüz puanlamadığı ürünler arasından en yüksek tahmini 5 ürünü öneriyoruz
ve bunların kaçının gerçekten o kullanıcının en çok seveceği 5 ürün arasında
olduğuna bakıyoruz (gerçek zevkleri biliyoruz, çünkü veriyi biz ürettik):

```python
def precision_at_5(u, scores):
    unseen = np.where(~seen[u])[0]
    best = set(unseen[np.argsort(-true[u, unseen])[:5]])
    picked = unseen[np.argsort(-scores[unseen])[:5]]
    return len(best & set(picked)) / 5


best_model = models[2]
full = np.array([[best_model(u, i) for i in range(n_items)]
                 for u in range(n_users)])
for name, scores in (("mf", lambda u: full[u]), ("popular", lambda u: item_mean),
                     ("random", lambda u: rng.random(n_items))):
    hits = [precision_at_5(u, scores(u)) for u in range(n_users)]
    print(name, round(float(np.mean(hits)), 3))
```

```text
mf 0.593
popular 0.331
random 0.068
```

Matris ayrıştırmanın 5 önerisinin ortalama 3'e yakını kişinin gerçek ilk 5'i
arasında (0,593). Herkese en beğenilen ürünleri önermek 0,331'de, rastgele öneri
0,068'de kalıyor. Kişiselleştirme, popülerliğin yaklaşık 1,8 katı isabet
veriyor.

## Özet

- Öneri sistemi seyrek bir derecelendirme matrisinin boş hücrelerini tahmin
  eder, en yüksekleri önerir.
- Taban çizgileri: genel ortalama, ürün ortalaması, kullanıcı + ürün sapması.
- Kullanıcı tabanlı işbirlikçi filtreleme: benzer kullanıcıların
  sapmalarının ağırlıklı ortalaması.
- Matris ayrıştırma: `R ≈ μ + b_u + b_i + P Qᵀ`, yalnızca dolu hücrelerle
  SGD; `k` ve düzenlileştirme aşırı uyumu belirler.
- Değerlendirme yalnızca RMSE değil; önerilen listenin isabeti (precision@k)
  de ölçülür.
