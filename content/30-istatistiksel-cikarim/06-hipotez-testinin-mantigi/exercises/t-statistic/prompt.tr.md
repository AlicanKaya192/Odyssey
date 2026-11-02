`t_stat(values, mu0)` tek örneklem t istatistiğini elle hesaplasın:
`(ortalama - mu0) / (s / sqrt(n))`, burada `s` örneklem standart sapması
(`n - 1`'e bölünmüş). 3 basamakla döndür. `ttest_1samp` yasak. Başlangıç
kodu paydada `sqrt(n)` yerine `n` kullanıyor.

**Beklenen çıktı:**

```text
3.667
1.414
```
