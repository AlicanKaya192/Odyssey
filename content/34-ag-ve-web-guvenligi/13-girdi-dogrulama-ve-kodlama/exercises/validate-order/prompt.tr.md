`validate(form)` hatalı alanların adlarını **bu sırayla** bir liste
olarak döndürsün: `zip` tam 5 rakam değilse; `qty` 1–2 rakam değilse ya da
1–99 arasında değilse; `color` `COLORS` içinde değilse. Eksik alan da
hatalıdır. Biçim için `re.fullmatch`.

**Beklenen çıktı:**

```
[]
['zip', 'qty', 'color']
['zip']
```
