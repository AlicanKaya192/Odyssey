Bilgi çıkarma kuralları büyüdükçe tek satırlık düzenli ifadeler okunmaz
hâle gelir. Üç alışkanlık işi kolaylaştırır.

## Adlı gruplar ve açıklamalı yazım

```python
import re

AMOUNT = re.compile(r"""
    \$                          # dolar işareti
    (?P<whole>\d{1,3}(?:,\d{3})*)  # binlik ayraçlı tam kısım
    (?:\.(?P<cents>\d{2}))?     # isteğe bağlı kuruş
""", re.VERBOSE)

for match in AMOUNT.finditer("Paid $1,200.00, refunded $5."):
    parts = match.groupdict()
    value = int(parts["whole"].replace(",", "")) + int(parts["cents"] or 0) / 100
    print(match.group(), parts, value)
```

```text
$1,200.00 {'whole': '1,200', 'cents': '00'} 1200.0
$5 {'whole': '5', 'cents': None} 5.0
```

- `re.VERBOSE` boşlukları ve `#` sonrasını yok sayar: kuralı parça parça,
  açıklamalı yazabilirsin. (İfadede gerçek bir boşluk gerekiyorsa `\ `
  ya da `\s` yazılır.)
- `(?P<ad>...)` **adlı grup**: eşleşmenin parçasına numarayla değil adla
  ulaşırsın (`groupdict()`). Eşleşmeyen isteğe bağlı grup `None` olur; bu
  yüzden `parts["cents"] or 0`.
- `(?:...)` **yakalamayan grup**: yalnızca gruplamak için. `re.findall`
  yakalayan grup görünce bütün eşleşme yerine grubu döndürür; derste tutar
  kuralında bu yüzden `(?:...)` kullandık.

## Açgözlü ve tembel

```python
html = "<b>late</b> and <i>damaged</i>"
print(re.findall(r"<.*>", html))
print(re.findall(r"<.*?>", html))
```

```text
['<b>late</b> and <i>damaged</i>']
['<b>', '</b>', '<i>', '</i>']
```

`.*` **açgözlü** (greedy): olabildiğince uzun eşleşir, ilk `<`'den son `>`'ye
kadar her şeyi yutar. `.*?` **tembel** (lazy): olabildiğince kısa eşleşir.
Etiket, tırnak ya da parantez arasını çekerken neredeyse her zaman tembel
olan gerekir (ya da `<[^>]*>` gibi "kapanış dışında her şey").

## Kuralları test et

Her kuralın yanında birkaç örnek dur: eşleşmesi gerekenler ve
**eşleşmemesi** gerekenler. Dersteki altın standart bunun küçük bir
hâliydi. Bir kuralı genişlettiğinde eski örneklerin hâlâ doğru çalıştığını
görmek, düzenli ifadelerdeki en sık hatayı (bir şeyi düzeltirken başka bir
şeyi bozmak) yakalar.
