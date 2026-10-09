## shutil

| Yazım | Ne yapar |
|---|---|
| `shutil.copy(k, h)` | dosya içeriğini kopyalar |
| `shutil.copy2(k, h)` | içerik + değiştirilme zamanı |
| `shutil.copytree(k, h)` | klasörü içindekilerle kopyalar |
| `copytree(..., ignore=shutil.ignore_patterns("*.log"))` | atlanacaklar |
| `copytree(..., dirs_exist_ok=True)` | var olan klasörün üstüne |
| `shutil.move(k, h)` | dosya ya da klasörü taşır |
| `shutil.rmtree(k)` | klasörü **içindekilerle, kalıcı** siler |
| `shutil.disk_usage(yol)` | `total`, `used`, `free` (bayt) |
| `shutil.which("git")` | programın yolu, yoksa `None` |

## glob

| Yazım | Ne verir |
|---|---|
| `glob.glob("*.csv")` | bu klasördeki `.csv` yolları (metin) |
| `glob.glob("data/**/*.csv", recursive=True)` | her derinlikte |
| `glob.glob("log_202?.txt")` | `?` tek karakter |
| `glob.glob("[!_]*.py")` | `_` ile başlamayanlar |
| `glob.escape(ad)` | adındaki `*`, `?`, `[` harf olarak aransın |

## Hangisi?

| İş | En kısa yol |
|---|---|
| Tek dosyayı kopyalamak | `shutil.copy2` |
| Klasörü kopyalamak | `shutil.copytree` |
| Taşımak / ad değiştirmek | `shutil.move` ya da `Path.rename` |
| Dosya silmek | `Path.unlink` |
| Boş klasör silmek | `Path.rmdir` |
| Dolu klasör silmek | `shutil.rmtree` |
| Kalıpla aramak | `Path.glob` / `glob.glob` |

## Dikkat

- `copy` hedef klasör yoksa o adla **dosya** oluşturur.
- `rmtree`'den önce yolu yazdırıp kontrol et.
- `glob.glob` sırasız; `sorted`.
