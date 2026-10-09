## Saatler

| Fonksiyon | Ne verir | Ne için |
|---|---|---|
| `time.time()` | şu anın zaman damgası (saniye) | kayıt, damga |
| `time.perf_counter()` | en hassas monoton saat | süre ölçmek |
| `time.monotonic()` | monoton saat | "N saniye geçti mi?" |
| `time.process_time()` | bu programın işlemci süresi | hesap yükü |
| `time.time_ns()`, `perf_counter_ns()` | aynıları, tam sayı nanosaniye | çok kısa süreler |

**Monoton** saat geri gitmez; `time.time()` gidebilir (saat düzeltilince).

## Bekletmek

| Yazım | Ne yapar |
|---|---|
| `time.sleep(0.5)` | yarım saniye bekletir |
| `time.sleep(base * 2 ** n)` | üstel bekleme (ikinci not) |

## Damga ↔ tarih

| Yazım | Sonuç |
|---|---|
| `dt.timestamp()` | tarih → saniye |
| `datetime.fromtimestamp(s, timezone.utc)` | saniye → UTC tarih |
| `datetime.fromtimestamp(s)` | saniye → **yerel** tarih (bilgisayara göre değişir) |
| `time.gmtime(s)` / `time.localtime(s)` | `time` modülünün tarih yapısı |

## Süre ölçme kalıbı

```python
import time

start = time.perf_counter()
# ölçülecek iş
elapsed = time.perf_counter() - start
print(f"{elapsed * 1000:.1f} ms")
```

- Birkaç kez ölç, **en kısasını** al.
- Ölçtüğün kodun içine `print` koyma; ekrana yazmak da zaman alır.
- İlk çalıştırma çoğu zaman daha yavaştır (dosya, önbellek); onu sayma.
- Daha titiz ölçüm: `timeit` (İleri Python modülü).
