## os.path

| Yazım | Ne verir |
|---|---|
| `os.path.join("a", "b.txt")` | `a\b.txt` (Windows) / `a/b.txt` |
| `os.path.basename(p)` / `dirname(p)` | dosya adı / klasör |
| `os.path.splitext(p)` | `(ad, son uzantı)` |
| `os.path.exists(p)` | var mı |
| `os.path.isfile(p)` / `isdir(p)` | dosya mı / klasör mü |
| `os.path.getsize(p)` | bayt |
| `os.path.abspath(p)` | mutlak yol |
| `os.path.relpath(p, start)` | `start`'a göre göreli yol |

## os

| Yazım | Ne yapar |
|---|---|
| `os.getcwd()` | programın çalıştığı klasör |
| `os.listdir(k)` | içindekiler (sırasız) |
| `os.makedirs(k, exist_ok=True)` | klasör + aradakiler |
| `os.mkdir(k)` | tek klasör |
| `os.rename(eski, yeni)` | ad değiştir / taşı |
| `os.remove(d)` | dosyayı **kalıcı** sil |
| `os.rmdir(k)` | **boş** klasörü sil |
| `os.walk(k)` | `(root, dirs, files)` ağaç boyunca |
| `os.environ.get(ad, vars.)` | ortam değişkeni (metin) |
| `os.cpu_count()` | çekirdek sayısı |

Dolu bir klasörü silmek için `shutil.rmtree` (iki bölüm sonra).

## sys

| Yazım | Ne verir |
|---|---|
| `sys.version_info >= (3, 10)` | sürüm denetimi |
| `sys.platform` | `win32`, `linux`, `darwin` |
| `sys.argv` | komut satırı argümanları (ilki betik adı) |
| `sys.path` | modül arama klasörleri |
| `sys.executable` | çalışan Python'un yolu |
| `sys.exit(kod_ya_da_metin)` | programı bitir |
| `print(..., file=sys.stderr)` | hata akışına yaz |

## Dikkat

- Yolları `+` ile yapıştırma; `join` kullan.
- `os.listdir` sırasız; `sorted` ile sırala.
- `os.remove` geri dönüşüm kutusuna göndermez.
- Ortam değişkenleri metin; sayıyı `int`, evet/hayırı açık bir listeyle
  çevir.
