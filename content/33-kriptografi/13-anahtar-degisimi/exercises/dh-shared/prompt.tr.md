`dh_shared(their_public, my_secret, p)` ortak sırrı hesaplıyor ama
karşıdan geleni hiç denetlemiyor. `1 < their_public < p - 1` değilse
`"invalid"` döndürsün; geçerliyse `pow(their_public, my_secret, p)`. Açık
değer `1` ya da `p - 1` olursa ortak sır yalnızca `1` ya da `p - 1`
olabilir, yani tahmin edilir.

**Beklenen çıktı:**

```
2
invalid
invalid
```
