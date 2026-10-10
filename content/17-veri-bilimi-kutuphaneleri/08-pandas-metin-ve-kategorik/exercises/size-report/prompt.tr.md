`size_report(sizes)` bedenleri `S < M < L < XL` sırasıyla **sıralı bir
kategoriye** çevirsin (`pd.CategoricalDtype([...], ordered=True)`). Şunu
döndürsün:

- `"sorted"`: bedenlere göre sıralı liste
- `"large"`: `L` ya da daha büyük olanların sayısı (`int`)
- `"max"`: en büyük beden

**Döngü yazma.**

**Beklenen çıktı:**

```
['S', 'M', 'M', 'L', 'XL']
2 XL
```
