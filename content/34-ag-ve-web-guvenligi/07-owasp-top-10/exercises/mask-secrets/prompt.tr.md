`mask(line)` kayda yazılacak bir satırda `password`, `token` ve
`api_key` değerlerini `***` ile değiştirsin; adı korusun
(`password=***`). Değer `&` ya da boşluğa kadar sürer. Başlangıç kodu
yalnızca `password`'ü maskeliyor.

**Beklenen çıktı:**

```
user=ada&password=***
token=*** api_key=*** status=200
nothing secret here
```
