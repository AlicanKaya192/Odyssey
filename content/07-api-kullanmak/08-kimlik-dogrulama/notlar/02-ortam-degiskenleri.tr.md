Anahtarı koddan ayırmanın pratik yolları.

## Ortam değişkeni

Windows komut satırında (yalnızca o pencere için):

```text
set LIBRARY_KEY=gercek-anahtarin
python program.py
```

PowerShell'de:

```text
$env:LIBRARY_KEY = "gercek-anahtarin"
python program.py
```

Python'da okumak:

```python
import os

key = os.environ.get("LIBRARY_KEY")
if key is None:
    raise SystemExit("LIBRARY_KEY tanımlı değil")
```

Gerçek projede varsayılan değer koyma: anahtar yoksa program sessizce yanlış
anahtarla çalışmasın, açıkça dursun.

## `.env` dosyası

Projelerde anahtarlar çoğu zaman proje klasöründeki `.env` dosyasında:

```text
LIBRARY_KEY=gercek-anahtarin
LIBRARY_TOKEN=baska-bir-jeton
```

Bu dosyayı okuyan hazır paketler var (`python-dotenv` gibi). Kendin de
okuyabilirsin:

```python
def load_env(path=".env"):
    values = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip()
    return values
```

## `.gitignore`

`.env` dosyasının git'e girmemesi için proje kökündeki `.gitignore`
dosyasına bir satır:

```text
.env
```

Örnek olarak paylaşmak istersen değerleri boş bir `.env.example` dosyası
koy; herkes kendi anahtarını doldursun.

## Sızdıysa

1. Anahtarı API'nin panelinden **hemen iptal et**.
2. Yenisini al, ortam değişkenine koy.
3. Git geçmişinden silmeye çalışmak iptalin yerini tutmaz: kopyalar çoktan
   başka yerlerde olabilir.
