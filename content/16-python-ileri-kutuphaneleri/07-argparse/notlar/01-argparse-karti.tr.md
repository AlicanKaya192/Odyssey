## İskelet

```python
import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tool", description="...")
    parser.add_argument("path")
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)
    ...
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## add_argument seçenekleri

| Yazım | Anlamı |
|---|---|
| `"path"` | konumsal, zorunlu |
| `"--top"`, `"-t", "--top"` | seçenekli; kısa ve uzun ad |
| `type=int`, `type=float`, `type=Path` | dönüştürücü |
| `default=5` | verilmezse |
| `required=True` | seçenekliyi zorunlu yapar |
| `choices=["csv", "json"]` | yalnızca bunlar |
| `nargs="+"` / `"*"` / `"?"` / `2` | bir+, sıfır+, en fazla bir, tam iki |
| `action="store_true"` | anahtar |
| `action="append"` | her yazılışta listeye ekle |
| `action="count"` | `-vvv` → 3 |
| `help="..."` | yardım metni |
| `dest="name"` | `args` içindeki ad |

## Diğer

| Yazım | Ne yapar |
|---|---|
| `parser.add_subparsers(dest="command")` | alt komutlar |
| `parser.format_help()` | yardım metnini döndürür |
| `ArgumentParser(exit_on_error=False)` | çıkmak yerine `ArgumentError` |
| `parser.error("mesaj")` | kendi hatanla çıkış kodu 2 |

Hatalı girdide varsayılan: kullanım satırı + hata stderr'e, çıkış kodu 2.
