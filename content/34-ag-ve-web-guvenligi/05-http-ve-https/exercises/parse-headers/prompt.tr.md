`parse_headers(text)` satır satır (`\n`) gelen başlıkları bir sözlüğe
çevirsin. Ad ile değer **ilk** `:` işaretinden ayrılır; ad küçük harfe
çevrilir, ikisinin de baştaki ve sondaki boşlukları atılır. İçinde `:`
olmayan satır atlanır.

**Beklenen çıktı:**

```
host = shop.example.com
cookie = session=abc123
x-mode = test
```
