**İşler arasında**

| Yazım | Anlamı |
|---|---|
| (hiçbir şey) | İşler aynı anda, ayrı makinelerde |
| `needs: test` | `test` başarıyla bitince başla |
| `needs: [lint, test]` | İkisi de başarıyla bitince başla |
| `continue-on-error: true` | Bu iş düşse de çalışma başarılı sayılır |

**Durum fonksiyonları** (`if` içinde)

| Fonksiyon | Ne zaman doğru |
|---|---|
| `success()` | Önceki işlerin hepsi başarılı (varsayılan) |
| `failure()` | Önceki işlerden biri düştü (zincirde geride olanlar dahil) |
| `always()` | Her zaman |
| `cancelled()` | Çalışma iptal edildi |

**Bağlam değerleri**

| Değer | Örnek |
|---|---|
| `github.event_name` | `push`, `pull_request`, `schedule` |
| `github.ref` | `refs/heads/main`, `refs/tags/v1.2.0` |
| `github.ref_name` | `main`, `v1.2.0` |
| `github.sha` | Commit'in kimliği |
| `github.actor` | Çalışmayı başlatan kullanıcı |
| `needs.<iş>.result` | `success`, `failure`, `skipped` |
| `needs.<iş>.outputs.<ad>` | İşin dışarı açtığı değer |

**Koşul yazımı**

- Metin tek tırnakla: `github.ref == 'refs/heads/main'`
- `&&` ve, `||` veya, `!` değil
- `if` içinde `${{ }}` gerekmez
- Durum fonksiyonu yoksa başa `success() &&` eklenir

**Değer aktarmak**

```yaml
  version:
    runs-on: ubuntu-latest
    outputs:
      number: ${{ steps.read.outputs.number }}
    steps:
      - id: read
        run: echo "number=1.4.2" >> "$GITHUB_OUTPUT"
  build:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ needs.version.outputs.number }}"
```
