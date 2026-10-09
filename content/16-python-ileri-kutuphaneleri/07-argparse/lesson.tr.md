# argparse

Bir betiği başkasının (ya da bir haftalık sonra senin) kullanacağı bir
**komut satırı aracına** çevirmek için ayarları kodun içine yazmak yerine
dışarıdan almak gerekir: `python report.py sales.csv --top 3 --verbose`.
`sys.argv` bunları düz metin listesi olarak verir; türü çevirmek, eksikleri
bulmak, yardım metni yazmak sana kalır. **`argparse`** bunların hepsini
yapar: argümanları tanımlarsın, o okur, çevirir, denetler ve `--help`
yazar.

Bu bölümdeki örnekler `parse_args`'a listeyi kendimiz veriyor; gerçek
programda liste verilmez ve `sys.argv` okunur.

## İlk ayrıştırıcı

```python
import argparse

parser = argparse.ArgumentParser(prog="report", description="Summarise a CSV file.")
parser.add_argument("path", help="the CSV file to read")
parser.add_argument("--top", type=int, default=5, help="how many rows to show")
parser.add_argument("--verbose", action="store_true", help="print details")
args = parser.parse_args(["sales.csv", "--top", "3"])
print(args)
print(args.path, args.top, args.verbose, type(args.top).__name__)
print(parser.parse_args(["data.csv", "--verbose"]))
```

```text
Namespace(path='sales.csv', top=3, verbose=False)
sales.csv 3 False int
Namespace(path='data.csv', top=5, verbose=True)
```

- **Konumsal** argüman (`path`) zorunludur, sırasıyla verilir.
- `--` ile başlayan **seçenekli** argüman (`--top`) isteğe bağlıdır;
  verilmezse `default` kullanılır.
- **`type=int`** metni sayıya çevirir (`args.top` gerçekten `int`).
- **`action="store_true"`** değer almayan bir anahtardır: yazılırsa `True`,
  yazılmazsa `False`.
- Sonuç bir `Namespace`: değerlere `args.path` gibi özellik olarak
  ulaşılır; `--top` gibi adlardaki tireler alt çizgiye döner.

## Çok değer, seçenekler, kısa adlar

```python
import argparse

parser = argparse.ArgumentParser(prog="convert")
parser.add_argument("files", nargs="+")
parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv")
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("--tag", action="append", default=[])
argv = ["a.txt", "b.txt", "-f", "json", "--tag", "x", "--tag", "y"]
args = parser.parse_args(argv)
print(args.files, args.format, args.quiet, args.tag)
```

```text
['a.txt', 'b.txt'] json False ['x', 'y']
```

- **`nargs="+"`** bir ya da daha çok değeri liste olarak alır (`"*"` sıfır
  ya da daha çok, `"?"` en fazla bir).
- **`choices`** yalnızca listedeki değerleri kabul eder.
- **`-f`, `--format`** aynı seçeneğin kısa ve uzun adı.
- **`action="append"`** seçenek her yazılışta listeye bir değer ekler.

## Yardım metni bedava

```python
import argparse

parser = argparse.ArgumentParser(prog="report", description="Summarise a CSV file.")
parser.add_argument("path", help="the CSV file to read")
parser.add_argument("--top", type=int, default=5, help="how many rows to show")
print(parser.format_help())
```

```text
usage: report [-h] [--top TOP] path

Summarise a CSV file.

positional arguments:
  path        the CSV file to read

options:
  -h, --help  show this help message and exit
  --top TOP   how many rows to show
```

Komut satırında `python report.py --help` (ya da `-h`) yazılınca bu metin
çıkar. `help=` açıklamaları buraya girer; kullanım satırı (`usage`) da
tanımdan kendiliğinden kurulur. İyi bir yardım metni aracın belgesidir.

## Hatalı girdi

```python
import argparse

parser = argparse.ArgumentParser(prog="report", exit_on_error=False)
parser.add_argument("--top", type=int, default=5)
parser.add_argument("--format", choices=["csv", "json"], default="csv")
for argv in (["--top", "ten"], ["--format", "xml"]):
    try:
        parser.parse_args(argv)
    except argparse.ArgumentError as error:
        print("ArgumentError:", error)
strict = argparse.ArgumentParser(prog="report")
strict.add_argument("path")
try:
    strict.parse_args([])
except SystemExit as error:
    print("SystemExit:", error.code)
```

```text
ArgumentError: argument --top: invalid int value: 'ten'
ArgumentError: argument --format: invalid choice: 'xml' (choose from 'csv', 'json')
SystemExit: 2
```

- `argparse` yanlış türü, listede olmayan seçimi ve eksik zorunlu argümanı
  kendisi yakalar ve ne olduğunu söyler.
- Varsayılan davranış: kullanım satırını ve hatayı hata akışına yazıp
  programı **çıkış kodu 2** ile bitirir (`SystemExit`). Komut satırı aracı
  için doğru olan budur.
- **`exit_on_error=False`** ile çıkmak yerine `ArgumentError` fırlatır;
  hatayı kendin ele almak istediğinde.

## Alt komutlar

```python
import argparse

parser = argparse.ArgumentParser(prog="notes")
commands = parser.add_subparsers(dest="command", required=True)
add = commands.add_parser("add")
add.add_argument("text")
show = commands.add_parser("list")
show.add_argument("--limit", type=int, default=10)
print(parser.parse_args(["add", "buy milk"]))
print(parser.parse_args(["list", "--limit", "3"]))
```

```text
Namespace(command='add', text='buy milk')
Namespace(command='list', limit=3)
```

`git commit`, `git push` gibi **alt komutlu** araçlar `add_subparsers` ile
kurulur: her alt komutun kendi argümanları var, hangisinin seçildiği
`dest="command"` ile `args.command`'a yazılır.

## main(argv=None): sınanabilir araç

```python
import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="greet")
    parser.add_argument("name")
    parser.add_argument("--times", type=int, default=1)
    args = parser.parse_args(argv)
    for _ in range(args.times):
        print(f"hello {args.name}")
    return 0


print(main(["ada", "--times", "2"]))
```

```text
hello ada
hello ada
0
```

`parse_args(None)` `sys.argv`'yi okur, liste verilirse onu. Aracı
`main(argv=None)` içine koymak, onu hem komut satırından çalıştırmayı hem de
testte argüman listesiyle çağırmayı sağlar. Dosyanın sonuna
`if __name__ == "__main__": sys.exit(main())` yazılır; dönüş değeri çıkış
kodu olur (0 başarı).

## Özet

- `ArgumentParser` + `add_argument` + `parse_args`; sonuç `Namespace`.
- Konumsal zorunlu, `--seçenek` isteğe bağlı; `type`, `default`, `choices`,
  `nargs`, `action="store_true"` / `"append"`.
- `--help` tanımdan kendiliğinden; `help=` açıklamaları.
- Hatalı girdi: kullanım + çıkış kodu 2 (ya da `exit_on_error=False`).
- Alt komutlar `add_subparsers`; araç `main(argv=None)` içinde.
