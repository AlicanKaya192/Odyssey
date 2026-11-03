`assign_cities(user_cities, seed=0)` her kullanıcının şehrini alıp
şehirlerin yarısını B'ye atasın ve B şehirlerini sıralı liste olarak
döndürsün. Başlangıç kodu kullanıcıları tek tek atıyor: bir şehir iki
gruba bölünüyor. Şehirleri sırala (`sorted(set(...))`), karıştır
(`rng.permutation`) ve ilk yarısını al.

**Beklenen çıktı:**

```text
['W', 'Y']
```
