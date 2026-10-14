# Düşük Ranklı Uyarlama (LoRA)

Önceki bölümde ince ayarın iki yolunu gördük: bütün ağırlıkları
güncellemek (iyi sonuç, ama her şey değişiyor) ya da yalnızca son katmanı
(ucuz, ama yetersiz). Milyarlarca parametreli bir modelde bütün
ağırlıkları güncellemek hem pahalıdır hem de her görev için modelin tam
bir kopyasını saklamak demektir. **LoRA** (low-rank adaptation, düşük
ranklı uyarlama) arada bir yol: ağırlıkları dondurur ve yanlarına çok
küçük bir **düzeltme** ekler.

## Fikir: değişim düşük ranklıdır

Bir ağırlık matrisi $W$'yi ince ayarla $W + \Delta W$ yapıyoruz. LoRA'nın
gözlemi şu: $\Delta W$ çoğu zaman birkaç yönde yoğunlaşır, yani **düşük
ranklıdır**. O zaman onu iki ince matrisin çarpımı olarak yazabiliriz:

$$\Delta W = A B, \qquad A: d_{\text{giriş}} \times r, \quad B: r \times d_{\text{çıkış}}$$

64 × 32'lik bir katmanda tam $\Delta W$ 2048 sayı; $r = 4$ ile $A$ ve $B$
birlikte $4 \times (64 + 32) = 384$ sayı. Önce gözlemi sınayalım:
12'deki deneyde tam ince ayarın ilk katmanda yaptığı değişimin tekil
değerlerine bakıyoruz. 12'nin veri ve fonksiyonları `finetune_tools.py`
dosyasında.

```python
import numpy as np
from finetune_tools import X_old, y_old, X_new, y_new, init, train, accuracy

pre = train(init([64, 32, 10], np.random.default_rng(0)),
            X_old[:700], y_old[:700], 500)
few = np.concatenate([np.where(y_new[:400] == d)[0][:10]
                      for d in range(5, 10)])
Xf, yf = X_new[few], y_new[few]
full = train(pre, Xf, yf, 300)

delta = full[0][0] - pre[0][0]
S = np.linalg.svd(delta, compute_uv=False)
energy = np.cumsum(S ** 2) / (S ** 2).sum()
for r in [1, 2, 4, 8]:
    print(f"first {r} directions hold {energy[r - 1]:.1%} of the change")
```

```text
first 1 directions hold 32.1% of the change
first 2 directions hold 54.1% of the change
first 4 directions hold 85.2% of the change
first 8 directions hold 99.6% of the change
```

Değişimin 32 olası yönünden ilk 4'ü değişimin %85'ini, ilk 8'i %99,6'sını
taşıyor. Yani 64 × 32'lik değişim, aslında 8 boyutluk bir değişim gibi
davranıyor. LoRA'yı öneren çalışma büyük dil modellerinin ince ayarında
da benzer bir düşük ranklılık gözlemlemişti; buradaki küçük ağ yalnızca
fikri gösteriyor.

## LoRA'yı eğitmek

İlk katmanın ağırlığı $W_1$ donuk kalıyor; ileri hesapta $W_1 + AB$
kullanılıyor. $B$ sıfırdan başlıyor, böylece eğitim başında model ön
eğitimli modelin **tam kendisi**. Eğitilen yalnızca $A$, $B$ ve son
katman. $AB$ çarpımının türevi zincir kuralıyla: $M = W_1 + AB$ için
$\partial L / \partial A = (\partial L / \partial M) B^\top$,
$\partial L / \partial B = A^\top (\partial L / \partial M)$.

```python
def train_lora(pre, X, y, r, steps=300, lr=0.5, seed=0):
    rng = np.random.default_rng(seed)
    (W1, b1), (W2, b2) = pre
    A, B = rng.normal(0, 0.01, (64, r)), np.zeros((r, 32))
    W2, b2 = W2.copy(), b2.copy()
    onehot = np.eye(10)[y]
    for _ in range(steps):
        h = np.tanh(X @ (W1 + A @ B) + b1)
        z = h @ W2 + b2
        e = np.exp(z - z.max(axis=1, keepdims=True))
        grad = (e / e.sum(axis=1, keepdims=True) - onehot) / len(X)
        g_W2, g_b2 = h.T @ grad, grad.sum(axis=0)
        g_M = X.T @ (grad @ W2.T * (1 - h ** 2))
        g_A, g_B = g_M @ B.T, A.T @ g_M
        W2, b2 = W2 - lr * g_W2, b2 - lr * g_b2
        A, B = A - lr * g_A, B - lr * g_B
    return A, B, (W2, b2)


def adapted(pre, A, B, head):
    (W1, b1), _ = pre
    return [(W1 + A @ B, b1), head]


head_only = train(pre, Xf, yf, 300, layers=[1])
results = [("last layer", head_only, 330)]
for r in [1, 2, 4, 8]:
    A, B, head = train_lora(pre, Xf, yf, r)
    results.append((f"LoRA r={r}", adapted(pre, A, B, head),
                    330 + r * (64 + 32)))
results.append(("full", full, 64 * 32 + 32 + 330))
for name, net, params in results:
    print(f"{name:10} accuracy {accuracy(net, X_new[400:], y_new[400:])}",
          f"trained parameters {params}")
```

