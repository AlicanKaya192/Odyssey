Belirtimlerin asıl kazancı, kod **çalışmadan** yakalanan hatalardır. Bunu
**tip denetleyicisi** yapar: kodu okur, türleri izler ve uyuşmayanı
gösterir. En yaygın ikisi **mypy** (komut satırı aracı, `pip install mypy`,
sonra `mypy dosya.py`) ve **Pyright** (VS Code'da Pylance eklentisinin
içinde, yazarken altı çizili uyarı olarak).

## Neleri yakalar?

| Kod | Denetleyici ne der |
|---|---|
| `area("ab", 2)` | `str`, `float` bekleyen yere verilmiş |
| `open_log("app.log", "x")` | `"x"`, `Literal["r", "w", "a"]` değil |
| `MAX_SIZE = 5` (`Final` iken) | `Final` yeniden atanamaz |
| `name.upper()` (<code>name: str &#124; None</code> iken) | `None`'ın `upper`'ı yok |
| `movie["ratng"]` (`TypedDict`) | böyle bir anahtar yok |
| `return` unutulmuş `-> int` | `None` dönebilir |

## None'ı daraltmak

`str | None` türündeki bir değeri kullanmadan önce `None` olmadığını
göstermen gerekir; `if` ile baktıktan sonra denetleyici türü **daraltır**:

```python
def label(name: str | None) -> str:
    if name is None:
        return "anonymous"
    return name.upper()


print(label(None), label("ada"))
```

```text
anonymous ADA
```

`if name is None: return` satırından sonra denetleyici `name`'in artık
`str` olduğunu bilir; `name.upper()` uyarı almaz. Aynı daraltma
`isinstance` ile de olur.

## Nereden başlamalı?

- Belirtimler **kademeli** eklenir (gradual typing): belirtimsiz kod da
  çalışır ve denetlenir; önemli fonksiyonlardan başla.
- Önce **fonksiyon imzaları** (parametreler ve dönüş): en çok hatayı onlar
  yakalar. Yerel değişkenlerin türünü denetleyici çoğu zaman kendisi çıkarır.
- Dışarıdan gelen veriyi (JSON, CSV) `TypedDict` ile tarif et.
- `Any` denetimi kapatır; kullanmak zorunda kalırsan bilinçli kullan.
- Belirtim hiçbir şeyi çalışma anında denetlemez: kullanıcıdan gelen
  değeri yine kendin doğrula.
