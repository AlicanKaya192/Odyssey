# decimal ve fractions

Python'da `0.1 + 0.2` tam olarak `0.3` etmez. Bu bir hata değil, `float`
türünün sayıları bilgisayarda nasıl sakladığının sonucu. Bilimsel hesapta ve
makine öğrenmesinde bu küçük fark sorun olmaz; ama **para** hesabında bir
kuruşun bile kaybolmaması gerekir. Bu bölüm iki standart kütüphane modülünü
anlatıyor: ondalık sayıları **tam** tutan `decimal` ve kesirleri tam tutan
`fractions`.

## float neden şaşırtır?

```python
from decimal import Decimal

print(0.1 + 0.2, 0.1 + 0.2 == 0.3)
print(Decimal(0.1))
print(round(2.675, 2))
print(round(0.5), round(1.5), round(2.5))
```

```text
0.30000000000000004 False
0.1000000000000000055511151231257827021181583404541015625
2.67
0 2 2
```

- `float` sayıyı **ikili** (binary) kesir olarak saklar. `0.1` ikili tabanda
  sonsuz devreden bir kesir (onluk tabanda 1/3'ün `0.333...` olması gibi);
  bellekte ona en yakın sayı duruyor. `Decimal(0.1)` o sayının gerçek
  değerini gösteriyor.
- Bu yüzden `0.1 + 0.2` küçük bir artıkla çıkıyor ve `==` yanlış veriyor.
- `round(2.675, 2)` `2.68` değil `2.67`: bellekteki `2.675` aslında biraz
  küçük.
- `round` yarımları **en yakın çifte** yuvarlıyor (banker yuvarlaması):
  `0.5` → `0`, `2.5` → `2`. Okulda öğrenilen "beş yukarı" kuralı değil.

## Decimal: onluk tabanda tam sayılar

```python
from decimal import Decimal, InvalidOperation

total = Decimal("0.1") + Decimal("0.2")
print(total, total == Decimal("0.3"))
print(Decimal("1.10") + Decimal("2.20"), Decimal("19.99") * 3)
try:
    Decimal("1.5") + 1.5
except TypeError as error:
    print("TypeError:", error)
try:
    Decimal("abc")
except InvalidOperation:
    print("InvalidOperation")
```

```text
0.3 True
3.30 59.97
TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'
InvalidOperation
```

- `Decimal` sayıyı **onluk** tabanda saklar; `0.1` gerçekten `0.1`'dir.
- **Metinden kur:** `Decimal("0.1")`. `Decimal(0.1)` yazarsan float'ın hatalı
  değeri olduğu gibi kopyalanır (yukarıdaki uzun sayı).
- Sondaki sıfırlar korunur: `1.10 + 2.20` → `3.30`. Para için doğal.
- `Decimal` ile `int` karışabilir (`* 3`), `float` ile **karışmaz**:
  `TypeError`. Bu bilinçli; hatalı float'ın sessizce girmesini önlüyor.
- Okunamayan metin `InvalidOperation` verir.

## quantize: basamağa yuvarlamak

```python
from decimal import Decimal, ROUND_HALF_UP

cent = Decimal("0.01")
print(Decimal("2.675").quantize(cent))
half = Decimal("2.665")
print(half.quantize(cent), half.quantize(cent, rounding=ROUND_HALF_UP))
print(Decimal("100.00").quantize(Decimal("1")))
print(f"{Decimal('1234.5'):,.2f}")
```

```text
2.68
2.66 2.67
100
1,234.50
```

- **`quantize(Decimal("0.01"))`** sayıyı verilen örneğin basamağına (iki
  ondalık) yuvarlar. Burada `2.675` gerçekten `2.675` olduğu için `2.68`
  çıkıyor; float'ta `2.67` çıkmıştı.
- Varsayılan kural `ROUND_HALF_EVEN` (yarımda çift olana): `2.675` → `2.68`
  ama `2.665` → `2.66`. Çok sayıda yuvarlamada hatalar birbirini götürsün
  diye bankacılıkta yaygın.
- **`rounding=ROUND_HALF_UP`** okuldaki "beş yukarı" kuralı: `2.665` →
  `2.67`. Faturada, vergide hangi kural geçerliyse o yazılır; sözleşmede ya
  da mevzuatta belirtilir.
- f-string biçimleri `Decimal` ile de çalışır: binlik ayırıcı ve iki ondalık.

## Duyarlık: bağlam (context)

```python
from decimal import Decimal, getcontext, localcontext

print(getcontext().prec)
print(Decimal(1) / Decimal(3))
with localcontext() as ctx:
    ctx.prec = 5
    print(Decimal(1) / Decimal(3))
print(Decimal(10) / Decimal(3))
```

```text
28
0.3333333333333333333333333333
0.33333
3.333333333333333333333333333
```

- `Decimal` sonsuz basamak tutamaz; bölmede kaç **anlamlı basamak**
  hesaplanacağını bağlam belirler. Varsayılan `prec` 28.
- **`localcontext()`** yalnızca `with` bloğunun içinde geçerli bir bağlam
  açar; blok bitince eski ayar geri gelir. `getcontext().prec = 5` yazmak
  bütün programı etkiler; kütüphane kodunda yapılmaz.
- `prec` ondalık basamak değil, **toplam** anlamlı basamak sayısı. Kuruşa
  yuvarlamak için `quantize` kullanılır.

## Parayı bölmek: kayıp kuruş

```python
from decimal import Decimal, ROUND_DOWN

total = Decimal("100.00")
share = (total / 3).quantize(Decimal("0.01"))
print(share, share * 3)
base = (total / 3).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
rest = total - base * 3
cents = int(rest / Decimal("0.01"))
parts = [base + Decimal("0.01") if i < cents else base for i in range(3)]
print(parts, sum(parts))
```

```text
33.33 99.99
[Decimal('33.34'), Decimal('33.33'), Decimal('33.33')] 100.00
```

- 100 lira üçe bölünüp kuruşa yuvarlanınca `33.33 × 3 = 99.99`: bir kuruş
  kayboldu. `Decimal` tam hesap yapıyor ama yuvarlama yine de bilgi atıyor.
- Doğrusu: payları **aşağı** yuvarla (`ROUND_DOWN`), kalanı (`0.01`) say ve
  ilk paylara birer kuruş dağıt. Toplam her zaman tam tutar.
- Bu, taksitlendirmede ve hesap bölüşmede gerçek programların yaptığı iş.

## Fraction: tam kesirler

```python
from fractions import Fraction

print(Fraction(1, 3) + Fraction(1, 6))
print(Fraction(6, 8), Fraction("0.75"))
f = Fraction(3, 4)
print(f.numerator, f.denominator, float(f))
print(Fraction(0.1))
print(Fraction(0.1).limit_denominator(100))
```

```text
1/2
3/4 3/4
3 4 0.75
3602879701896397/36028797018963968
1/10
```

- `Fraction(pay, payda)` kesri tam tutar ve **kendiliğinden sadeleştirir**:
  `6/8` → `3/4`. `1/3 + 1/6` tam olarak `1/2`.
- Metinden de kurulur: `Fraction("0.75")`.
- `numerator` (pay) ve `denominator` (payda) özellikleri; `float(f)` ondalığa
  çevirir.
- Float'tan kurulan kesir float'ın gerçek (ikili) değerini taşır: devasa bir
  kesir. `limit_denominator(100)` paydası en fazla 100 olan en yakın kesri
  bulur: `1/10`.
- Olasılık, oran, müzikte ritim, tarifte ölçü gibi sonucun kesir olarak tam
  kalması gereken yerlerde kullanılır. Odyssey'nin matematik problemleri de
  cevapları `Fraction` ile karşılaştırıyor (`1/2` = `0.5`).

## Hangisi ne zaman?

| Tür | Ne için | Dikkat |
|---|---|---|
| `float` | bilim, ölçüm, ML, grafik | hızlı; `==` yerine `math.isclose` |
| `Decimal` | para, fatura, vergi | metinden kur; `quantize` + yuvarlama kuralı |
| `Fraction` | tam oranlar, kesirli sonuç | payda büyüyebilir, yavaşlar |
| `int` | kuruş cinsinden tutar | `1999` kuruş = 19,99 lira; bölmede dikkat |

Float'larla karşılaştırma gerekirse `math.isclose(0.1 + 0.2, 0.3)` → `True`.
Veritabanında para çoğu zaman `DECIMAL(10, 2)` sütununda ya da kuruş cinsinden
tam sayı olarak saklanır.

## Özet

- `float` ikili tabanda yaklaşık; `0.1 + 0.2 != 0.3`, `round` yarımda çifte.
- `Decimal("...")` metinden kurulur, onluk tabanda tam; float ile karışmaz.
- `quantize(Decimal("0.01"), rounding=...)` kuruşa yuvarlar; kuralı sen seç.
- `localcontext()` ile geçici duyarlık; `prec` anlamlı basamak sayısı.
- Para bölerken kalanı dağıt; toplam tutmalı.
- `Fraction` kesirleri tam ve sade tutar; `limit_denominator` float'ı kesre
  yaklaştırır.
