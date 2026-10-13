# Transformer Bloğu

2017'de "Attention Is All You Need" makalesi (Vaswani ve arkadaşları) RNN'i
tamamen bıraktı: metni adım adım okumak yerine bütün kelimeler **aynı anda**
birbirine dikkat ediyor. Bu yapıya **transformer** denir ve bugünkü büyük
dil modellerinin hepsi transformer bloklarının üst üste dizilmesinden
oluşur. Bu bölümde bir bloğu parça parça NumPy ile kuracağız: kendi kendine
dikkat, konum bilgisi, nedensel maske, çok başlı dikkat, katman normu ve
artık bağlantılar. Ağırlıklar rastgele; amaç bloğun ne yaptığını ve neden
böyle kurulduğunu görmek.

## Kendi kendine dikkat

10'da tek bir sorgu vardı. **Kendi kendine dikkatte** (self-attention) her
kelime kendi sorgusunu, anahtarını ve değerini üç ayrı ağırlık matrisiyle
üretir: `Q = X Wq`, `K = X Wk`, `V = X Wv`. Sonra her kelime bütün
kelimelere dikkat eder; puanlar bir `n × n` tablo olur.

```python
import numpy as np

rng = np.random.default_rng(0)
words = ["the", "dog", "chased", "the", "cat"]
vocab = sorted(set(words))
d = 16
E = rng.normal(0, 1, (len(vocab), d))
X = E[[vocab.index(w) for w in words]]
Wq, Wk, Wv = (rng.normal(0, d ** -0.5, (d, d)) for _ in range(3))


def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def self_attention(X, mask=None):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    scores = Q @ K.T / np.sqrt(d)
    if mask is not None:
        scores = np.where(mask, scores, -np.inf)
    A = softmax(scores)
    return A @ V, A


out, A = self_attention(X)
print(X.shape, out.shape, A.shape)
print(A.round(2))
```

```text
(5, 16) (5, 16) (5, 5)
[[0.11 0.14 0.14 0.11 0.49]
 [0.05 0.52 0.33 0.05 0.05]
 [0.26 0.11 0.19 0.26 0.18]
 [0.11 0.14 0.14 0.11 0.49]
 [0.44 0.04 0.02 0.44 0.06]]
```

- Her satır bir kelimenin dikkat ağırlıkları, toplamı 1. Çıktı girdiyle
  aynı boyutta: her kelime için 16 sayı, ama artık diğer kelimelerden
  karışım taşıyor.
- Birinci ve dördüncü satır aynı: ikisi de "the". Bu bir sorunun
  habercisi.

## Sıra nerede?

"the dog chased the cat" ile "the cat chased the dog" aynı şey değil.
Kelimelerin yerini değiştirelim:

```python
order = [0, 4, 2, 3, 1]
out2, _ = self_attention(X[order])
print(np.allclose(out2, out[order]))
print(np.allclose(out[0], out[3]))
```

```text
True
True
```

- Sırayı değiştirmek çıktıların yalnızca yerini değiştiriyor; her kelimenin
  çıktısı aynı. Kendi kendine dikkat sırayı **görmüyor**: kelimeleri bir
  küme gibi işliyor. "dog" kovalayan mı kovalanan mı, bilmiyor.
- Aynı kelime her yerde aynı çıktıyı veriyor.

## Konum kodlaması

Çözüm, her konuma özel bir vektörü kelimenin gömmesine **eklemek**.
Transformer makalesi farklı hızlarda dönen sinüs ve kosinüs dalgaları
kullandı: düşük boyutlar hızlı, yüksek boyutlar yavaş değişir.

```python
def positions(n, d):
    pos = np.arange(n)[:, None]
    angle = pos / 10000 ** (np.arange(0, d, 2) / d)
    P = np.zeros((n, d))
    P[:, 0::2], P[:, 1::2] = np.sin(angle), np.cos(angle)
    return P


Pe = positions(5, d)
a, _ = self_attention(X + Pe)
b, _ = self_attention(X[order] + Pe)
print(np.allclose(b, a[order]), np.allclose(a[0], a[3]))
Pl = positions(60, 64)
cos = [Pl[10] @ Pl[10 + k] / 32 for k in [0, 1, 2, 5, 10, 20, 40]]
print([round(float(c), 2) for c in cos])
```

```text
False False
[1.0, 0.97, 0.88, 0.73, 0.66, 0.59, 0.48]
```

- Konum eklenince sıra değişikliği çıktıyı gerçekten değiştiriyor ve iki
  "the" artık farklı.
- Son satır 10. konumun 64 boyutlu vektörünün 0, 1, 2, 5, 10, 20, 40 adım
  ötesindekilerle benzerliği (kosinüs): yakın konumlar daha benzer. Model
  "iki kelime yan yana mı, uzak mı" bilgisini buradan okuyabilir.
- Bugünkü modellerin çoğu konum vektörlerini öğreniyor ya da göreli konum
  yöntemleri kullanıyor; fikir aynı: sırayı dikkate ayrıca vermek gerekir.

## Nedensel maske

Dil modeli sonraki kelimeyi tahmin eder; eğitimde bir kelime kendinden
**sonrakileri** görürse cevabı kopyalar. **Nedensel maske** (causal mask)
her kelimenin yalnızca kendisine ve öncekilere bakmasına izin verir: puan
tablosunun köşegen üstü `-inf` yapılır, softmax orada sıfır verir.

