# Düzenli İfadeler

CS50 Python'un sekizinci haftası. Videoyu **Video** sekmesinden
izleyebilirsin; bu sayfa dersin yazılı hâli. **Düzenli ifade** (regular
expression, kısaca regex) bir **kalıptır** (pattern). Programlamada veriyi,
çoğu zaman kullanıcının girdisini, bir kalıpla karşılaştırmak çok yaygın:
yazılan şey gerçekten bir e-posta adresine benziyor mu? Bu hafta kalıplarla
üç iş yapacağız: veriyi **doğrulamak**, **temizlemek** ve içinden bilgi
**çıkarmak**.

## Kalıpsız doğrulama

Bir e-posta adresini doğrulayalım. En gevşek kural: içinde `@` varsa
geçerli say. `validate.py`:

```python
email = input("What's your email? ").strip()

if "@" in email:
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@harvard.edu
Valid
```

`"@" in email` dizenin herhangi bir yerinde `@` arıyor. Sorun şu: yalnızca
`@` yazan biri de geçiyor.

```text
$ python validate.py
What's your email? @
Valid
```

Biraz daha sıkı olalım: adresi `@`'den ikiye bölüp (`split`) solda bir
kullanıcı adı olmasını, sağdaki alan adının `.edu` ile bitmesini isteyelim:

```python
email = input("What's your email? ").strip()

username, domain = email.split("@")

if username and domain.endswith(".edu"):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@harvard.edu
Valid
```

`if username` dize boş değilse doğru sayılır. Ama bu da kandırılıyor:

```text
$ python validate.py
What's your email? malan@.edu
Valid
```

`malan@.edu`'da alan adı yok. Her yeni eksik için bir koşul daha eklemek
çabucak büyüyor. Bu iş için Python'un **`re`** kütüphanesi var.

## re.search

`re.search(kalıp, dize)` kalıbı dizede arar; bulursa bir eşleşme nesnesi
(doğru sayılır), bulamazsa `None` döndürür. En basit kalıp harfiyen bir
metindir:

```python
import re

email = input("What's your email? ").strip()

if re.search("@", email):
    print("Valid")
else:
    print("Invalid")
```

Bu, `"@" in email`'den farklı değil. Güç, kalıbın içindeki özel
işaretlerden geliyor:

| İşaret | Anlamı |
|---|---|
| `.` | satır sonu dışında herhangi bir karakter |
| `*` | soldakinden sıfır ya da daha fazla |
| `+` | soldakinden bir ya da daha fazla |
| `?` | soldakinden sıfır ya da bir (isteğe bağlı) |
| `{m}` | soldakinden tam `m` tane |
| `{m,n}` | soldakinden `m` ile `n` arası |

"Solda bir şey, `@`, sağda bir şey" kalıbı `.+@.+`:

```python
import re

email = input("What's your email? ").strip()

if re.search(".+@.+", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@
Invalid
```

İlk denemede `.*@.*` yazsaydık `malan@` geçerdi: `*` "sıfır ya da daha
fazla" olduğu için `@`'den sonra hiçbir şey olmaması da kabul. `.+` ile en az
bir karakter şart. (`..*` de aynı işi görür: bir nokta, sonra sıfır ya da
daha fazla.)

`re.search` kalıbı soldan sağa okuyup bir **sonlu durum makinesi** (finite
state machine) gibi çalışır: başlangıç durumundan, her karakterle bir sonraki
duruma geçmeye çalışır; girdinin sonunda bir kabul durumundaysa kalıp
tutmuştur.

## Kaçış ve ham dize

Sona `.edu` ekleyelim: `.+@.+.edu`. Ama buradaki nokta da "herhangi bir
karakter":

```text
$ python validate.py
What's your email? malan@harvard?edu
Valid
```

Harfiyen nokta için önüne **ters bölü** koyarız: `\.`. Ters bölü Python
dizesinde de özeldir (`\n` satır sonu); Python'un ona dokunmaması için kalıbı
**ham dize** (raw string) yaparız: başına `r`.

```python
import re

email = input("What's your email? ").strip()

if re.search(r".+@.+\.edu", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@harvard?edu
Invalid
```

