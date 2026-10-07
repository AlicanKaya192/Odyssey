`main.py`, `textkit` adlı bir klasördeki (paketteki) fonksiyonu kullanıyor:
`from textkit.shout import shout`. Bunun çalışması için imajda
`/app/textkit/shout.py` olmalı; klasör korunmalı.

**Yapman gereken:** yorum satırının yerine `textkit` klasörünü **klasör
olarak** `/app/textkit/` içine kopyalayan `COPY` satırını yaz.

`COPY textkit/ .` yazarsan klasörün içindekiler doğrudan `/app`'e dökülür ve
`import` bulamaz.

**Beklenen çıktı:**

```
FOLDERS MATTER!
```
