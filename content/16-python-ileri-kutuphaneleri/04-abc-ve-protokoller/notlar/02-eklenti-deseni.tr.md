Soyut temel sınıfın sık kullanıldığı bir desen: **eklenti** (plugin).
Program bir sözleşme tanımlar; yeni bir biçim eklemek isteyen yalnızca yeni
bir alt sınıf yazar, programın geri kalanına dokunmaz.

```python
from abc import ABC, abstractmethod


class Reader(ABC):
    registry: dict[str, type["Reader"]] = {}

    def __init_subclass__(cls, suffix: str, **kwargs):
        super().__init_subclass__(**kwargs)
        Reader.registry[suffix] = cls

    @abstractmethod
    def parse(self, text: str) -> list[str]:
        ...


class CsvReader(Reader, suffix=".csv"):
    def parse(self, text):
        return text.split(",")


class LinesReader(Reader, suffix=".txt"):
    def parse(self, text):
        return text.splitlines()


def read(name: str, text: str) -> list[str]:
    suffix = name[name.rfind("."):]
    reader = Reader.registry[suffix]()
    return reader.parse(text)


print(sorted(Reader.registry))
print(read("a.csv", "x,y,z"), read("b.txt", "one\ntwo"))
```

```text
['.csv', '.txt']
['x', 'y', 'z'] ['one', 'two']
```

## Neler oluyor?

- **`__init_subclass__`**, `Reader`'dan bir alt sınıf **tanımlandığı anda**
  çalışır. Sınıf satırındaki `suffix=".csv"` ona gelir; alt sınıf kendini
  `registry` sözlüğüne kaydeder.
- `read` hiçbir okuyucuyu adıyla bilmiyor: uzantıya bakıp kayıttan sınıfı
  buluyor ve `parse`'ı çağırıyor.
- Yeni bir biçim (`.json`) eklemek için yalnızca
  `class JsonReader(Reader, suffix=".json")` yazılır; `read`'e dokunulmaz.
- `@abstractmethod` sayesinde `parse`'ı unutan bir eklenti, ilk kurulduğu
  anda hata verir.

Bu, büyük kütüphanelerin (web çatıları, test araçları, veri okuyucular)
uzantılarını tanıdığı yolun küçük bir hâlidir.
