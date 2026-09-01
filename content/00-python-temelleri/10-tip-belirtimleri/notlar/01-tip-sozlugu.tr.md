# Tip Sözlüğü

Karşılaşacağın belirtimlerin listesi. Ezberlemek için değil, takıldığında
bakmak için.

## Temel tipler

| Belirtim | Ne demek | Örnek değer |
|---|---|---|
| `str` | Metin | `"Ada"` |
| `int` | Tam sayı | `42` |
| `float` | Ondalıklı sayı | `3.14` |
| `bool` | Doğru / yanlış | `True` |
| `bytes` | Ham bayt dizisi | `b"abc"` |
| `None` | Değer yok | `None` |

`int` yazılan bir yere `float` verilebiliyor; tersi genelde kastedilmiyor.
Python'da `True` aynı zamanda `1` sayılıyor ama belirtimde `bool` ile `int`
ayrı tutulur.

## Kaplar

Kabın içinde ne olduğunu köşeli parantezle yazıyorsun.

| Belirtim | Ne demek |
|---|---|
| `list[str]` | Metinlerden oluşan liste |
| `dict[str, int]` | Metin anahtarlı, sayı değerli sözlük |
| `set[str]` | Metinlerden oluşan küme |
| `tuple[int, int]` | **Tam olarak iki** tam sayılı demet |
| `tuple[int, ...]` | Uzunluğu belli olmayan, hepsi sayı olan demet |

Demette bir incelik var: `tuple[int, str]` "birinci eleman sayı, ikinci eleman
metin" demek — sıra önemli. Listede ise `list[int]` bütün elemanlar için
geçerli.

## Birden fazla ihtimal

| Belirtim | Ne demek |
|---|---|
| `int \| None` | Ya tam sayı ya hiçbir şey |
| `int \| str` | Ya tam sayı ya metin |
| `list[int \| str]` | Elemanları sayı ya da metin olan liste |

En sık göreceğin biçim `X | None`. Bir fonksiyon "bulursam veririm,
bulamazsam vermem" diyorsa dönüşü böyle yazılıyor.

## İç içe kaplar

Kabın içine kap koyabiliyorsun. Uzuyorlar ama kuralı aynı:

| Belirtim | Ne demek |
|---|---|
| `list[list[int]]` | Sayı listelerinden oluşan liste |
| `dict[str, list[int]]` | Her anahtarın altında bir sayı listesi |
| `list[dict[str, str]]` | Sözlüklerden oluşan liste |
| `dict[str, dict[str, int]]` | Sözlük içinde sözlük |

Üçüncüsü veri işlerinde çok karşına çıkacak: bir CSV dosyasının her satırı
bir sözlük, dosyanın tamamı o sözlüklerin listesi.

## Fonksiyonun kendisi

Bir fonksiyon başka bir fonksiyonu parametre olarak alabiliyor. O zaman:

```python
from typing import Callable

def apply_twice(func: Callable[[int], int], value: int) -> int:
    return func(func(value))
```

`Callable[[int], int]` şu demek: "bir tam sayı alıp bir tam sayı döndüren bir
fonksiyon". İlk köşeli parantez parametreleri, ikincisi dönüşü tutuyor.

Şimdilik tanıman yeterli; yazman gereken bir yer nadiren çıkar.

## Kaçış kapısı: `Any`

```python
from typing import Any

def dump(value: Any) -> str:
    return str(value)
```

`Any` "her şey olabilir" demek. Yazması kolay ama belirtimin bütün faydasını
siliyor — editör de artık bir şey söyleyemiyor.

Gerçekten her tipi kabul eden bir şey yazmıyorsan kullanma. `Any` yazmak,
belirtimi hiç yazmamaktan pek farklı değil.

## Eski karşılıkları

Python 3.9 öncesinde kaplar `typing` modülünden alınıyordu. Eski kodda
göreceğin biçim solda:

| Eski | Yeni |
|---|---|
| `List[str]` | `list[str]` |
| `Dict[str, int]` | `dict[str, int]` |
| `Set[str]` | `set[str]` |
| `Tuple[int, int]` | `tuple[int, int]` |
| `Optional[str]` | `str \| None` |
| `Union[int, str]` | `int \| str` |

Yeni yazarken sağdakini kullan. Soldakini yalnızca okuyabilmen yeterli.
