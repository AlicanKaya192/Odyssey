**Olaylar**

| Olay | Ne zaman |
|---|---|
| `push` | Bir dala ya da etikete commit gönderilince |
| `pull_request` | PR açılınca, yeni commit eklenince, yeniden açılınca |
| `schedule` | cron ifadesindeki zamanda (UTC) |
| `workflow_dispatch` | Actions sekmesindeki Run workflow düğmesiyle |

**Süzgeçler** (`push` ve `pull_request` altında)

| Süzgeç | Anlamı |
|---|---|
| `branches` | Yalnızca bu dallarda (PR'da: hedef dal) |
| `branches-ignore` | Bu dallar dışında; `branches` ile birlikte yazılmaz |
| `tags` | Bu etiketler gönderilince (`push`) |
| `paths` | Bu dosyalardan biri değiştiyse |
| `paths-ignore` | Değişenlerin hepsi bunlardansa çalışmaz |

Dal ve yol süzgeci birlikteyse **iki şart da** tutmalı.

**Kalıplar**

| Kalıp | Uyar | Uymaz |
|---|---|---|
| `release/*` | `release/1.0` | `release/2026/oct` |
| `release/**` | `release/2026/oct` | `hotfix/1` |
| `*.md` | `README.md` | `docs/guide.md` |
| `**.md` | `docs/guide.md` | `docs/logo.png` |
| `docs/**` | `docs/img/logo.png` | `src/docs.py` |

`*` eğik çizgiye uymaz, `**` uyar.

**Sık kullanılan düzen**

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

**Tuzaklar**

- Süzgeçsiz `on: [push, pull_request]`: açık PR'ın dalına gönderim iki
  çalışma başlatır.
- Yalnızca `tags` yazılırsa dal gönderimleri başlatmaz; yalnızca
  `branches` yazılırsa etiket gönderimleri başlatmaz.
- `schedule` ve `workflow_dispatch` yalnızca varsayılan daldaki dosyadan
  okunur.
- Commit mesajında `[skip ci]`: o gönderimin çalışmaları atlanır.
