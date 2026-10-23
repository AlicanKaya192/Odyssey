Dosyaların çoğunun adı noktayla başlayan bir **uzantıyla** biter: GIF'ler `.gif`, JPEG'ler `.jpg` ya da `.jpeg`. Tarayıcılar ise dosyayı nasıl göstereceklerini **ortam türüne** (media type, eski adıyla MIME türü) bakarak anlar: GIF için `image/gif`, JPEG için `image/jpeg`.

Kullanıcıdan bir dosya adı isteyen ve ad (büyük/küçük harf fark etmeden) şu uzantılardan biriyle bitiyorsa ortam türünü yazan bir program yaz:

- `.gif` → `image/gif`
- `.jpg`, `.jpeg` → `image/jpeg`
- `.png` → `image/png`
- `.pdf` → `application/pdf`
- `.txt` → `text/plain`
- `.zip` → `application/zip`

Başka bir uzantı ya da hiç uzantı yoksa `application/octet-stream` yaz. (CS50'de dosyanın adı `extensions.py`.)

## Nasıl denenir

CS50'nin verdiği durumlar; Odyssey her birini ayrı çalıştırıp çıktını karşılaştırıyor. Soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir.

- Girdi `happy.jpg` → çıktı `image/jpeg`
- Girdi `document.pdf` → çıktı `application/pdf`
- Girdi `Photo.PNG` → çıktı `image/png`
- Girdi ` notes.txt ` → çıktı `text/plain`
- Girdi `cat.gif` → çıktı `image/gif`
- Girdi `picture.jpeg` → çıktı `image/jpeg`
- Girdi `archive.ZIP` → çıktı `application/zip`
- Girdi `page.html` → çıktı `application/octet-stream`
- Girdi `README` → çıktı `application/octet-stream`
