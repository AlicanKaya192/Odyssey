PR başlıklarını denetleyen bir `title` işi ekle:

- Yalnızca PR'da çalışsın: `if: github.event_name == 'pull_request'`. Makine `ubuntu-latest`.
- Kodu çeksin, sonra `python scripts/check_title.py "$TITLE"` çalıştırsın; `TITLE` ortam değişkeni `${{ github.event.pull_request.title }}`.
- Başlık düzeltilince de çalışsın: `pull_request` altına `types: [opened, edited, synchronize, reopened]`.

Başlık `run:` satırına doğrudan yazılmasın.
