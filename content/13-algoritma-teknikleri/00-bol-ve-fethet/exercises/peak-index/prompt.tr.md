`peak_index(values)` fonksiyonunu yaz: liste önce **kesin artıyor**, sonra
**kesin azalıyor** (dağ biçimi; yalnızca artan ya da yalnızca azalan da
olabilir). En büyük elemanın **indeksini** `O(log n)`'de bul.

İpucu: `values[mid] < values[mid + 1]` ise yokuş yukarı gidiyorsun, zirve
sağda; değilse zirve `mid` ya da solunda.

Son satır bir milyon elemanlı listede 2000 kez arıyor; doğrusal tarama süre
sınırına takılır. `max` ve `index` yok.

**Beklenen çıktı:**

```
2
2
1199998000
```
