İki mesaj **aynı** anahtarla şifrelenmiş; anahtarı bilmiyorsun ama
birinci mesajı biliyorsun. `recover_second(c1_hex, c2_hex, first)` ikinci
mesajı metin olarak döndürsün: `c1 ^ c2 = m1 ^ m2`, sonra bunu `first` ile
XOR'la. Uzunluklar farklıysa kısa olan kadarı okunur.

**Beklenen çıktı:**

```
RETREAT AT TEN
```
