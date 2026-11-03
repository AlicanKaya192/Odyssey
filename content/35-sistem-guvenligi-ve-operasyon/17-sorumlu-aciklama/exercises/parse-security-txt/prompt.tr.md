`parse_security_txt(text)` her `Alan: değer` satırını okuyup alan adı
(küçük harfle) → değerler listesi sözlüğü döndürsün. Boş satırlar, `#` ile
başlayan yorum satırları ve iki nokta içermeyen satırlar atlanır. Değer
yalnızca ilk iki noktadan bölünür.

**Beklenen çıktı:**

```
contact 2
expires 1
```
