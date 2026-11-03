`hsts_ok(value)` bir `Strict-Transport-Security` başlık değerini
denetlesin: `max-age` yönergesi varsa, değeri yalnızca rakamdan oluşuyorsa
ve **en az bir yıl** (31536000 saniye) ise `True`, değilse `False`.
Yönerge adları büyük/küçük harfe duyarsızdır, aralarında `;` vardır.

**Beklenen çıktı:**

```
True
False
True
False
False
```
