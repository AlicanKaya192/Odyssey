`is_balanced(text)` fonksiyonunu **yığınla** yaz: metindeki `()`, `[]`, `{}`
parantezleri düzgün açılıp kapanıyorsa `True`, değilse `False` döndürsün.
Parantez olmayan karakterler önemsiz.

Üç durumu unutma: kapanan parantez gelince yığın **boş** olabilir, üstteki
parantez **yanlış türde** olabilir, sonunda **açık kalan** parantez
olabilir.

**Beklenen çıktı:**

```
(a[b]{c}) True
(a[b)] False
(( False
)( False
 True
```
