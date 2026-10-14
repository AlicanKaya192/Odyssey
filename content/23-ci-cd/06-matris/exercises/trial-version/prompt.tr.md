Henüz çıkmamış Python 3.15'i de dene, ama o iş düşerse hat kırmızı olmasın:

- `include` ile yeni bir birleşim ekle: `python-version` `"3.15"`, `experimental` `true`.
- İşe `continue-on-error: ${{ matrix.experimental == true }}` yaz (`runs-on` ile aynı hizada).
- Bir iş düşünce öbürleri iptal edilmesin: `fail-fast` kapalı.
