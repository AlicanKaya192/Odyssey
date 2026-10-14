`output_problems(reply, canary, allowed)` cevaptaki sorunların listesini
döndürsün: cevapta `canary` geçiyorsa `"leaks the system message"`;
hazır `LINK` kalıbının bulduğu her alan adı `allowed` içinde değilse
`"link to <alan adı>"` (cevaptaki sırayla).

**Beklenen çıktı:**

```
ok
['leaks the system message']
['link to bad.example']
```