```python
mask = np.tril(np.ones((5, 5), dtype=bool))
_, A = self_attention(X + Pe, mask)
print(A.round(2))
```

```text
[[1.   0.   0.   0.   0.  ]
 [0.17 0.83 0.   0.   0.  ]
 [0.5  0.14 0.37 0.   0.  ]
 [0.22 0.29 0.3  0.19 0.  ]
 [0.66 0.09 0.03 0.21 0.01]]
```

- Tablo alt üçgen: ilk kelime yalnızca kendine bakıyor (ağırlık 1), son
  kelime hepsine.
- Maske sayesinde bir cümlenin bütün konumları için "sonraki kelime"
  tahmini **tek seferde, paralel** hesaplanır; RNN'deki gibi sırayla
  beklemek gerekmez (ikinci not).

## Çok başlı dikkat ve blok

Tek bir dikkat tek bir "soru" sorar. **Çok başlı dikkat** (multi-head
attention) vektörü parçalara ayırır ve her parçada ayrı dikkat çalıştırır:
bir baş özneye, bir başka baş yakındaki kelimeye bakabilir. Sonuçlar
birleştirilip bir matrisle (`Wo`) karıştırılır. Bloğun geri kalanı:

- **Katman normu** (layer normalization): her kelimenin vektörünü ortalaması
  0, standart sapması 1 olacak şekilde ölçekler.
- **İleri beslemeli ağ** (feed-forward): her kelimeye ayrı ayrı uygulanan
  iki katmanlı ağ; genişliği genellikle `4d`.
- **Artık bağlantı** (residual connection): her alt katmanın çıktısı
  girdisine **eklenir** (`X + f(X)`).

```python
heads = 4
Wo = rng.normal(0, d ** -0.5, (d, d))
W1 = rng.normal(0, d ** -0.5, (d, 4 * d))
W2 = rng.normal(0, (4 * d) ** -0.5, (4 * d, d))


def layer_norm(x):
    mu, var = x.mean(axis=-1, keepdims=True), x.var(axis=-1, keepdims=True)
    return (x - mu) / np.sqrt(var + 1e-5)


def multi_head(X, mask):
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    size = d // heads
    outs = []
    for h in range(heads):
        s = slice(h * size, (h + 1) * size)
        scores = Q[:, s] @ K[:, s].T / np.sqrt(size)
        outs.append(softmax(np.where(mask, scores, -np.inf)) @ V[:, s])
    return np.concatenate(outs, axis=1) @ Wo


def block(X, mask):
    X = X + multi_head(layer_norm(X), mask)
    return X + np.maximum(layer_norm(X) @ W1, 0) @ W2


Y = block(X + Pe, mask)
N = layer_norm(Y)
print(Y.shape, np.allclose(N.mean(axis=1), 0), N.std(axis=1).round(3))
```

```text
(5, 16) True [1. 1. 1. 1. 1.]
```

- Blok girdiyle aynı boyutta çıktı veriyor; bu yüzden bloklar üst üste
  istenildiği kadar dizilebilir. Gerçek modellerde 12, 32, 80 blok olur.
- Her baş 4 boyutlu bir parçada çalışıyor: dört başın toplam maliyeti tek
  bir 16 boyutlu dikkatle aynı.
- Normu alt katmanın **girişine** koyan bu düzen (pre-norm) bugün en yaygın
  olanı; ilk makale normu toplamadan sonra uyguluyordu.

## Kaç parametre?

Bir blokta dikkatin dört matrisi (`Wq`, `Wk`, `Wv`, `Wo`: `4d²`), ileri
beslemeli ağın iki matrisi (`2 × 4d²`) ve iki katman normunun ölçek ve
kayma değerleri (`4d`) var. Sapma terimlerini saymıyoruz.

```python
def block_params(d):
    return 4 * d * d + 2 * 4 * d * d + 4 * d


for d_model, layers in [(16, 1), (768, 12), (4096, 32)]:
    print(d_model, layers, f"{layers * block_params(d_model):,}")
```

```text
16 1 3,136
768 12 84,971,520
4096 32 6,442,975,232
```

- Bizim bloğumuz 3136 parametre. 768 boyutlu, 12 bloklu bir model blokları
  için yaklaşık 85 milyon, 4096 boyutlu 32 bloklu bir model 6,4 milyar
  parametre taşır. Sözlüğün gömme tablosu bunlara eklenir.
- Parametre sayısı `d²` ile büyür: boyutu iki katına çıkarmak bloğu dört
  katına çıkarır.

## Özet

- Kendi kendine dikkat: her kelime `Q`, `K`, `V` üretir ve bütün kelimelere
  dikkat eder; `n × n` tablo.
- Dikkat sırayı görmez; konum kodlaması gömmeye eklenerek sıra verilir.
- Nedensel maske kelimenin sonrasını görmesini engeller; böylece bütün
  konumlar paralel eğitilir.
- Blok = çok başlı dikkat + ileri beslemeli ağ, her biri katman normu ve
  artık bağlantıyla. Çıktı girdiyle aynı boyutta, bloklar üst üste dizilir.
- Parametreler `12d²` ile büyür; büyük modeller bu bloğun yüzlerce kez
  büyütülmüş ve üst üste dizilmiş hâli.
