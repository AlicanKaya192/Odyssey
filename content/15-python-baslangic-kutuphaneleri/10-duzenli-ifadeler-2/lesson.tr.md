# Düzenli İfadeler 2: Gruplar ve Değiştirmek

Önceki bölümde bir kalıbın **nerede** geçtiğini bulduk. Çoğu zaman bundan
fazlası gerekir: bir tarihin yılını, ayını, gününü **ayrı ayrı** almak, bir
kayıt satırını parçalarına ayırmak, metinde bir şeyi **değiştirmek**. Bu
bölümde gruplarla parça çekmeyi, `sub` ile değiştirmeyi, `split` ile bölmeyi
ve kalıbın ne kadar "yuttuğunu" (açgözlü / tembel) görüyoruz.

## Gruplar: parçaları ayrı almak

Kalıbın bir bölümünü **parantez** içine almak onu bir **grup** yapar;
eşleşmeden sonra her grup ayrıca okunur.

```python
import re

m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "Due on 2026-03-15, paid")
print(m.group(0), m.group(1), m.group(2), m.group(3))
print(m.groups())
year, month, day = m.groups()
print(int(day) + 1)
```

```text
2026-03-15 2026 03 15
('2026', '03', '15')
16
```

- `group(0)` (ya da `group()`) eşleşmenin tamamı; `group(1)`, `group(2)`...
  parantezler, soldan sağa.
- `groups()` bütün grupları demet olarak verir; doğrudan değişkenlere
  açılabilir.
- Gruplar da **metindir**: hesap için `int(...)`.

## Adlı gruplar

Grup sayısı arttıkça `group(3)` gibi numaralar okunmaz olur.
**`(?P<ad>...)`** gruba ad verir:

```python
import re

pattern = r"(?P<user>[\w.]+)@(?P<domain>[\w.]+)"
m = re.search(pattern, "Write to ada.l@example.com today")
print(m.group("user"), m.group("domain"))
print(m.groupdict())
```

```text
ada.l example.com
{'user': 'ada.l', 'domain': 'example.com'}
```

`groupdict()` adlı grupları sözlük yapar. `[\w.]+` "kelime karakteri ya da
nokta": köşeli parantez içinde nokta özel anlamını kaybeder, harf olarak
aranır.

## findall ve finditer gruplarla

```python
import re

text = "pen=3, book=12, ink=7"
print(re.findall(r"\w+=\d+", text))
print(re.findall(r"(\w+)=(\d+)", text))
print({name: int(n) for name, n in re.findall(r"(\w+)=(\d+)", text)})
for m in re.finditer(r"(\w+)=(\d+)", text):
    print(m.start(), m.group(1))
```

```text
['pen=3', 'book=12', 'ink=7']
[('pen', '3'), ('book', '12'), ('ink', '7')]
{'pen': 3, 'book': 12, 'ink': 7}
0 pen
7 book
16 ink
```

- Kalıpta grup **yoksa** `findall` eşleşen metinleri verir.
- Grup **varsa** eşleşmenin tamamını değil, **grupları** verir: her eşleşme
  için bir demet. Bu, `key=value` metnini tek satırda sözlüğe çevirdi.
- **`finditer`** her eşleşmenin **nesnesini** sırayla verir: konum
  (`start`) gibi ek bilgi gerektiğinde ya da metin çok uzunsa (hepsini
  listede toplamaz).

## Ya o ya bu: |

```python
import re

print(re.findall(r"cat|dog", "cat, dog, bird, catalog"))
print(re.findall(r"\b(?:cat|dog)s?\b", "cats and dogs and catalog"))
print(re.findall(r"\b(cat|dog)s?\b", "cats and dogs and catalog"))
```

```text
['cat', 'dog', 'cat']
['cats', 'dogs']
['cat', 'dog']
```

- `cat|dog` "cat **ya da** dog". Kelime sınırı olmadan `catalog` içindeki
  `cat` de geldi.
- `|`'nin etki alanını sınırlamak için parantez gerekir. **`(?:...)`**
  yakalamayan gruptur: yalnızca sınır çizer, `findall`'ın sonucunu
  değiştirmez. Düz parantez yazılınca `findall` yalnızca grubu (`cat`,
  `dog`) verdi, `s` kayboldu.