Kalıplarda ters bölü olmasa da hep `r"..."` yazmak iyi bir alışkanlık: sonra
bir `\` eklediğinde unutmazsın.

## Baştan sona: ^ ve $

Bu kalıp bir cümlenin içindeki adresi de kabul eder:

```text
$ python validate.py
What's your email? My email address is malan@harvard.edu.
Valid
```

`^` dizenin **başında**, `$` **sonunda** eşleşmek demek. İkisi birlikte
"dizenin tamamı bu kalıp olsun":

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^.+@.+\.edu$", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? My email address is malan@harvard.edu.
Invalid
```

## Karakter kümeleri

`.` hâlâ fazla cömert: `@` da bir karakter, yani `malan@@@harvard.edu`
geçiyor. **Köşeli parantez** bir karakter kümesi tanımlar: `[abc]` bu
üçünden biri, `[a-z]` aralık, `[^@]` ise `@` **dışındaki** herhangi bir
karakter (köşeli parantezin içindeki `^` "değil" demek):

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^[^@]+@[^@]+\.edu$", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@@@harvard.edu
Invalid
```

Kullanıcı adını harf, rakam ve alt çizgiyle sınırlamak için
`[a-zA-Z0-9_]`. Bu küme o kadar yaygın ki kısaltması var: `\w`, "kelime
karakteri". Hazır kümelerin bazıları:

| İşaret | Anlamı |
|---|---|
| `\d` | rakam (`0`–`9`) |
| `\D` | rakam olmayan |
| `\s` | boşluk karakteri (boşluk, sekme...) |
| `\S` | boşluk olmayan |
| `\w` | kelime karakteri: harf, rakam, `_` |
| `\W` | kelime karakteri olmayan |

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^\w+@\w+\.edu$", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? MALAN@HARVARD.EDU
Invalid
```

## Bayraklar

`MALAN@HARVARD.EDU` düşer, çünkü kalıp küçük harfle `edu` istiyor. Girdiyi
`lower()` ile küçültebilirdik; ama `re.search`'ün üçüncü argümanı
**bayraklar** (flags): `re.IGNORECASE` büyük/küçük harfi yok sayar.
(`re.MULTILINE` çok satırlı metin, `re.DOTALL` noktanın satır sonunu da
tutması için.)

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^\w+@\w+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? MALAN@HARVARD.EDU
Valid
```

## Gruplar ve isteğe bağlı parçalar

`malan@cs50.harvard.edu` düşer: alan adında iki nokta var. Bir alt alan
(subdomain) olabilir de olmayabilir de. **Parantez** parçaları gruplar,
arkasındaki `?` grubun tamamını isteğe bağlı yapar:

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^\w+@(\w+\.)?\w+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@cs50.harvard.edu
Valid
```

`?`'yi parantezsiz yalnızca `\.`'nın arkasına koysaydık, yalnızca nokta
isteğe bağlı olurdu. `|` "ya da" demek: `(com|edu)` ikisinden biri;
`(\w|\.)+` harf, rakam, alt çizgi ya da nokta.

| Yazım | Anlamı |
|---|---|
| <code>A&#124;B</code> | A ya da B |
| `(...)` | grup (ve yakalama) |
| `(?:...)` | yakalamayan grup |

Bütün bunlara rağmen e-posta adreslerinin resmî kuralı çok daha geniş;
tarayıcıların kullandığı kalıp ekranı dolduruyor. Gerçek bir programda bu
iş için yaygın bir kütüphane kullanılır (problem setindeki Response
Validation tam bu). `re.match` kalıbı dizenin başından,
`re.fullmatch` dizenin tamamıyla eşleştirir; onlarla `^` ve `$` yazmaya gerek
kalmaz.

## Temizlemek: yakalama

Kullanıcılar adlarını bazen `Malan, David` diye yazar. Hepsini `David Malan`
biçiminde saklamak isteyelim. `split(", ")` ile başlayalım, `format.py`:

```python
name = input("What's your name? ").strip()

if "," in name:
    last, first = name.split(", ")
    name = f"{first} {last}"

print(f"hello, {name}")
```

```text
$ python format.py
What's your name? Malan, David
hello, David Malan
```

Virgülden sonra boşluk unutulursa program çöküyor:

```text
$ python format.py
What's your name? Malan,David
Traceback (most recent call last):
  File "format.py", line 4, in <module>
    last, first = name.split(", ")
    ^^^^^^^^^^^
ValueError: not enough values to unpack (expected 2, got 1)
```

