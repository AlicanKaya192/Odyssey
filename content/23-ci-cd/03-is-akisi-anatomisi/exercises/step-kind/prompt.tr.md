Bir adım bir sözlük. `step_kind(step)` fonksiyonunu yaz:

- `uses` ve `run` ikisi birden varsa: `"invalid"`
- Yalnızca `uses` varsa: `"action: "` + eylemin adı
- Yalnızca `run` varsa: `"command: "` + komutun **ilk satırı**
- İkisi de yoksa: `"invalid"`

Çok satırlı bir `run` metninin satırları `"\n"` ile ayrılır.

**Beklenen çıktı:**

```
action: actions/checkout@v4
command: python -m pytest
command: pip install -U pip
invalid
invalid
```
