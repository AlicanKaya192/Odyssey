Gerçek sızıntı tek seferde görünmez; program saatlerce çalıştıkça belli
olur. Uzun çalışan bir servisi izlemenin yolu: bir **başlangıç fotoğrafı**
al, sonra belirli aralıklarla yeni fotoğraf alıp başlangıçla karşılaştır.
Her seferinde aynı satır büyüyorsa sızıntı oradadır.

```python
import tracemalloc

sessions = {}


def serve(request_id):
    sessions[request_id] = {"id": request_id, "data": "x" * 200 + str(request_id)}
    return "ok"


tracemalloc.start()
baseline = tracemalloc.take_snapshot()
growth = []
for batch in range(3):
    for i in range(batch * 2_000, (batch + 1) * 2_000):
        serve(i)
    snapshot = tracemalloc.take_snapshot()
    top = snapshot.compare_to(baseline, "lineno")[0]
    growth.append(top.size_diff // 1024)
print(top.traceback[0].lineno, growth)
```

```text
7 [906, 1816, 2798]
```

## Okuma

- Her 2000 istekten sonra en çok büyüyen satır hep **7. satır**
  (`sessions[...] = ...`) ve büyüme her seferinde yaklaşık 0,9 MB artıyor:
  oturumlar hiç silinmiyor.
- Gerçek bir serviste döngü yerine zamanlayıcı ya da yönetici uç noktası
  (`/debug/memory` gibi) olur; fotoğraf alıp ilk 10 satırı günlüğe yazar.
- `tracemalloc` ayırmaları izlerken programı yavaşlatır ve bellek harcar;
  sürekli açık tutulmaz, sızıntı aranırken açılır.

## Düzeltme seçenekleri

- **Süre sınırı:** oturuma son kullanım zamanı yaz, belirli aralıklarla eski
  oturumları sil.
- **Sayı sınırı:** `OrderedDict` ile en eski oturumu at (LRU), ya da
  `lru_cache(maxsize=...)`.
- **Dışarıda sakla:** oturumları belleğe değil veritabanına ya da önbellek
  sunucusuna yaz.

## Kontrol listesi

1. Bellek gerçekten **sürekli** mi büyüyor, yoksa bir tepeye çıkıp duruyor
   mu? (Önbellek dolup durabilir; o sızıntı değil.)
2. `tracemalloc` ile fotoğrafları karşılaştır; büyüyen satırı bul.
3. O satırda oluşan nesneleri **kim tutuyor**? Modül düzeyi sözlük/liste mi,
   kayıtlı dinleyici mi, saklanan hata mı?
4. Sınır koy ya da zayıf başvuruya geç.
5. Düzelttikten sonra aynı ölçümü yeniden yap.
