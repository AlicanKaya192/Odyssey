`layer_norm(rows)` her **satırı** kendi içinde normalleştirsin: satırın
ortalamasını çıkar, `sqrt(varyans + 1e-5)`'e böl (yanlılı varyans). Sonucu 2
basamaklı liste listesi olarak döndür. Çözüm `nn.LayerNorm` ile aynı çıkmalı.

**Beklenen çıktı:**

```
[[-1.22, 0.0, 1.22], [-0.71, -0.71, 1.41]]
```
