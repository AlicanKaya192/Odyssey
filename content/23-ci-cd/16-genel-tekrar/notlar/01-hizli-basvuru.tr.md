**Dosyanın iskeleti**

```yaml
name: CI

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest -q
```

**Anahtarlar**

| Düzey | Anahtar | Ne yapar |
|---|---|---|
| Üst | `on` | Hangi olaylarda (`push`, `pull_request`, `schedule`, `workflow_dispatch`, `merge_group`) |
| Üst | `permissions` | `GITHUB_TOKEN` yetkisi |
| Üst | `concurrency` | Aynı gruptaki eski çalışmayı iptal |
| İş | `needs` | Sıra; bağlı iş düşerse atlanır |
| İş | `if` | Koşul (`github.ref`, `github.event_name`) |
| İş | `strategy.matrix` | Kopyalar; `fail-fast`, `include`, `exclude` |
| İş | `environment` | Onay, ortam gizli değerleri |
| İş | `services` / `container` | Yanında konteyner / içinde çalışmak |
| İş | `continue-on-error` | Düşse de çalışma kırmızı olmaz |
| Adım | `uses` + `with` | Bir eylem |
| Adım | `run` (<code>&#124;</code> ile çok satır) | Kabuk komutu |
| Adım | `env` | Yalnızca bu adımın ortam değişkenleri |

**İfadeler**

| İfade | Anlamı |
|---|---|
| `${{ secrets.AD }}` | Gizli değer |
| `${{ vars.AD }}` | Gizli olmayan ayar |
| `${{ matrix.python }}` | Matris değeri |
| `${{ needs.build.outputs.version }}` | Başka işin çıktısı |
| `success()` / `failure()` / `always()` | Önceki adım ve işlerin durumu |
| `startsWith(github.ref, 'refs/tags/v')` | Sürüm etiketi mi? |
| `contains(needs.*.result, 'failure')` | Bağlı işlerden biri düştü mü? |

**Sık eylemler**

| Eylem | İş |
|---|---|
| `actions/checkout@v4` | Kodu çek |
| `actions/setup-python@v5` | Python kur (`cache: pip`) |
| `actions/cache@v4` | Klasörü sakla |
| `actions/upload-artifact@v4` / `download-artifact@v4` | Dosyayı işler arasında taşı |
| `docker/build-push-action@v6` | İmaj derle ve gönder |

**On kural**

1. Hızlı kapı önce.
2. Üstte okuma izni, yazma yalnızca gereken işte.
3. Dışarıdan gelen metin `env:` ile.
4. Gizli değer yazdırılmaz.
5. Bir kez derle; test edilen = yayınlanan.
6. Her işin süre sınırı var.
7. Dağıtım iptal edilmez.
8. Tek zorunlu kontrol: kapı işi.
9. Kararsız test düzeltilir, yeniden çalıştırılmaz.
10. Yayınlanan etiket taşınmaz.
