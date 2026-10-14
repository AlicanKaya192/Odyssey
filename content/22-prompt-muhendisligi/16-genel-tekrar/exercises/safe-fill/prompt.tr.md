`fill(template, values)` şablondaki `{ad}` yer tutucularını bulsun
(`\{(\w+)\}`). Eksik olan varsa şablonu doldurmadan `[None, eksikler]`
döndürsün (şablondaki sırayla). Hepsi varsa her yer tutucuyu
`str(değer)` ile değiştirip `[metin, []]` döndürsün.

**Beklenen çıktı:**

```
Hello Ada, order ORD-48213 is shipped.
[None, ['order', 'status']]
```
