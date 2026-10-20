Bir sunucunun doluluğunu hesaplayan `utilization(rate, service_ms, workers)` fonksiyonunu yaz:

- `rate`: saniyede gelen istek, `service_ms`: bir isteğin süresi (milisaniye), `workers`: çalışan sayısı.
- Doluluk = `rate × service_ms / 1000 / workers`, üç basamağa yuvarlanmış.

**Beklenen çıktı:**

```
0.5
0.6
0.338
```
