Başlangıç kodu dersteki VAE'yi eğitiyor (`encode` ve `decode` salt okunur
`vae_model.py`'den), ama kodlayıcıya giden iki türev boş. Yaz:

- `d_mu = d_z + beta * mu / n`
- `d_lv = d_z * eps * 0.5 * std + beta * 0.5 * (std ** 2 - 1) / n`

İlk parça örnekleme adımından gelen türev, ikinci parça KL'nin türevi.
`train(beta, steps)` test resimlerinin hatasını ve KL'yi 3 basamağa
yuvarlanmış iki `float` olarak döndürüyor.

**Beklenen çıktı:**

```
[0.044, 2.012]
[0.047, 59.204]
```