```text
last layer accuracy 0.802 trained parameters 330
LoRA r=1   accuracy 0.869 trained parameters 426
LoRA r=2   accuracy 0.921 trained parameters 522
LoRA r=4   accuracy 0.94 trained parameters 714
LoRA r=8   accuracy 0.94 trained parameters 1098
full       accuracy 0.931 trained parameters 2410
```

Yalnızca son katman %80'de kalmıştı. Ona $r = 1$'lik bir LoRA eklemek
(96 parametre daha) %87'ye, $r = 2$ %92'ye çıkarıyor; $r = 4$ ile %94, tam
ince ayarın (%93) düzeyinde, ama tam ince ayarın eğittiği 2410
parametrenin yalnızca 714'üyle. $r = 8$ bir şey katmıyor: değişimin
neredeyse tamamı zaten ilk birkaç yöndeydi.

## Bir tohum yetmez

```python
for seed in [0, 1, 2]:
    base = train(init([64, 32, 10], np.random.default_rng(seed)),
                 X_old[:700], y_old[:700], 500)
    A, B, head = train_lora(base, Xf, yf, 4, seed=seed)
    print(seed, "LoRA r=4", accuracy(adapted(base, A, B, head),
                                     X_new[400:], y_new[400:]),
          "full", accuracy(train(base, Xf, yf, 300),
                           X_new[400:], y_new[400:]))
```

```text
0 LoRA r=4 0.94 full 0.931
1 LoRA r=4 0.933 full 0.938
2 LoRA r=4 0.931 full 0.921
```

Üç tohumda LoRA ($r = 4$) %93,1–94, tam ince ayar %92,1–93,8: farklar bir
puanın altında ve yön değiştiriyor. Bu küçük deneyde LoRA tam ince ayarla
aynı düzeyde; daha iyi olduğunu söylemek için daha çok veri gerekir.

## Takılıp çıkarılabilir

LoRA'nın pratikteki en büyük kolaylığı: ön eğitimli model **hiç
değişmiyor**. Her görev için yalnızca küçük bir adaptör ($A$, $B$ ve
gerekiyorsa yeni çıkış katmanı) saklanır; aynı büyük modelin üstüne
istenen adaptör takılır. Çalıştırırken ek maliyet de olmak zorunda değil:
$W_1 + AB$ tek bir matrise **birleştirilebilir**.

```python
A, B, head = train_lora(pre, Xf, yf, 4)
merged = pre[0][0] + A @ B
x = X_new[400:]
two_steps = np.tanh(x @ pre[0][0] + x @ A @ B + pre[0][1])
one_step = np.tanh(x @ merged + pre[0][1])
print("merged gives the same output:", np.allclose(two_steps, one_step))
print("old model untouched, old task:",
      accuracy(pre, X_old[700:], y_old[700:]))
print("adapter size vs full copy:", A.size + B.size, "vs", pre[0][0].size)
```

```text
merged gives the same output: True
old model untouched, old task: 1.0
adapter size vs full copy: 384 vs 2048
```

Birleştirilmiş matris aynı çıktıyı veriyor; ön eğitimli model eski
görevde hâlâ kusursuz, çünkü ona hiç dokunulmadı. Büyük modellerde fark
çok daha çarpıcıdır: milyarlarca parametreli bir model için bir adaptör
yalnızca birkaç milyon parametre tutabilir.

## Özet

- İnce ayarın ağırlıklarda yaptığı değişim çoğu zaman düşük ranklıdır;
  bölümde ilk 8 yön değişimin neredeyse tamamını taşıdı.
- LoRA, donuk $W$'nin yanına iki ince matrisin çarpımını ($AB$) ekler ve
  yalnızca onları eğitir; $B$ sıfırdan başladığı için eğitim ön eğitimli
  modelden başlar.
- Bölümde $r = 4$ LoRA, tam ince ayarın eğittiği parametrelerin üçte
  birinden azıyla aynı düzeyde doğruluk verdi (üç tohumda da; farklar bir
  puanın altında).
- Adaptör takılıp çıkarılabilir ve ana matrise birleştirilebilir; ön
  eğitimli model değişmez.
