`fits(buf_size, offset, length)` `buf_size` baytlık bir arabelleğe
`offset` sırasından başlayarak `length` bayt yazmanın **güvenli** olup
olmadığını döndürsün (`True` / `False`). Güvenli olması için üç şart:

- `offset` negatif değil,
- `length` negatif değil,
- `offset + length` arabellek boyunu aşmıyor.

**Beklenen çıktı:**

```
True
False
False
False
```
