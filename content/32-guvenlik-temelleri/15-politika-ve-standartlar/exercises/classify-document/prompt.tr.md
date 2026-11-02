`LEVELS` düzeyleri küçükten büyüğe sıralı tutuyor. `keywords` bir
düzeyden anahtar kelime listesine gidiyor.

`classify_document(text, keywords)` metinde (büyük-küçük harf fark etmez)
anahtar kelimesi geçen **en yüksek** düzeyi döndürsün; hiçbiri geçmiyorsa
`"public"`.

**Beklenen çıktı:**

```
public
internal
restricted
confidential
```
