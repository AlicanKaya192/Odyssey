`rules` listesindeki her kural `[anahtar, istenen, oneri]`.
`hardening_findings(config, rules)` yapılandırmada değeri istenene eşit
olmayan her kuralın önerisini, kuralların sırasıyla döndürsün. Anahtar
yapılandırmada **hiç yoksa** da kural tutmamış sayılır (başlangıç kodu
orada `KeyError` veriyor).

**Beklenen çıktı:**

```
turn on the firewall
disable guest
encrypt the disk
```
