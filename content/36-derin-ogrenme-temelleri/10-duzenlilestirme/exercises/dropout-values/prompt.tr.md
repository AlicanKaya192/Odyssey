`dropout_values(p)` 1000 tane 1'e Dropout uygulasın: önce eğitim kipinde, sonra
`eval()` kipinde. Her kipte çıkan **farklı** değerleri sıralı liste olarak
döndürsün: `[eğitimdekiler, değerlendirmedekiler]`. Eğitimdekileri 4 basamağa
yuvarla.

**Beklenen çıktı:**

```
[[0.0, 2.0], [1.0]]
[[0.0, 1.25], [1.0]]
```
