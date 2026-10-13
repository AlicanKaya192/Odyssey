# Sinir Ağıyla Metin Sınıflandırma

NLP Temelleri'nde yorumları TF-IDF ve doğrusal modellerle sınıflandırdık.
Bu bölümde aynı işi küçük bir **sinir ağıyla** yapacağız: kelimeleri
gömmelere çeviren bir **gömme katmanı** (embedding layer), gömmelerin
ortalaması, bir gizli katman ve olasılık veren bir çıkış. Gömmeleri bu kez
önceden kurmayacağız; ağ onları **görev için** kendisi öğrenecek. Bütün
ileri ve geri hesabı NumPy ile elle yazacağız; ML Algoritmaları modülünün
20. bölümündeki sinir ağının metne uyarlanmış hâli.

## Kelimelerden sayılara

Her kelimeye bir sıra numarası veriyoruz; eğitimde görülmemiş kelimeler 0
(bilinmeyen) oluyor. Bölme NLP Temelleri'ndekiyle aynı.

```python
import re

import numpy as np
from sklearn.model_selection import train_test_split
from text_data import make_reviews

TOKEN = re.compile(r"[a-z']+")
reviews = make_reviews(2000)
classes = ["negative", "neutral", "positive"]
texts = [r["text"] for r in reviews]
y_all = np.array([classes.index(r["label"]) for r in reviews])
X_train, X_test, y_train, y_test = train_test_split(
    texts, y_all, test_size=0.25, random_state=0, stratify=y_all)
vocab = sorted({w for t in X_train for w in TOKEN.findall(t.lower())})
index = {w: i + 1 for i, w in enumerate(vocab)}
V = len(vocab) + 1


def to_ids(text):
    return [index.get(w, 0) for w in TOKEN.findall(text.lower())] or [0]


def averaging(texts):
    A = np.zeros((len(texts), V))
    for row, text in enumerate(texts):
        ids = to_ids(text)
        for i in ids:
            A[row, i] += 1 / len(ids)
    return A


A_train, A_test = averaging(X_train), averaging(X_test)
print(V, A_train.shape, to_ids("The lid is great")[:4])
```

```text
308 (1500, 308) [253, 151, 144, 131]
```

`averaging` her metin için bir satır kuruyor: kelimelerin yerinde `1/uzunluk`.
Bu satırı gömme tablosuyla çarpınca (`A @ E`) metnin kelime gömmelerinin
**ortalaması** çıkıyor. Ortalamayı bir matris çarpımı olarak yazmak, geri
hesapta gömme tablosunun türevini de tek çarpımla almamızı sağlayacak.

## İleri hesap

Ağın katmanları:

1. `x = A @ E`: metnin ortalama gömmesi (16 sayı)
2. `h = ReLU(x @ W1 + b1)`: 32 nöronlu gizli katman
3. `p = softmax(h @ W2 + b2)`: üç sınıfın olasılıkları

```python
rng = np.random.default_rng(0)
params = {"E": rng.normal(0, 0.1, (V, 16)),
          "W1": rng.normal(0, np.sqrt(2 / 16), (16, 32)), "b1": np.zeros(32),
          "W2": rng.normal(0, np.sqrt(1 / 32), (32, 3)), "b2": np.zeros(3)}


def forward(P, A):
    x = A @ P["E"]
    h = np.maximum(x @ P["W1"] + P["b1"], 0)
    z = h @ P["W2"] + P["b2"]
    z = z - z.max(axis=1, keepdims=True)
    p = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
    return x, h, p


def loss(P, A, y):
    p = forward(P, A)[2]
    return float(-np.log(p[np.arange(len(y)), y]).mean())


print(forward(params, A_train[:2])[2].round(3))
print(round(loss(params, A_train, y_train), 3), round(np.log(3), 3))
```

```text
[[0.335 0.326 0.339]
 [0.334 0.336 0.329]]
1.102 1.099
```

Eğitimden önce olasılıklar üçte bire yakın ve kayıp `log 3 ≈ 1,099` civarında:
ağ hiçbir şey bilmiyor. Softmax'tan önce en büyük değeri çıkarmak sayısal
taşmayı önlüyor, sonucu değiştirmiyor.

## Geri hesap ve türev denetimi

Zincir kuralıyla her parametrenin türevini çıkarıyoruz. Elle yazılan türev
kolayca yanlış olur; bu yüzden onu **sayısal türevle** karşılaştırıyoruz:
bir parametreyi `ε` kadar oynatıp kayıptaki değişimi ölçmek.

```python
def backward(P, A, y):
    x, h, p = forward(P, A)
    g = p.copy()
    g[np.arange(len(y)), y] -= 1
    g /= len(y)
    grads = {"W2": h.T @ g, "b2": g.sum(axis=0)}
    gh = g @ P["W2"].T
    gh[h <= 0] = 0
    grads["W1"], grads["b1"] = x.T @ gh, gh.sum(axis=0)
    grads["E"] = A.T @ (gh @ P["W1"].T)
    return grads


A, y = A_train[:50], y_train[:50]
grads = backward(params, A, y)
for name, pos in [("W2", (0, 0)), ("E", (index["great"], 3))]:
    eps = 1e-5
    params[name][pos] += eps
    up = loss(params, A, y)
    params[name][pos] -= 2 * eps
    down = loss(params, A, y)
    params[name][pos] += eps
    numeric = (up - down) / (2 * eps)
    print(name, f"{grads[name][pos]:.6f}", f"{numeric:.6f}")
```

