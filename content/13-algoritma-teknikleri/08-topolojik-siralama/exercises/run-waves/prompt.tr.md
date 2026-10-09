`waves(deps)` fonksiyonunu yaz: işleri **dalgalar** hâlinde döndürsün: ilk
dalga hiçbir şeyi beklemeyenler, sonraki dalga yalnızca önceki dalgaları
bekleyenler. Her dalga alfabetik sıralı bir liste.

Kahn'ı tur tur çalıştır: o an bekleyeni sıfır olanların hepsi bir dalga;
sonra onların arkasındakilerin sayaçlarını düşür. `graphlib` yok.

**Beklenen çıktı:**

```
['extract']
['clean', 'validate']
['features']
['train']
['evaluate']
['report']
```
