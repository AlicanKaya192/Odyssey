Her `RUN` imaja bir katman ekliyor. Birbirine bağlı küçük adımları tek bir
`RUN`'da `&&` ile birleştirmek katman sayısını azaltıyor.

**Yapman gereken:** üç `RUN` satırını `&&` ile **tek** bir `RUN`'da birleştir.
Odyssey imajda en fazla 2 katman (Alpine'ın kendi katmanı + seninki)
olduğunu denetleyecek.

**Beklenen çıktı:**

```
alpha
beta
```
