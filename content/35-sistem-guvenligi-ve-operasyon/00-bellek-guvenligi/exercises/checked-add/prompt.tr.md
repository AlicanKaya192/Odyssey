`checked_add(a, b, bits)` iki boyutu toplasın ve sonuç `bits` bitlik bir
sayıya sığıyorsa (`2 ** bits`'ten küçükse) sonucu, sığmıyorsa `None`
döndürsün. Başlangıç kodu C gibi davranıp başa sarıyor: bu, küçük bir alan
ayrılmasına yol açar.

**Beklenen çıktı:**

```
255
None
None
300
```
