## Sihirli metinlerin sorunu

Durumları düz metinle tutan kod, bir harf hatasını **sessizce** yutar:

```python
import json
from enum import Enum


class Status(Enum):
    PAID = "paid"
    SHIPPED = "shipped"


def is_done(status):
    return status == "shiped"


print(is_done("shipped"))
try:
    print(Status.SHIPED)
except AttributeError as error:
    print("AttributeError:", error)
try:
    json.dumps({"status": Status.SHIPPED})
except TypeError as error:
    print("TypeError:", error)
record = json.dumps({"order": 7, "status": Status.SHIPPED.value})
print(record)
print(Status(json.loads(record)["status"]) is Status.SHIPPED)
```

```text
False
AttributeError: type object 'Status' has no attribute 'SHIPED'
TypeError: Object of type Status is not JSON serializable
{"order": 7, "status": "shipped"}
True
```

- `"shiped"` yazım hatası hiçbir hata vermedi; fonksiyon her zaman `False`
  döndürüyor ve bu ancak bir sipariş "bitmedi" görünce fark edilir.
- Aynı hata enum'da **anında** `AttributeError` verdi: yanlış yazılan üye
  yok. Editörler de üyeleri önerir (`Status.` yazınca liste açılır).
- **JSON'a yazarken** üyenin kendisi değil `value`'su yazılır; üye doğrudan
  yazılamıyor (`TypeError`). Okurken `Status(değer)` ile geri üyeye
  çevrilir.

## Ne zaman enum?

| Durum | Seçim |
|---|---|
| Sabit, bilinen birkaç seçenek (durum, rol, renk) | `Enum` |
| Sıralı seçenek (öncelik, seviye) | `IntEnum` |
| Birleştirilebilen seçenek (izinler) | `Flag` |
| Seçenekler sürekli değişiyor, kullanıcı ekliyor | veritabanı / dosya |
| Tek bir sabit (`MAX_SIZE = 100`) | düz değişken |

## Enum'u dolaşmak ve eşlemek

```python
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"


LABELS = {Color.RED: "Kırmızı", Color.GREEN: "Yeşil"}
for color in Color:
    print(color.value, LABELS[color])
```

Üyeler sözlük anahtarı olabilir: her seçeneğin ekrandaki adı, rengi, simgesi
bir sözlükte tutulur. Yeni bir üye eklenip sözlüğe eklenmeyi unutulursa
`KeyError` hemen hatırlatır.
