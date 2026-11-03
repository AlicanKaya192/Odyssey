İki özet onaltılık metin olarak verilir. `bit_difference(a_hex, b_hex)`
aynı uzunluktaki iki özetin kaç bitinin farklı olduğunu döndürsün: önce
`bytes.fromhex(...)` ile bayta çevir, XOR'la, sonra 1'leri say. İpucu:
`int.from_bytes(data, "big")` ile tek sayıya çevirip
`bin(...).count("1")`.

**Beklenen çıktı:**

```
0
True
```
