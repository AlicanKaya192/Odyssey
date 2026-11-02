`se_check(values, n, reps, seed)` benzetimle iki sayıyı karşılaştırsın:
`np.random.default_rng(seed)` ile `reps` tane `n` kişilik iadeli örneklem
çek; `real` = örneklem ortalamalarının standart sapması, `estimated` = her
örneklemin **kendi** standart hatasının (`std(ddof=1) / sqrt(n)`)
ortalaması. `[real, estimated]` döndür (3 basamak). Başlangıç kodu `ddof`'u
unutuyor ve küçük örneklemde standart hatayı küçük buluyor.

**Beklenen çıktı:**

```text
[3.441, 2.901]
[1.223, 1.225]
```
