`field_validator` ve `model_validator` hakkında bilmen gerekenler, hepsi
ölçüldü.

## `mode="after"` ve `mode="before"`

Varsayılan `after`: işlev tip denetiminden **sonra** çalışıyor, değer
zaten doğru tipte. `before` ise ham değeri alıyor; gelen veriyi tipe
uydurmak için kullanılır:

```python
class Post(BaseModel):
    tags: list[str] = []

    @field_validator("tags", mode="before")
    @classmethod
    def split(cls, value):
        if isinstance(value, str):
            return [t.strip() for t in value.split(",")]
        return value
```

`{"tags": "sf, classic"}` → `{"tags": ["sf", "classic"]}`; liste
gönderilirse olduğu gibi geçiyor.

## Başka bir alana bakmak

Alan doğrulayıcısı, kendinden **önce** tanımlanmış alanları `info.data`
içinde görür:

```python
class Range(BaseModel):
    a: int
    b: int

    @field_validator("b")
    @classmethod
    def b_after_a(cls, value, info):
        if "a" in info.data and value <= info.data["a"]:
            raise ValueError("b must be greater than a")
        return value
```

`{"a": 5, "b": 3}` → `422`, `loc: ["body", "b"]`. `a` kendisi bozuksa
(`"x"`) `info.data`'da yok; o yüzden `"a" in info.data` denetimi var.
İki alanlı kurallar için çoğu zaman `model_validator(mode="after")` daha
okunur.

## Sık yapılan hatalar

Hepsi ölçüldü; ilk üçü **hata vermeden** yanlış sonuç üretiyor, o yüzden
tehlikeli:

| Hata | Sonuç |
|---|---|
| `return value` unutuldu | `200`, alanın değeri `null` |
| `model_validator`'da `return self` unutuldu | `200`, cevap yalnızca `null` |
| `raise ValueError` yerine `return False` | `200`, alanın değeri `false` |
| Alan adı yanlış yazıldı (`"usernme"`) | Program açılırken `PydanticUserError` |

## Mesaj

`raise ValueError("must not contain spaces")` → `msg`:
`"Value error, must not contain spaces"`. Pydantic başa `Value error, `
ekliyor. Mesajı istemcinin okuyacağını düşünerek, kısa ve İngilizce yaz.
