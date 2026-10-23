Hafta 9'da geçen her şey tek sayfada.

## Küme

| Yazım | Ne yapar |
|---|---|
| `houses = set()` | boş küme (`{}` boş **sözlük**) |
| `{"Gryffindor", "Slytherin"}` | değerleri olan küme |
| `houses.add("Ravenclaw")` | ekler; zaten varsa hiçbir şey değişmez |
| `"Ravenclaw" in houses` | içinde mi; kümede çok hızlı |
| `sorted(houses)` | sıralı bir liste (kümenin sırası yok) |

## Genel değişkenler ve sabitler

| Yazım | Ne yapar |
|---|---|
| `balance = 0` (dosyanın en üstünde) | genel değişken; fonksiyonlar okuyabilir |
| `global balance` | fonksiyonun içinde: bu ad genel değişken, değiştirilebilir |
| `MEOWS = 3` | sabit; büyük harf yalnızca gelenek, Python korumaz |
| `Cat.MEOWS` | sınıfın içindeki sabit |

## Tip belirtimleri ve belge dizeleri

```python
def meow(n: int) -> str:
    """Meow n times."""
    return "meow\n" * n


number: int = int(input("Number: "))
```

- `n: int` parametre, `-> str` dönüş değeri, `number: int` değişken
- Python belirtimi `meow.__annotations__`'ta saklar ama **denetlemez**
- Denetleyen ayrı program: `pip install mypy`, sonra `mypy meows.py`
- Değer döndürmeyen fonksiyon: `-> None`
- Belge dizesi gövdenin ilk satırında, üçlü tırnakla; `meow.__doc__`

## argparse

```python
import argparse

parser = argparse.ArgumentParser(description="Meow like a cat")
parser.add_argument("-n", default=1, help="number of times to meow", type=int)
args = parser.parse_args()
```

| Yazım | Ne yapar |
|---|---|
| `add_argument("-n", "--number")` | kısa ve uzun ad; değer `args.number` |
| `default=1` | verilmezse değer (yoksa `None`) |
| `type=int` | dönüştürür; geçersizse kullanımı yazıp çıkar (kod 2) |
| `help="..."` | `-h` / `--help` çıktısındaki açıklama |

## Açmak ve toplamak

| Yazım | Ne yapar |
|---|---|
| `first, _ = "David Malan".split(" ")` | iki değişkene açar; `_` kullanılmayan |
| `total(*coins)` | listeyi konumsal argümanlara açar |
| `total(**coins)` | sözlüğü `anahtar=değer` argümanlarına açar |
| `def f(*args):` | konumsal argümanları bir **demette** toplar |
| `def f(**kwargs):` | adlandırılmış argümanları bir **sözlükte** toplar |

## map, filter, kavramalar, enumerate

| Yazım | Ne yapar |
|---|---|
| `map(str.upper, words)` | her öğeye uygular; tek kullanımlık `map` nesnesi |
| `filter(lambda s: s["house"] == "Gryffindor", students)` | `True` dönenleri bırakır |
| `[w.upper() for w in words]` | liste kavraması |
| `[s["name"] for s in students if s["house"] == "Gryffindor"]` | koşullu liste kavraması |
| `{s: "Gryffindor" for s in names}` | sözlük kavraması |
| `for i, s in enumerate(names):` | sıra (sıfırdan) ve öğe |
| `enumerate(names, start=1)` | birden saymak |

## Üreteçler

```python
def sheep(n):
    for i in range(n):
        yield "🐑" * i
```

- `yield` bir değer verir, fonksiyon durur ve kaldığı yeri hatırlar
- Bütün veri bellekte tutulmaz; çok büyük `n`'de de hemen başlar
- `sheep(3)` gövdeyi çalıştırmaz, bir üreteç nesnesi döndürür
- `next(g)` sıradaki değer; değer kalmayınca `StopIteration`
- Üreteç bir kez tüketilir; yeniden gezmek için yeniden çağır