```text
W2 0.003604 0.003604
E 0.000095 0.000095
```

- Elle çıkardığımız türev ile sayısal türev altı basamağa kadar aynı.
  Geri hesap doğru.
- Softmax + çapraz entropinin çıkıştaki türevi çok sade: `p − y` (doğru
  sınıfın olasılığından 1 çıkar).
- Gömme tablosunun türevi `A.T @ ...`: yalnızca metinde geçen kelimelerin
  satırları güncellenecek.

## Eğitim

```python
def predict(P, A):
    return forward(P, A)[2].argmax(axis=1)


rng = np.random.default_rng(1)
for epoch in range(1, 31):
    order = rng.permutation(len(y_train))
    for start in range(0, len(order), 32):
        batch = order[start:start + 32]
        grads = backward(params, A_train[batch], y_train[batch])
        for name in params:
            params[name] -= 0.5 * grads[name]
    if epoch % 10 == 0:
        accuracy = (predict(params, A_test) == y_test).mean()
        print(epoch, round(loss(params, A_train, y_train), 3), round(float(accuracy), 3))
```

```text
10 0.169 0.87
20 0.135 0.878
30 0.113 0.866
```

Test doğruluğu %87 civarına çıkıyor: NLP Temelleri'nde TF-IDF + lojistik
regresyon %88'di. Ağın yaklaşık 5600 parametresi var (`308 × 16 + 16 × 32
+ 32 × 3` ağırlık ve 35 sabit). Eğitim kaybı düşmeye devam ederken test
doğruluğu 20. turdan 30. tura 0,878'den 0,866'ya iniyor: ağ eğitim verisini
ezberlemeye başlamış olabilir (aşırı öğrenme). Eğitimi doğrulama verisine
bakarak durdurmak (erken durdurma) bunu önler.

## Ağ hangi kelimelere dayanıyor?

Gömme katmanının satırlarına tek tek bakmak pek bir şey söylemiyor; anlamı
gizli katmanla birlikte taşıyorlar. Daha açık bir soru soralım: her kelimeyi
**tek başına** ağa verince ağ ne diyor? `olumlu − olumsuz` olasılığı kelimenin
"eğilimi" olsun:

```python
probs = forward(params, averaging(vocab))[2]
lean = probs[:, 2] - probs[:, 0]
order = np.argsort(lean)
print("negative", [vocab[i] for i in order[:6]])
print("positive", [vocab[i] for i in order[::-1][:6]])
for word in ["good", "bad", "great", "not"]:
    print(word, round(float(lean[vocab.index(word)]), 3))
```

```text
negative ['not', 'hate', 'awful', 'terrible', 'i', 'just']
positive ['much', 'totally', 'better', 'well', 'excellent', 'fantastic']
good 1.0
bad 1.0
great -0.971
not -1.0
```

- Olumsuz uçta "not", "hate", "awful", "terrible"; olumlu uçta "excellent",
  "fantastic", "better". Beklenen bu.
- Ama "great" **olumsuz** (−0,97). Veride "Great, the lid broke on day 3"
  gibi alaycı cümleler olumsuz yorumlarda geçiyor; ağ "great"i olumsuz bir
  işaret olarak öğrendi. Olumsuz uçtaki "just" de "Just perfect, the strap
  is weak again" kalıbından.
- "bad" ise tek başına **olumlu** (+1,0): "not bad" olumlu yorumlarda geçiyor
  ve olumsuzluğu "not" kelimesi taşıyor.
- Ağ bir duygu sözlüğü öğrenmedi; **bu verideki işaretleri** öğrendi.
  Etiketli veriden öğrenen her model böyledir (kısayol öğrenme). Modelin
  hangi kelimelere dayandığına bakmak (09'daki `coef_` gibi) bu sürprizleri
  yakalamanın yolu.

## Ortalamanın sınırı

```python
for text in ["good", "not good at all", "bad", "not bad at all"]:
    print(text, classes[predict(params, averaging([text]))[0]])
```

```text
good positive
not good at all negative
bad positive
not bad at all negative
```

Ortalama bir torbadır: "not good" ile "good"un farkı yalnızca "not"
kelimesinin vektörü. "good" olumlu, "not good at all" olumsuz: doğru. Ama
"bad" olumlu, "not bad at all" olumsuz: ikisi de yanlış. Ağ "not"u her yerde
olumsuz işaret sayıyor; "not"un neyi olumsuzladığını bilmiyor, çünkü sırayı
görmüyor. Kelime sırasını işleyebilen bir ağ için bir sonraki bölümde
tekrarlayan sinir ağlarına (RNN) geçeceğiz.

## Özet

- Metin sınıflandıran basit bir sinir ağı: gömme katmanı → ortalama →
  gizli katman → softmax.
- Geri hesap zincir kuralıyla elle yazıldı ve sayısal türevle denetlendi.
- Test doğruluğu %87 civarı, TF-IDF + lojistik regresyona yakın.
- Ağ bu verinin işaretlerini öğrendi: alaycı kalıplar yüzünden "great"
  olumsuz, "not bad" yüzünden "bad" olumlu. Ortalama sırayı görmüyor.
