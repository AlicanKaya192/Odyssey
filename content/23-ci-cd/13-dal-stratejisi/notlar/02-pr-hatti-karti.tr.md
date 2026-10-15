**Tetikleyiciler**

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, edited, synchronize, reopened]
  merge_group:
```

| Olay | Ne zaman |
|---|---|
| `pull_request` (varsayılan) | Açılınca, yeni commit gelince, yeniden açılınca |
| `types` içinde `edited` | Başlık ya da açıklama değişince de |
| `merge_group` | PR birleştirme kuyruğunda sınanırken |
| `push` `main` | Birleştirmeden sonra `main`'in kendisi |

**Kapı işi**

```yaml
  ci-ok:
    if: always()
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
        if: >-
          contains(needs.*.result, 'failure')
          || contains(needs.*.result, 'cancelled')
      - run: echo "lint and test passed or were skipped"
```

Zorunlu listede yalnızca `ci-ok`.

| `needs.*.result` değeri | Kapı |
|---|---|
| Hepsi `success` | Geçer |
| Biri `skipped` | Geçer (atlanan iş sorun değil) |
| Biri `failure` | Düşer |
| Biri `cancelled` | Düşer |

**PR başlığı denetimi**

```yaml
  title:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/check_title.py "$TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

- Başlık `env:` ile; `run:` satırına `${{ }}` ile yazılmaz (kod
  enjeksiyonu).
- Squash ile birleştirmede PR başlığı commit mesajı olur.

**`pull_request` ve `pull_request_target`**

| | `pull_request` | `pull_request_target` |
|---|---|---|
| Hangi kod | PR'ın birleştirilmiş hâli | Hedef dalın kodu |
| Fork'tan gizli değerler | Boş | Dolu |
| `GITHUB_TOKEN` | Okuma | Yazma olabilir |
| Test için | Evet | Asla PR'ın kodunu çalıştırma |
