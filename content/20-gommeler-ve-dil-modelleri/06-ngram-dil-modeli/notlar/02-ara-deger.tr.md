Add-k her görülmemiş n-grama aynı küçük olasılığı veriyor. Daha akıllıca bir
yol **ara değer** (interpolation): trigram olasılığını bigram olasılığıyla
karıştırmak. Trigram hiç görülmemişse bigram devreye girer.

`P(c | a, b) = λ · P_tri(c | a, b) + (1 − λ) · P_bi(c | b)`

Dersteki sayımlarla deneyelim (trigram kısmı sayımdan, bigram kısmı
add-0,01):

```python
def p_interp(s, i, lam):
    bigram = p_bigram(s[i - 1], s[i], 0.01)
    if i == 1 or pairs[s[i - 2], s[i - 1]] == 0:
        return (1 - lam) * bigram
    a, b, c = s[i - 2], s[i - 1], s[i]
    return lam * trigrams[a, b, c] / pairs[a, b] + (1 - lam) * bigram


for lam in [0.3, 0.5, 0.7, 0.9]:
    print(lam, perplexity(lambda s, i: p_interp(s, i, lam)))
```

```text
0.3 2.85
0.5 2.6
0.7 2.45
0.9 2.42
```

- λ büyüdükçe şaşkınlık 0,9'a kadar düşüyor; ama derste add-0,001 trigram
  2,15 bulmuştu. Bu küçük ve kalıplı veride basit add-k yeterince iyi.
- Bu basit sürümde trigram bağlamı hiç görülmemişse olasılığın yalnızca
  `(1 − λ)` kadarı kalıyor; bu yüzden toplam olasılık 1 etmiyor. Gerçek
  uygulamalarda λ, bağlamın kaç kez görüldüğüne göre ayarlanır.
- Uzun yıllar en iyi n-gram yöntemi **Kneser-Ney** düzgünleştirmesi oldu:
  bir kelimenin kaç **farklı** bağlamda geçtiğine bakar ("francisco" sık
  geçer ama hep "san"dan sonra; yeni bir bağlamda görülmesi beklenmez).
  Sinir ağı dil modelleri gelene kadar konuşma tanıma ve makine çevirisi bu
  modellerle çalıştı.