## Açgözlü ve tembel

```python
import re

html = "<b>bold</b> and <i>italic</i>"
print(re.findall(r"<.+>", html))
print(re.findall(r"<.+?>", html))
print(re.findall(r"<(\w+)>", html))
```

```text
['<b>bold</b> and <i>italic</i>']
['<b>', '</b>', '<i>', '</i>']
['b', 'i']
```

`+` ve `*` **açgözlüdür** (greedy): olabildiğince çok yutar. `<.+>` ilk `<`'den
**son** `>`'ye kadar her şeyi aldı. Arkalarına `?` eklenince **tembel**
(lazy) olurlar: olabildiğince az. `<.+?>` her etiketi ayrı buldu. En sağlam
yol çoğu zaman ne istediğini daraltmaktır: `<(\w+)>` yalnızca harfli açılış
etiketleri.

## Değiştirmek ve bölmek: sub, split

```python
import re

print(re.sub(r"\s+", " ", "too    many   spaces"))
text = "on 15/03/2026 and 01/04/2026"
print(re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\2-\1", text))
print(re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "3 apples, 10 pears"))
print(re.split(r"[,;]\s*", "a, b;c; d"))
print(re.sub(r"\d", "#", "card 1234-5678", count=4))
```

```text
too many spaces
on 2026-03-15 and 2026-04-01
6 apples, 20 pears
['a', 'b', 'c', 'd']
card ####-5678
```

- **`re.sub(kalıp, yeni, metin)`** her eşleşmeyi değiştirir: art arda
  boşluklar teke indi.
- Yeni metinde **`\1`, `\2`, `\3`** grupları geri koyar: gün/ay/yıl, yıl-ay-gün
  sırasına döndü. Yeni metin de `r"..."` yazılır.
- Yeni metin yerine bir **fonksiyon** verilebilir: her eşleşme nesnesiyle
  çağrılır, döndürdüğü metin konur. Burada sayılar ikiyle çarpıldı.
- **`re.split`** kalıba göre böler: virgül ya da noktalı virgül, ardından
  isteğe bağlı boşluk. `str.split` tek bir ayıraç alabilir.
- `count=4` yalnızca ilk dört eşleşmeyi değiştirdi.

## compile ve bayraklar

Aynı kalıp birçok kez kullanılacaksa **`re.compile`** ile bir kez derlenir;
kod okunaklılaşır ve kalıba ad verilmiş olur.

```python
import re

log = """2026-03-15 10:02 ERROR disk full
2026-03-15 10:05 INFO saved
2026-03-15 10:09 ERROR timeout"""
line_re = re.compile(r"^(\S+) (\S+) (ERROR|INFO) (.+)$", re.MULTILINE)
for date, time, level, message in line_re.findall(log):
    if level == "ERROR":
        print(time, message)
print(len(re.findall(r"^2026", log)))
print(len(re.findall(r"^2026", log, flags=re.MULTILINE)))
```

```text
10:02 disk full
10:09 timeout
1
3
```

- Derlenmiş kalıbın da `search`, `findall`, `sub` metotları var.
- `^` ve `$` normalde **bütün metnin** başı ve sonu. **`re.MULTILINE`** ile
  **her satırın** başı ve sonu olurlar: üç satırlık kayıtta `^2026` bir yerine
  üç kez buldu.
- Bayraklar `|` ile birleştirilir: `re.MULTILINE | re.IGNORECASE`.

## Özet

- `(...)` grup: `group(n)`, `groups()`; `(?P<ad>...)` adlı grup,
  `groupdict()`.
- Gruplu kalıpta `findall` grupları (demetleri) verir; `finditer` eşleşme
  nesnelerini.
- `a|b` ya o ya bu; `(?:...)` yakalamayan grup.
- `+ *` açgözlü, `+? *?` tembel.
- `re.sub` (yeni metinde `\1`, ya da fonksiyon), `re.split`, `count=`.
- `re.compile`; `re.MULTILINE` ile `^ $` her satırda.
