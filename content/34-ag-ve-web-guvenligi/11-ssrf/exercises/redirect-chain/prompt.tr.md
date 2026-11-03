`chain` bir isteğin izlediği adresler (ilk istek ve yönlendirmeler).
`first_bad(chain, hosts)` her adımı denetlesin: şema `http`/`https` ve ana
bilgisayar `hosts` içinde olmalı. Denetimi geçemeyen **ilk** adresin
sırasını (0'dan) döndürsün; hepsi geçerse `-1`. Başlangıç kodu yalnızca
ilk adrese bakıyor.

**Beklenen çıktı:**

```
2
-1
```
