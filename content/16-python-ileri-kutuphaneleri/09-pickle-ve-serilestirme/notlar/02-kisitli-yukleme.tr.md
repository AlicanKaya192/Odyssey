Kural değişmiyor: güvenmediğin pickle verisini yükleme. Ama bazen elindeki
veri pickle'dan başka bir biçimde gelmiyor ve hangi türlerin içinde
olabileceğini biliyorsun. O durumda yükleyiciyi **kısıtlayabilirsin**.

Pickle verisi bir fonksiyon ya da sınıfa ihtiyaç duyduğunda onu
`find_class(modül, ad)` ile arar. Bu metot ezilirse yalnızca izin verilen
adlar geçer:

```python
import io
import pickle
from datetime import date

ALLOWED = {("datetime", "date")}


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in ALLOWED:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked: {module}.{name}")


def safe_loads(blob):
    return SafeUnpickler(io.BytesIO(blob)).load()


class Trap:
    def __reduce__(self):
        return (print, ("this ran while loading!",))


print(safe_loads(pickle.dumps({"day": date(2026, 3, 2), "n": [1, 2]})))
try:
    safe_loads(pickle.dumps(Trap()))
except pickle.UnpicklingError as error:
    print(error)
```

```text
{'day': datetime.date(2026, 3, 2), 'n': [1, 2]}
blocked: builtins.print
```

- Sözlük, liste, metin, sayı gibi temel türler `find_class`'a hiç uğramıyor;
  tarih için `datetime.date` izinli.
- Tuzak nesnesi `builtins.print`'i istedi ve durduruldu; mesaj hiç
  yazdırılmadı.
- `pickle.Unpickler(dosya)` bir dosya bekliyor; bellekteki baytlar
  `io.BytesIO` ile dosyaya benzetiliyor.

## Sınırları

- İzin listesi **dar** tutulur. `builtins` modülünün tamamına izin vermek
  (`eval`, `exec`, `open` dahil) korumayı ortadan kaldırır.
- Bu bir azaltma, tam güvence değil. Dışarıdan gelen veri için asıl çözüm
  yine JSON gibi yalnızca veri taşıyan bir biçim.
- Kendi ürettiğin dosyanın yolda değiştirilmediğinden emin olmak için
  baytları bir anahtarla imzalamak (`hmac`) da kullanılır; bu, ileride
  `hashlib` bölümünde.
