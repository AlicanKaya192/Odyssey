`ENTRYPOINT` ile `CMD`'nin birlikte nasıl davrandığı. İmajın içinde
`python tool.py` duruyor ve konteyner `docker run imaj` ya da `docker run
imaj x y` ile çalıştırılıyor.

## Birleşim tablosu

| Dockerfile | `docker run imaj` | `docker run imaj x y` |
|---|---|---|
| `CMD ["python", "tool.py"]` | `python tool.py` | `x y` |
| `ENTRYPOINT ["python", "tool.py"]` | `python tool.py` | `python tool.py x y` |
| `ENTRYPOINT ["python", "tool.py"]` + `CMD ["--help"]` | `python tool.py --help` | `python tool.py x y` |
| `ENTRYPOINT python tool.py` (shell) | `/bin/sh -c "python tool.py"` | `/bin/sh -c "python tool.py"` (x y yok sayılır) |

Son satır neden "shell biçimli ENTRYPOINT yazma" dendiğini gösteriyor:
argümanlar hiç ulaşmıyor.

## Bir kerelik değiştirmek

| İstediğin | Komut |
|---|---|
| `CMD`'yi değiştirmek | `docker run imaj yeni komut` |
| `ENTRYPOINT`'i değiştirmek | `docker run --entrypoint sh imaj` |
| İkisini birden | `docker run --entrypoint python imaj -c "print(1)"` |

`--entrypoint` yalnızca programın adını alıyor; argümanları imajın adından
sonra yazılıyor.

## Python'da argümanlar

```python
import sys

print(sys.argv)
```

`docker run --rm imaj a b` → `['tool.py', 'a', 'b']`. `sys.argv[0]` dosyanın
adı, gerisi argümanlar. Daha düzenli bir komut satırı için Python'un
`argparse` modülü (`--help`'i kendisi üretiyor):

```python
import argparse

parser = argparse.ArgumentParser(description="Count words")
parser.add_argument("path")
parser.add_argument("--top", type=int, default=5)
args = parser.parse_args()
```

## Ortam değişkeni mi, argüman mı?

- **Argüman:** her çalıştırmada değişen, işin kendisi (hangi dosya, hangi
  ad).
- **Ortam değişkeni:** bir kez ayarlanan yapılandırma (hangi veritabanı,
  hangi kip). Ortam Değişkenleri bölümünde.
