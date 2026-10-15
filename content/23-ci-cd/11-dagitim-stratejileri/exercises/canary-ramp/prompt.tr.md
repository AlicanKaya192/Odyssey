Kanarya payı adım adım artırılıyor. `ramp(old, stages, max_increase=0.01, min_requests=500)` fonksiyonunu yaz:

- `old` eski sürümün `[hata, istek]` sayıları.
- `stages` adımların listesi; her adım `[pay, hata, istek]`, payı yüzde olarak (`5`, `25`...).

Adımları sırayla gez:

- İstek `min_requests`'ten azsa: `"waiting at 5%"` gibi döndür.
- Yeni hata oranı, eski oran + `max_increase`'ten büyükse: `"rolled back at 25%"` gibi döndür.
- Bütün adımlar geçtiyse: `"fully promoted"`.

**Beklenen çıktı:**

```
fully promoted
rolled back at 25%
waiting at 5%
```
