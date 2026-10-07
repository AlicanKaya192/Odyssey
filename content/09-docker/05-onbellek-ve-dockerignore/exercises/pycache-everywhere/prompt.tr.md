`shapes` klasörünün içinde bir `__pycache__` var: bilgisayarındaki eski
önbellek, imaja girmemeli.

**Yapman gereken:** `.dockerignore`'a **her klasördeki** `__pycache__`'yi
dışarıda bırakan tek bir kalıp yaz. Yalnızca `__pycache__` yazarsan bu
kalıp yalnızca kökteki klasörü tutar; `shapes/__pycache__` imaja girer.

**Beklenen çıktı:**

```
area: 49
```
