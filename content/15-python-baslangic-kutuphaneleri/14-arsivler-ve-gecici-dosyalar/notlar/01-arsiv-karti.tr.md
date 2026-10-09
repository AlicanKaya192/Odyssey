## zipfile

| Yazım | Ne yapar |
|---|---|
| `ZipFile(ad, "w", compression=ZIP_DEFLATED)` | sıkıştırarak yaz |
| `ZipFile(ad, "a")` | var olana ekle |
| `zf.write(dosya, arcname="klasör/ad")` | diskteki dosyayı ekle |
| `zf.writestr(ad, metin)` | içeriği doğrudan yaz |
| `zf.namelist()` / `zf.infolist()` | adlar / bilgiler |
| `info.file_size`, `info.compress_size` | asıl / arşivdeki boyut |
| `zf.read(ad)` | bayt; metin için `.decode("utf-8")` |
| `zf.extract(ad, klasör)` / `zf.extractall(klasör)` | çıkar |
| `zipfile.is_zipfile(ad)` | gerçekten zip mi |

## shutil

| Yazım | Ne yapar |
|---|---|
| `make_archive(ad, "zip", root_dir=klasör)` | klasörü arşivle |
| `unpack_archive(dosya, klasör)` | biçimi uzantıdan anlayıp aç |
| `get_archive_formats()` | `zip`, `tar`, `gztar`, `bztar`, `xztar`, `zstdtar` |

## gzip

| Yazım | Ne yapar |
|---|---|
| `gzip.compress(bayt)` / `gzip.decompress(bayt)` | bellekte |
| `gzip.open(ad, "wt", encoding="utf-8")` | metin olarak yaz |
| `gzip.open(ad, "rt", encoding="utf-8")` | metin olarak oku |

## tempfile

| Yazım | Ne verir |
|---|---|
| `TemporaryDirectory()` | blok bitince silinen klasör |
| `NamedTemporaryFile(delete=False)` | adı olan geçici dosya |
| `mkstemp(dir=..., suffix=...)` | `(tanıtıcı, ad)`: güvenle yazmak için |
| `gettempdir()` | sistemin geçici klasörü |

## Kurallar

- Sıkıştırma tekrardan beslenir; küçük ya da zaten sıkıştırılmış dosyada
  kazanç yok.
- Güvenmediğin arşivi boş, ayrı bir klasöre aç.
- Asıl dosyanın üstüne yazarken önce geçiciye yaz, sonra `os.replace`.
