`headers` küçük harfli başlık adları sözlüğü, `allowed` izinli kökenler
(`"https://bank.example"`). `origin_ok(headers, allowed)`: `origin`
başlığı varsa izin listesinde mi; yoksa `referer` varsa onun kökeni
(`scheme + "://" + netloc`, `urlsplit` ile) listede mi; ikisi de yoksa
`False`.

**Beklenen çıktı:**

```
True
False
True
False
```