Düzenli ifadede parantezin bir işi daha var: içindekini **yakalar**
(capture). `re.search` dönen eşleşme nesnesinden yakalananları verir:
`matches.groups()` hepsini, `matches.group(1)` birinciyi (gruplar 1'den
sayılır; `group(0)` eşleşmenin tamamı). Boşluk sayısını ` *` ile serbest
bırakalım:

```python
import re

name = input("What's your name? ").strip()

matches = re.search(r"^(.+), *(.+)$", name)
if matches:
    name = matches.group(2) + " " + matches.group(1)

print(f"hello, {name}")
```

```text
$ python format.py
What's your name? Malan,David
hello, David Malan
```

### Mors işleci

"Ata, sonra `if` ile sor" o kadar yaygın ki Python'da tek satırda yazılabilir:
`:=` hem atar hem değeri koşulda kullanır. Yandan bakınca bir morsa
benzediği için **mors işleci** (walrus operator) deniyor:

```python
import re

name = input("What's your name? ").strip()

if matches := re.search(r"^(.+), *(.+)$", name):
    name = matches.group(2) + " " + matches.group(1)

print(f"hello, {name}")
```

Çıktı aynı.

## Çıkarmak: re.sub

Kullanıcıdan Twitter profilinin adresini (bugün adı X) alıp kullanıcı adını
çıkaralım. `twitter.py`:

```python
url = input("URL: ").strip()

username = url.replace("https://twitter.com/", "")
print(f"Username: {username}")
```

```text
$ python twitter.py
URL: https://twitter.com/davidjmalan
Username: davidjmalan
```

Ama `http://`, `www.` ya da protokolsüz bir adres gelirse ya da adres bir
cümlenin içindeyse iş bozuluyor. `str.removeprefix` cümle sorununu çözer, öte
yandakileri çözmez. `re.sub(kalıp, yerine, dize)` düzenli ifadeyle bul ve
değiştir yapar:

```python
import re

url = input("URL: ").strip()

username = re.sub(r"^(https?://)?(www\.)?twitter\.com/", "", url)
print(f"Username: {username}")
```

```text
$ python twitter.py
URL: http://www.twitter.com/davidjmalan
Username: davidjmalan
```

Kalıbın her parçası bir sorunu çözüyor: `^` baştan, `s?` `http` ya da
`https`, `(www\.)?` isteğe bağlı `www.`, `(https?://)?` isteğe bağlı protokol,
`twitter\.com`'daki `\.` harfiyen nokta.

### Yalnızca eşleşirse

`re.sub` kalıp tutmasa da dizeyi olduğu gibi döndürür; `https://google.com/`
kullanıcı adı diye yazılırdı. `re.search` ile koşullu yapalım. `(www\.)?`'nin
parantezi de yakalar, yani kullanıcı adı 2. grup olurdu; **yakalamayan grup**
`(?:...)` gruplar ama yakalamaz, kullanıcı adı 1. grupta kalır. Twitter'ın
kuralına göre kullanıcı adı yalnızca harf, rakam ve alt çizgi:

```python
import re

url = input("URL: ").strip()

if matches := re.search(
    r"^(?:https?://)?(?:www\.)?twitter\.com/([a-z0-9_]+)", url, re.IGNORECASE
):
    print("Username:", matches.group(1))
```

```text
$ python twitter.py
URL: twitter.com/davidjmalan/
Username: davidjmalan
```

```text
$ python twitter.py
URL: https://google.com/
```

Uzun bir kalıbı bir seferde yazmaya çalışma: küçük bir kalıpla başla,
çalıştığını gör, bir parça ekle, yine dene.

## Özet

`re`'de bunların yanında `re.split` (kalıba göre bölmek) ve `re.findall`
(bir kalıbın bütün eşleşmeleri) da var; alıştırmalarda kullanacaksın.
Düzenli ifadeler JavaScript, Java, Ruby gibi pek çok dilde de aynı yazımla
var.

- `re.search`, `re.match`, `re.fullmatch`; `re.sub`, `re.split`, `re.findall`
- `. * + ? {m} {m,n}`, `^ $`, `[...] [^...]`, `\d \s \w`, `A|B`, `(...)`,
  `(?:...)`
- Ham dize `r"..."`, kaçış `\.`
- Bayrak `re.IGNORECASE`
- Gruplar: `matches.group(1)`; mors işleci `:=`

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 7. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
