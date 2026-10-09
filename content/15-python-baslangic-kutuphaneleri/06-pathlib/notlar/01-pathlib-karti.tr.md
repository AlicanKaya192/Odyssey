## Kurmak

| Yazım | Sonuç |
|---|---|
| `Path("data") / "sales.csv"` | birleştirilmiş yol |
| `Path.cwd()` | çalışılan klasör |
| `Path.home()` | ev klasörü |
| `Path(__file__).parent` | bu dosyanın klasörü |
| `p.resolve()` | mutlak yol |

## Parçalar (diske dokunmaz)

| Özellik / metot | `Path("data/raw/sales.csv")` için |
|---|---|
| `p.name` | `sales.csv` |
| `p.stem` | `sales` |
| `p.suffix` / `p.suffixes` | `.csv` / `['.csv']` |
| `p.parent` | `data/raw` |
| `p.parts` | `('data', 'raw', 'sales.csv')` |
| `p.with_suffix(".txt")` | `data/raw/sales.txt` |
| `p.with_stem("stock")` | `data/raw/stock.csv` |
| `p.as_posix()` | `/` ile metin |
| `p.relative_to("data")` | `raw/sales.csv` |

## Disk işleri

| Metot | Ne yapar |
|---|---|
| `p.exists()`, `is_file()`, `is_dir()` | var mı, ne |
| `p.read_text(encoding="utf-8")` | bütün içerik |
| `p.write_text(metin, encoding="utf-8")` | yazar (üzerine) |
| `p.read_bytes()`, `write_bytes()` | ikili içerik |
| `p.mkdir(parents=True, exist_ok=True)` | klasör |
| `p.iterdir()` | klasörün içi |
| `p.glob("*.csv")` / `rglob("*.csv")` | arama / alt klasörlerle |
| `p.rename(yeni)` | ad değiştir, taşı |
| `p.unlink(missing_ok=True)` | dosyayı sil |
| `p.rmdir()` | boş klasörü sil |
| `p.stat().st_size` | bayt |

## Glob kalıpları

| Kalıp | Eşleşen |
|---|---|
| `*.csv` | bu klasördeki `.csv` dosyaları |
| `sales_*.csv` | `sales_` ile başlayanlar |
| `*/*.py` | bir alt klasördeki `.py` dosyaları |
| `**/*.py` | her derinlikte (`rglob("*.py")` ile aynı) |
| `report_?.txt` | `?` tek karakter: `report_1.txt` |
