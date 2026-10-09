A pattern where abstract base classes are often used: the **plugin**. The
program defines a contract; whoever wants to add a new format writes only a
new subclass and does not touch the rest of the program.

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

## What happens?

- **`__init_subclass__`** runs **the moment** a subclass of `Reader` is
  defined. The `suffix=".csv"` on the class line goes to it; the subclass
  registers itself in the `registry` dictionary.
- `read` knows no reader by name: it looks at the extension, finds the class
  in the registry and calls `parse`.
- To add a new format (`.json`), only `class JsonReader(Reader,
  suffix=".json")` is written; `read` is not touched.
- Thanks to `@abstractmethod`, a plugin that forgets `parse` raises an error
  the first time it is built.

This is a small version of how large libraries (web frameworks, test tools,
data readers) discover their extensions.
