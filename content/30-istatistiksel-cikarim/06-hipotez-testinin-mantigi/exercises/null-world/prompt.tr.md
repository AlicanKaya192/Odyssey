Bu kez sunucu değişikliğinden sonra yalnızca 20 açılış ölçüldü
(`make_speed_test(n=20, seed=81)`). Ortalamanın eski ortalamadan uzaklığını
(`gap`, 1 basamak) yazdır. Sonra p değerini benzetimle bul: eski açılış
sürelerinden (`old`) 10000 tane 20'lik örneklem çek
(`rng.choice(old, size=(10000, 20))`), ortalamalarını al ve `old.mean()`'den
**en az** `gap` kadar uzak olanların payını 3 basamakla yazdır.

**Beklenen çıktı:**

```text
87.4
0.001
```
