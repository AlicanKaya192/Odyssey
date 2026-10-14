İki değişiklik:

- Aynı dalda yeni bir çalışma başlayınca süren eski çalışma iptal edilsin. Grup adı iş akışı ve dal: `${{ github.workflow }}-${{ github.ref }}`. Üst düzeyde, `on` ile aynı hizada.
- `test` işi 15 dakikadan uzun sürerse durdurulsun.
