1'den `n`'e kadar sayıların toplamını iki ayrı algoritmayla yaz:

- `sum_loop(n)`: sayıları bir `for` döngüsüyle tek tek toplasın
  (`sum()` kullanma).
- `sum_formula(n)`: döngü kullanmadan `n * (n + 1) // 2` formülüyle bulsun.

`n` 0 ise ikisi de `0` döndürmeli.

Sonra `n` değeri 10, 100 ve 1000 için her satıra `n`'yi ve iki sonucu
yazdır.

**Beklenen çıktı:**

```
10 55 55
100 5050 5050
1000 500500 500500
```

İkisi aynı sonucu veriyor ama döngü `n` toplama yapıyor, formül her zaman
birkaç işlem.
