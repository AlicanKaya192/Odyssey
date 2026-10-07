`data` klasöründe büyük bir dışa aktarım (`full_export.csv`) ve küçük bir
örnek (`sample.csv`) var. Program yalnızca örneği kullanıyor.

**Yapman gereken:** `.dockerignore`'a iki satır yaz:

1. `data` klasörünü dışarıda bırak.
2. Ama `data/sample.csv` yine de girsin: önceki kuralın **istisnası** `!`
   ile başlıyor.

**Beklenen çıktı:**

```
rows: 3
data files: ['sample.csv']
```
