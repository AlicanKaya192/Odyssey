`matches(rule, packet)` hazır. `rule_hits(rules, packets)` her paketi
ilk tutan kurala saysın ve sayaçları bir liste olarak döndürsün: her kural
için bir sayı, **sonda** da hiçbir kurala tutmayan (varsayılana düşen)
paketlerin sayısı. Sıfır kalan kural hiç kullanılmıyor demektir.

**Beklenen çıktı:**

```
[2, 0, 1, 1]
```
