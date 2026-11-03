`run_exchange(p, g, a, b)` iki tarafın anahtar değişimini taklit etsin
ve `[ada_public, can_public, ada_shared, can_shared]` döndürsün. Her taraf
ortak sırrı **karşının** açık değerinden ve **kendi** gizli sayısından
hesaplar. Başlangıç kodunda iki taraf kendi açık değerini kullanıyor ve
ortak sırlar tutmuyor.

**Beklenen çıktı:**

```
[8, 19, 2, 2]
True
```
