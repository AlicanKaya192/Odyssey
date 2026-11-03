Kurallar `[port, action]` listeleri; `port` bir sayı ya da `"any"`.
Bir kuralın üstünde portu `"any"` olan ya da **aynı** portu taşıyan bir
kural varsa o kural hiç çalışmaz. `shadowed(rules)` bu kuralların
numaralarını (1'den başlayarak) bir liste olarak döndürsün.

**Beklenen çıktı:**

```
[2]
[]
[2, 4]
```
