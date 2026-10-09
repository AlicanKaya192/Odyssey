## Basics (Python path)

| Code | Meaning |
|---|---|
| `x: int`, `def f(a: str) -> bool:` | a variable, a parameter, a return |
| `list[int]`, `dict[str, float]`, `tuple[int, str]` | containers |
| <code>str &#124; None</code> | text or nothing |
| `-> None` | returns nothing |

## Advanced forms

| Code | Meaning | From |
|---|---|---|
| `Literal["r", "w"]` | only these values | `typing` |
| `Final` | not reassigned | `typing` |
| `type Name = ...` | a type alias (3.12+) | the language |
| `Callable[[int, str], bool]` | a function type | `collections.abc` |
| `Iterable[int]`, `Sequence[str]` | "iterable", "ordered" | `collections.abc` |
| `TypedDict` + `NotRequired` | a dictionary with known keys | `typing` |
| `NamedTuple` | a typed, named tuple | `typing` |
| `def f[T](x: T) -> T` | a generic function (3.12+) | the language |
| `class Box[T]:` | a generic class (3.12+) | the language |
| `Any` | do not check | `typing` |
| `object` | could be anything, look first | built in |

## At run time

| Code | What it gives |
|---|---|
| `f.__annotations__` | the dictionary of hints |
| `typing.get_type_hints(f)` | the resolved hints |
| `typing.get_args(Literal["a", "b"])` | `("a", "b")` |
| `isinstance(x, int)` | a real check |

`isinstance(x, list[int])` does not work: a type with square brackets cannot
be checked at run time.

## Wide for parameters, narrow for returns

Write `Iterable[int]` for a parameter (a list, tuple, set, generator all
fit); write `list[int]` for a return (so the caller knows exactly what it
gets).
