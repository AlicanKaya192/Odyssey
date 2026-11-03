`keystream(key_hex, nonce_hex, length)` anahtar ve nonce'tan `length`
baytlık bir anahtar dizisi üretsin: `counter` 0'dan başlar, her blok
`sha256(key + nonce + counter.to_bytes(4, "big")).digest()`, bloklar
`length` baytı geçene kadar eklenir ve sonuç `length` bayta kırpılır.

**Beklenen çıktı:**

```
3addfb141c
10
40
0b4ce3c3
```
