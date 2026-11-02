Aynı testte (`n=3000, seed=141`) "B eksi A" farkının %95 Newcomb aralığını
`confint_proportions_2indep(..., method="newcomb")` ile yazdır (iki sınır, 4
basamak). İlk iki bağımsız değişken birinci grup, sonrakiler ikinci grup:
fark "birinci eksi ikinci". Başlangıç kodu A'yı başa koyuyor.

**Beklenen çıktı:**

```text
0.0 0.034
```
