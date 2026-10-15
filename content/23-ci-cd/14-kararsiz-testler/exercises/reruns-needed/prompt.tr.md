Bir test her çalıştırmada `rate` olasılıkla düşüyor. `n` çalıştırmada en az bir kez düşmüş görme olasılığı `1 - (1 - rate) ** n`.

`reruns_needed(rate, confidence=0.95)` fonksiyonunu yaz: bu olasılığın `confidence`'a ulaştığı ya da onu geçtiği **en küçük** `n`'i döndürsün. `rate` 0 ya da daha küçükse test hiç düşmez: `None`.

**Beklenen çıktı:**

```
0.5 5
0.1 29
0.02 149
0.1 44
0.0 None
```
