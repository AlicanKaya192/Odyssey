Bir bayt 0–255 arası 256 değeri eşit olasılıkla verir. `bias(n)`, 256
baytın her biri için `b % n` hesaplayıp her sonucun kaç kez çıktığını
saysın ve `[en_az, en_cok]` listesi döndürsün (`1 <= n <= 256`).

İkisi eşitse `b % n` eşit dağılıyor demektir; farklıysa modulo yanlılığı
var. Başlangıç kodu `256 // n` ile kalanı yok sayıyor.

**Beklenen çıktı:**

```
100 [2, 3]
16 [16, 16]
6 [42, 43]
```
