`count_calls(n)` `fib(n)`'yi `cProfile.Profile().runcall` ile profillesin ve
`fib`'in **toplam kaç kez çağrıldığını** döndürsün. `pstats.Stats(profiler).stats`
sözlüğünde anahtar `(dosya, satır, ad)`, değer `(cc, nc, tottime, cumtime,
callers)`; özyinelemeli çağrılar dahil toplam sayı `nc`.

**Beklenen çıktı:**

```
177 1973
```
