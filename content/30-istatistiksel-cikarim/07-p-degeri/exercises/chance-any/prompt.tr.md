`chance_any(k, alpha)` hiç fark yokken `k` bağımsız testten **en az birinin**
`p < alpha` çıkma olasılığını 3 basamakla döndürsün: `1 - (1 - alpha) ** k`.
Başlangıç kodu `k * alpha` yazıyor: 20 testte 1, 30 testte 1,5 gibi
imkânsız olasılıklar veriyor.

**Beklenen çıktı:**

```text
0.05
0.642
```
