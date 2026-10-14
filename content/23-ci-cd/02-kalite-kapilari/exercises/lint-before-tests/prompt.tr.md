Bu iş akışı testleri çalıştırıyor ama hiçbir kalite kapısı yok.

Yorumun yerine, testlerden **önce** gelecek üç adım ekle:

- `pip install ruff`
- `ruff check .` (lint)
- `ruff format --check .` (biçim, dosyaları değiştirmeden)

Hızlı kapılar önde olsun: ruff adımları `pip install -r requirements.txt` adımından önce gelmeli.
