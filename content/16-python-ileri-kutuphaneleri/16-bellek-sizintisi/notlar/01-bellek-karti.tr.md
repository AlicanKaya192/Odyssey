## Python belleği nasıl boşaltır?

| Mekanizma | Ne zaman | Neyi siler |
|---|---|---|
| Başvuru sayımı | sayı sıfıra düştüğü **anda** | döngüsüz her nesne |
| Döngüsel çöp toplayıcı (`gc`) | ara sıra, kendiliğinden | dışarıdan ulaşılamayan döngüler |
| Hiçbiri | — | hâlâ ulaşılabilir olan her şey (**sızıntı**) |

## Araçlar

| Yazım | Ne yapar |
|---|---|
| `sys.getrefcount(x)` | başvuru sayısı (+1 çağrının kendisi) |
| `gc.collect()` | döngüleri hemen topla, bulunan sayı döner |
| `gc.get_referrers(x)` | `x`'i kimler tutuyor? |
| `weakref.finalize(x, f, ...)` | `x` silinince `f` çağrılır |
| `weakref.ref(x)` / `WeakMethod` / `WeakSet` / `WeakValueDictionary` | canlı tutmayan başvuru |
| `tracemalloc.start()` | izlemeyi aç |
| `tracemalloc.get_traced_memory()` | `(şu an, tepe)` bayt |
| `snap = tracemalloc.take_snapshot()` | fotoğraf |
| `snap.compare_to(önceki, "lineno")` | satır satır artış |

## Sızıntı kaynakları

| Kaynak | Önlem |
|---|---|
| Sınırsız önbellek / modül düzeyi liste | `lru_cache(maxsize=...)`, süre ya da sayı sınırı |
| Kayıtlı dinleyici, geri çağırma | abonelikten çık; zayıf başvuru |
| Kapanışın yakaladığı büyük nesne | yalnızca gerekeni yakala |
| Saklanan hata (`__traceback__`) | metnini sakla |
| Kapatılmayan dosya, bağlantı | `with` |
| Bitmeyen iş parçacığı | durdurma işareti + `join` |
| Jupyter çıktıları | `del`, `gc.collect()`, çekirdeği yeniden başlat |
