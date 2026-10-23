Düzenli ifadelerde en sık yapılan hatalar (Python 3.14'te, bu bilgisayarda
ölçüldü). Kalıp hataları çoğu zaman **hata mesajı vermez**: kalıp yalnızca
beklediğin şeyi tutmaz. Her kalıbı tutması ve tutmaması gereken birkaç
girdiyle dene.

## Ham dizeyi unutmak

`r` olmadan `"\b"` Python için bir kontrol karakteri (geri silme); kalıba
kelime sınırı olarak gitmez. Hata yok, sonuç boş:

```python
import re

print(re.findall("\bum\b", "um, thanks, um"))
```

```text
$ python um.py
[]
```

`r` ile:

```python
import re

print(re.findall(r"\bum\b", "um, thanks, um"))
```

```text
$ python um.py
['um', 'um']
```

Kalıpları her zaman `r"..."` yaz.

## Noktayı kaçırmamak

`.edu` kalıbında nokta "herhangi bir karakter": `harvard?edu` de tutar.
Harfiyen nokta `\.`.

## ^ ve $'ı unutmak

`re.search` dizenin **herhangi bir yerinde** arar: `^` ve `$` olmadan
`"My email address is malan@harvard.edu."` da geçerli bir adres sayılır.
Dizenin tamamını denetleyeceksen `^...$` ya da `re.fullmatch`.

## Eşleşme yokken group çağırmak

Kalıp tutmazsa `re.search` `None` döndürür ve `None`'un `group`'u yok:

```python
import re

name = "David Malan"
matches = re.search(r"^(.+), *(.+)$", name)
print(matches.group(2))
```

```text
$ python format.py
Traceback (most recent call last):
  File "format.py", line 5, in <module>
    print(matches.group(2))
          ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
```

Önce sor: `if matches := re.search(...):`.

## Yanlış grup numarası

Bu kalıpta tek grup var; `group(2)` yok:

```python
import re

url = "https://twitter.com/davidjmalan"
matches = re.search(r"^https://twitter\.com/(\w+)$", url)
print(matches.group(2))
```

```text
$ python twitter.py
Traceback (most recent call last):
  File "twitter.py", line 5, in <module>
    print(matches.group(2))
          ~~~~~~~~~~~~~^^^
IndexError: no such group
```

Gruplar soldan sağa, açılan parantez sırasıyla 1'den sayılır. Yalnızca
gruplamak için kullandığın parantezi `(?:...)` yaparsan numaralar kaymaz.

## Kapanmamış parantez

Kalıbın kendisi hatalıysa `re` daha aramadan hata verir; mesaj hatanın
kalıptaki konumunu söyler (konum 0'dan sayılır):

```python
import re

print(re.search(r"^(\w+@\w+\.edu$", "malan@harvard.edu"))
```

```text
$ python validate.py
Traceback (most recent call last):
  File "validate.py", line 3, in <module>
  ...
re.PatternError: missing ), unterminated subpattern at position 1
```

## Açgözlü .+

`+` ve `*` tutabildiği **en uzun** parçayı alır. `<(.+)>` ilk `<`'den son
`>`'ye kadar her şeyi yakalar:

```python
import re

html = "<b>bold</b> and <i>it</i>"
print(re.findall(r"<(.+)>", html))
```

```text
$ python tags.py
['b>bold</b> and <i>it</i']
```

İçine ne gireceğini kümeyle sınırla: `[^>]+` "`>` dışındaki karakterler".

```python
import re

html = "<b>bold</b> and <i>it</i>"
print(re.findall(r"<([^>]+)>", html))
```

```text
$ python tags.py
['b', '/b', 'i', '/i']
```

## match ile search'ü karıştırmak

`re.match("b", "ab")` `None` döndürür: `match` yalnızca dizenin başından
bakar. Herhangi bir yerde aramak için `re.search`, dizenin tamamı için
`re.fullmatch`.
