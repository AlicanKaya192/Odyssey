Bağımlılığın kullanıldığı dört kalıp ve nerede işe yaradıkları.

| Kalıp | Yazım | Ne zaman? |
|---|---|---|
| Değer veren | `x: Annotated[T, Depends(f)]` | Ortak parametreler, kaydı bulmak |
| Yalnızca denetleyen | `@app.get(..., dependencies=[Depends(f)])` | Anahtar, izin, istek sınırı |
| Aç/kapat | `def f(): ... yield ... finally:` | Veritabanı bağlantısı, dosya |
| Zincir | `def f(x: Annotated[T, Depends(g)])` | Önce kullanıcı, sonra izni |

## Bağımlılık nereden okur?

Bağımlılığın parametreleri uç noktanınkiyle aynı kurallarla dolar:

| Parametre | Kaynak |
|---|---|
| Adreste `{book_id}` var | Yol |
| Basit tip, adreste yok | Sorgu |
| `Annotated[str, Header()]` | Başlık (`x_key` → `X-Key`) |
| Pydantic modeli | Gövde |
| `Annotated[T, Depends(g)]` | Başka bir bağımlılık |

## Adlandırılmış tip

Sık kullanılan bağımlılıklara ad ver:

```python
Paging = Annotated[dict, Depends(paging)]
CurrentBook = Annotated[dict, Depends(get_book)]


@app.get("/books/{book_id}")
def read_book(book: CurrentBook):
    return book
```

Uç noktalar kısa kalır ve "bu uç nokta neye ihtiyaç duyuyor" ilk satırdan
okunur.

## Sık yapılan hatalar

İlk üçü ölçüldü:

| Hata | Sonuç |
|---|---|
| `Depends(paging())` (parantezli) | Program açılırken `TypeError: {'limit': 10} is not a callable object` |
| Bağımlılıkta `return` yerine `print` | `200`, parametre `null` |
| `yield`'li bağımlılıkta `try/finally` yok | Uç nokta hata verirse kapanış **hiç çalışmıyor** |
| `dependencies=` ile verilen işlevin sonucunu kullanmaya çalışmak | Sonuç uç noktaya gelmez |

`Depends(paging)`'e **işlevin kendisi** verilir, çağrısı değil.
