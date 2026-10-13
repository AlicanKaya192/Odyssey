Düz ortalamada her kelime eşit sayılıyor. Arora ve arkadaşlarının (2017)
**SIF** (smooth inverse frequency) yöntemi sık kelimelere daha az ağırlık
verir: kelimenin ağırlığı `a / (a + p(w))`, `p(w)` kelimenin sıklığı, `a`
küçük bir sabit (burada 0,001). Dersteki `E`, `counts`, `vocab` ve arama
düzeniyle deneyelim:

```python
total = sum(counts.values())
weight = {w: 1e-3 / (1e-3 + counts[w] / total) for w in vocab}


def embed_weighted(text):
    words = [w for w in TOKEN.findall(text.lower())
             if w in index and w not in ENGLISH_STOP_WORDS]
    if not words:
        return np.zeros(E.shape[1])
    v = np.sum([weight[w] * E[index[w]] for w in words], axis=0)
    return v / np.linalg.norm(v)


A_w = np.array([embed_weighted(t) for t in article_texts])
Q_w = np.array([embed_weighted(q) for q in queries])
hits = categories[(Q_w @ A_w.T).argmax(axis=1)] == labels
print(round(float(hits.mean()), 3))
print([round(weight[w], 3) for w in ["the", "refund", "pracel"]])
```

```text
0.791
[0.016, 0.165, 0.963]
```

- Ağırlıklı ortalama burada düz ortalamadan (%81,9) **kötü**. Durak
  kelimeleri zaten attığımız için sık kelime sorunu büyük ölçüde çözülmüştü;
  SIF ise nadir kelimeleri, burada çoğunlukla **yazım hatalarını**, öne
  çıkarıyor ("pracel"in ağırlığı "refund"unkinden büyük).
- SIF'in asıl çalışmasında ayrıca bütün cümle vektörlerinin ortak bir
  yönü (ilk tekil vektörü) çıkarılıyor; burada yalnızca ağırlığı denedik.
- Ders yine aynı: bir yöntem bir yerde işe yaradı diye her yerde yaramaz.
  Kendi verinde ölç.
