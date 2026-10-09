## Kalıbı adım adım kurmak

Uzun bir kalıbı tek seferde yazmaya çalışma; küçük parçadan başla, her
adımda örnek metinlerle dene:

1. Doğru olması gereken 3–4 örnek ve **yanlış** olması gereken 3–4 örnek yaz.
2. En küçük parçayı yaz (`\d{2}`), dene.
3. Bir parça ekle (`\d{2}:`), yeniden dene.
4. Bütün örnekler beklendiği gibi çıkana kadar sürdür.

Yanlış örnekler doğrularından daha önemlidir: kalıbı yazarken akla gelmeyen
metni kabul eden kalıp, ancak öyle yakalanır.

## Regex biçimi denetler, anlamı değil

Saat için `[0-2]\d:[0-5]\d` makul görünüyor: saat 0–2 ile başlıyor, dakika
0–5 ile.

```python
import re

samples = ["09:30", "23:59", "24:00", "29:99", "9:30"]
print([bool(re.fullmatch(r"[0-2]\d:[0-5]\d", s)) for s in samples])


def valid_time(text):
    if not re.fullmatch(r"\d{2}:\d{2}", text):
        return False
    hour, minute = int(text[:2]), int(text[3:])
    return hour < 24 and minute < 60


print([valid_time(s) for s in samples])
```

```text
[True, True, True, False, False]
[True, True, False, False, False]
```

Kalıp `24:00`'ı kabul etti: biçimi doğru ama öyle bir saat yok. Kalıbı daha
da karmaşık yazmak mümkün, ama okunması zorlaşır. Daha temiz yol işi
bölmek: **regex biçimi** ("iki rakam, iki nokta, iki rakam"), **Python
anlamı** (saat 24'ten, dakika 60'tan küçük) denetler.

Aynı şey tarihler için de geçerli: `\d{4}-\d{2}-\d{2}` `2026-02-30`'u kabul
eder. Biçimi regex ile denetledikten sonra `date.fromisoformat` ile gerçekten
tarihe çevirmeyi dene; geçersizse `ValueError` verir.

## E-posta gibi şeyler

E-posta adresinin kuralları o kadar geniş ki "doğru" bir regex yüzlerce
karakter tutar. Uygulamada yapılan şey basit bir biçim denetimi
(`\S+@\S+\.\S+`: boşluksuz, bir `@`, sonrasında bir nokta) ve adrese
doğrulama postası göndermektir. Regex "kesinlikle yanlış" olanı ayıklar,
"gerçekten var mı" sorusuna cevap veremez.

## Regex gerekmeyen yerler

| İş | Daha basit yol |
|---|---|
| Metin `"Error"` ile mi başlıyor? | `text.startswith("Error")` |
| İçinde `"@"` var mı? | `"@" in text` |
| Virgülle böl | `text.split(",")` |
| Yalnızca rakam mı? | `text.isdigit()` |

Metin metodu yetiyorsa onu kullan; okuyan herkes anlar. Regex, kalıp
gerçekten karmaşık olduğunda değerlidir.
