Bölümde öğrendiklerini birleştiren küçük ama tam bir araç: metin
dosyalarındaki en sık kelimeleri sayan `wordcount`.

```python
import argparse
from collections import Counter
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="wordcount", description="Count words in text files.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--lower", action="store_true")
    args = parser.parse_args(argv)
    counts = Counter()
    for path in args.files:
        text = path.read_text(encoding="utf-8")
        if args.lower:
            text = text.lower()
        counts.update(text.split())
    for word, n in counts.most_common(args.top):
        print(f"{n:>3} {word}")
    return 0


Path("a.txt").write_text("The cat and the dog", encoding="utf-8")
Path("b.txt").write_text("the end", encoding="utf-8")
main(["a.txt", "b.txt", "--top", "2"])
print("---")
main(["a.txt", "b.txt", "--top", "2", "--lower"])
```

```text
  2 the
  1 The
---
  3 the
  1 cat
```

- **`type=Path`**: `type` herhangi bir dönüştürücü olabilir; dosya adları
  doğrudan `Path` nesnesi oldu.
- `--lower` olmadan `The` ve `the` ayrı sayıldı; anahtar verilince üçü
  birleşti.
- `main` bir dönüş değeri veriyor; gerçek dosyada son satır
  `if __name__ == "__main__": sys.exit(main())` olur ve terminalde
  `python wordcount.py a.txt b.txt --top 2 --lower` diye çalıştırılır.

## İyi bir komut satırı aracı

- Her argümana `help=` yaz; `--help` aracın belgesidir.
- Makul varsayılanlar ver; en sık kullanım hiç seçenek yazmadan çalışsın.
- Asıl çıktıyı `print` ile stdout'a, durum ve hata mesajlarını `logging`
  ya da stderr'e yaz: çıktı başka bir programa borulanabilsin.
- Başarıda 0, hatada 0'dan farklı çıkış koduyla bit.
- Mantığı `main(argv=None)` içinde tut; testten liste vererek çağır.
