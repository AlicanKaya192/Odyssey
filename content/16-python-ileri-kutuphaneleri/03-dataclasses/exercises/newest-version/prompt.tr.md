`Version` dataclass'ını `frozen=True, order=True` ile yaz: alanlar
`major`, `minor`, `patch` (hepsi `int`). `newest(texts)` fonksiyonu
`"1.10.0"` gibi metinlerden `Version` kurup en büyüğünü (`max`) yine
`"1.10.0"` biçiminde metin olarak döndürsün.

**Beklenen çıktı:**

```
1.10.0
0.1.0
```
