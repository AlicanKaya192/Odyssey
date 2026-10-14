`build_system(settings)` satırları `"\n"` ile birleştirip döndürsün:
önce `role`, sonra `tone`; `rules` anahtarı varsa ve boş değilse
ardından `Rules:` satırı ve her kural için `1. kural`, `2. kural` gibi
numaralı satırlar. Kural yoksa `Rules:` satırı da yazılmaz.

**Beklenen çıktı:**

```
You help hikers.
Be brief.
Rules:
1. No promises.
2. Be polite.
---
You help hikers.
Be brief.
```
