**İşler ve bağımlılıklar**

| İş | Bağlı olduğu | Ne zaman çalışır | Neyi garanti eder |
|---|---|---|---|
| `lint` | – | Her çalışmada | Biçim ve lint temiz |
| `test` (×2) | `lint` | Her çalışmada | İki sürümde testler, kapsam ≥ %90 |
| `build` | `test` | Her çalışmada | Paket derleniyor, `dist` saklandı |
| `ci-ok` | hepsi | Her zaman (`always()`) | Tek zorunlu kontrol |
| `release` | `ci-ok` | Yalnızca `v*` etiketinde | Sürüm tutarlı, sürüm sayfası |

**Hangi olayda ne olur?**

| Olay | lint | test | build | ci-ok | release |
|---|---|---|---|---|---|
| PR açıldı / yeni commit | ✓ | ✓ | ✓ | ✓ | – |
| Birleştirme kuyruğu | ✓ | ✓ | ✓ | ✓ | – |
| `main`'e gönderim | ✓ | ✓ | ✓ | ✓ | – |
| `v0.3.0` etiketi | ✓ | ✓ | ✓ | ✓ | ✓ |

**İzinler**

| Yer | İzin |
|---|---|
| Dosyanın üstü | `contents: read` |
| `release` işi | `contents: write` |
| Hiçbir yerde | `write-all` |

**İptal ve süre**

- `concurrency` grubu iş akışı + ref; iptal yalnızca PR'da.
- `timeout-minutes`: lint 10, test 15.
- `cache: pip` testlerde.

**Depo ayarları**

- `main` kuralı: PR, bir onay, zorunlu kontrol `ci-ok`, zorla gönderim yok.
- İş akışı izinleri varsayılan "yalnızca okuma".
- `v*` etiketlerini yalnızca bakımcılar oluşturur.
