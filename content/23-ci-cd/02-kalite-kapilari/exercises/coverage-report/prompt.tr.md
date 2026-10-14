Bir kapsam aracının iki sorusu: hangi satırlar hiç çalışmadı ve yüzde kaçı çalıştı?

İki fonksiyon yaz. `ran` çalışan satırların, `body` ölçülen bütün satırların listesi:

- `missed_lines(ran, body)`: `body`'de olup `ran`'da olmayan satırlar, `body`'deki sırayla.
- `coverage_percent(ran, body)`: çalışan satırların yüzdesi, `round` ile tam sayıya yuvarlanmış. `body` boşsa `100`.

Dersteki ölçüm: `ran = [2, 4, 5, 7]`, `body = [2, 3, 4, 5, 6, 7]` → eksik `[3, 6]`, `67`.

**Beklenen çıktı:**

```
[3, 6]
67
100
100
```
