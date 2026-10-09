`mf_step(r, p, q, lr, reg)` fonksiyonunu yaz (sapmasız): `err = r − p·q`;
`p_yeni = p + lr (err q − reg p)`, `q_yeni = q + lr (err p − reg q)` (ikisi de
**eski** `p` ve `q` ile). `(p_yeni, q_yeni)` listelerini `round(..., 4)`
döndürsün.

**Beklenen çıktı:**

```
[0.2192, 0.1591]
[0.3384, -0.0197]
```
