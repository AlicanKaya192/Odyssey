Bir parolanın hangi karakter türlerini içerdiğine bakıp, saldırganın
denemesi gereken alfabenin büyüklüğünü tahmin edelim:

- küçük harf varsa `26`, büyük harf varsa `26`, rakam varsa `10`,
- bunların dışında herhangi bir karakter (işaret, boşluk) varsa `32`.

`alphabet_size(password)` bulunan türlerin toplamını döndürsün. Her tür bir
kez sayılır. `str.islower()`, `isupper()`, `isdigit()` tek karakterde de
çalışır.

**Beklenen çıktı:**

```
hello 26
Hello 52
Hello1 62
Hello1! 94
1234 10
```
