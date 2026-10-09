`key_values(text)` fonksiyonunu yaz: `"name=Ada; age=36"` gibi `;` ile
ayrılmış `anahtar=değer` çiftlerini sözlüğe çevirsin. `=` çevresinde boşluk
olabilir; değerin baştaki ve sondaki boşlukları atılsın. Kalıp:
`(\w+)\s*=\s*([^;]+)`, `findall` grupları verir.

**Beklenen çıktı:**

```
name Ada
age 36
city London
{'mode': 'test', 'debug': '1'}
```
