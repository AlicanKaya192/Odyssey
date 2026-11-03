Bağlantılar `[src, sport, dst, dport]` listeleri. `replies_ok(outgoing,
incoming)` dışarıdan gelen her paket için, içeriden başlamış bir
bağlantının **tersi** (`[dst, dport, src, sport]`) olup olmadığını
`True`/`False` listesi olarak döndürsün. İpucu: liste bir kümeye
konamaz, `tuple` konabilir.

**Beklenen çıktı:**

```
[True, False, False]
```
