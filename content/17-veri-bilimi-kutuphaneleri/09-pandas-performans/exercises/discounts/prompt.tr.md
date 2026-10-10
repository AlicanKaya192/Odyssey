`discounts(qtys)` her adet için indirim oranını döndürsün: 25 ve üstü
`0.2`, 10 ve üstü `0.1`, gerisi `0.0`. `np.select` kullan. Başlangıç kodu da
`np.select` kullanıyor ama 30 adet için `0.1` veriyor: koşulların sırası
yanlış. **Döngü yazma.**

**Beklenen çıktı:**

```
[0.0, 0.1, 0.0, 0.2, 0.2]
```
