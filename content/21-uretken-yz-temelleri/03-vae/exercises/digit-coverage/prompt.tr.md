Başlangıç kodu dersteki VAE'yi (`P`) ve hakemi (`judge`) hazırlıyor.
`coverage(n, seed)` standart normalden `n` tane 2 boyutlu kod çeksin
(`np.random.default_rng(seed).normal(size=(n, 2))`), `decode(z, P)[1]` ile
resimlere çevirsin ve iki değer döndürsün: hakemin tahminine göre en az
`n`'nin %5'i kadar resmi olan rakam sayısı (`int`) ve hakemin %90'dan fazla
emin olduğu resimlerin oranı (3 basamağa yuvarlanmış `float`).

**Beklenen çıktı:**

```
[10, 0.333]
[10, 0.332]
```
