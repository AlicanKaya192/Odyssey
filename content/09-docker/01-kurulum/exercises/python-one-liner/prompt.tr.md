`python -c "kod"` Python'a bir dosya yerine doğrudan kod vermenin yolu:
`python -c "print(1 + 1)"` ekrana `2` yazar.

**Yapman gereken:** `python:3.13-slim` imajında, konteyner çalışınca
`python -c` ile `7 * 6` işleminin sonucunu yazdıran `CMD` satırını yaz.
Köşeli parantezli biçimde komutun üç parçası var: `"python"`, `"-c"` ve
kodun kendisi.

**Beklenen çıktı:**

```
42
```
