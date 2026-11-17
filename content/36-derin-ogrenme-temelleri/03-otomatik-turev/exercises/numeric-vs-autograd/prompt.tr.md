`compare(value)` `f(t) = 3t² + t` için iki türevi döndürsün:
otomatik türev (`float64` tensörle) ve `h = 1e-4` ile sayısal türev
`(f(x + h) − f(x − h)) / 2h`. İkisini de 4 basamakla, `[otomatik, sayısal]`.

**Beklenen çıktı:**

```
[10.0, 10.0]
[-11.0, -11.0]
```
