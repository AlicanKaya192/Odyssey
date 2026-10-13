Önyargı vektörlere nereden giriyor? Aynı yöntemle iki külliyat kuralım:
biri dersteki önyargılı meslek cümleleriyle, öteki her meslekte "she"
oranının 0,5 olduğu **dengeli** cümlelerle (`make_jobs(..., skew=...)`).

```python
import numpy as np
from corpus_data import GENDER_PAIRS, JOB_SKEW, make_corpus, make_jobs


def job_projections(skew):
    texts = make_corpus(20000) + make_jobs(4000, skew=skew)
    sentences = [s.split() for s in texts]
    vocab = sorted({w for s in sentences for w in s})
    index = {w: i for i, w in enumerate(vocab)}
    M = np.zeros((len(vocab), len(vocab)))
    for s in sentences:
        for i, w in enumerate(s):
            for j in range(max(0, i - 3), min(len(s), i + 4)):
                if j != i:
                    M[index[w], index[s[j]]] += 1
    with np.errstate(divide="ignore"):
        P = np.maximum(np.log(M * M.sum() / np.outer(M.sum(1), M.sum(0))), 0)
    U, S, _ = np.linalg.svd(P)
    E = U[:, :50] * S[:50]
    E = E / np.linalg.norm(E, axis=1, keepdims=True)
    pairs = GENDER_PAIRS + [("he", "she"), ("his", "her")]
    g = np.mean([E[index[f]] - E[index[m]] for m, f in pairs], axis=0)
    g = g / np.linalg.norm(g)
    return {job: round(float(E[index[job]] @ g), 3) for job in JOB_SKEW}


biased = job_projections(JOB_SKEW)
balanced = job_projections({job: 0.5 for job in JOB_SKEW})
for job in ["nurse", "engineer", "teacher"]:
    print(f"{job:<9} {biased[job]:+.3f} {balanced[job]:+.3f}")
for name, proj in [("biased", biased), ("balanced", balanced)]:
    print(name, round(max(proj.values()) - min(proj.values()), 3))
```

```text
nurse     +0.167 -0.074
engineer  -0.227 -0.068
teacher   -0.046 -0.048
biased 0.398
balanced 0.035
```

- Dengeli veride bütün meslekler cinsiyet yönünde aynı yerde duruyor:
  en büyük ile en küçük izdüşüm arasındaki fark 0,398'den 0,035'e, on
  birinden azına iniyor. Kod aynı, yöntem aynı; değişen yalnızca veri.
- Yani gömme önyargıyı "uydurmuyor", verideki kalıbı ölçüp sıkıştırıyor.
  Gerçek gömmeler haber, web ve kitap metinlerinden öğrenilir; o metinler
  toplumdaki kalıp yargıları taşıdığı için gömmeler de taşır.
- Pratik sonuç: önyargıyı azaltmanın en sağlam yolu veriye bakmaktır
  (kim, hangi bağlamda, ne sıklıkla anılıyor). Vektörü sonradan
  düzeltmek, derste gördüğümüz gibi, ancak yüzeyi düzeltir.
