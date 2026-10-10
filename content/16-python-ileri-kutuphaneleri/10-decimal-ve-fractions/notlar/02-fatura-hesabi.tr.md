Bir faturada vergiyi **her satırda** yuvarlamak ile **toplamda bir kez**
yuvarlamak farklı sonuç verebilir. Hangisinin geçerli olduğu mevzuatta ya da
sözleşmede yazar; programın işi, kuralı tek bir yerde tutmak.

```python
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
VAT = Decimal("0.20")
lines = [("pen", "1.15", 3), ("book", "12.49", 2), ("bag", "7.33", 1)]


def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


net = sum(Decimal(price) * qty for _, price, qty in lines)
per_line = sum(money(Decimal(price) * qty * VAT) for _, price, qty in lines)
on_total = money(net * VAT)
print("net:", net)
print("tax per line:", per_line)
print("tax on total:", on_total)
print("total:", net + on_total)
```

```text
net: 35.76
tax per line: 7.16
tax on total: 7.15
total: 42.91
```

## Ne oldu?

- Satır vergileri `0.69`, `4.996` ve `1.466`. Satır satır yuvarlanınca
  `0.69 + 5.00 + 1.47 = 7.16`.
- Toplam `35.76` üzerinden bir kez hesaplanınca `7.152` → `7.15`. Bir kuruş
  fark.
- İkisi de "doğru" olabilir; yanlış olan, programın bir yerinde birini, başka
  yerinde ötekini kullanmak. Fatura ekranı 7.16, muhasebe dökümü 7.15 derse
  hesaplar tutmaz.

## İyi alışkanlıklar

- **Yuvarlama tek fonksiyonda** (`money`): kural değişirse tek satır değişir.
- **Fiyatlar metin olarak gelir** (`"1.15"`): CSV'den, formdan, veritabanından
  metin okunur ve doğrudan `Decimal`'a çevrilir; arada `float` olmaz.
- **Ara hesaplar yuvarlanmaz**, yalnızca gösterilecek ya da kaydedilecek
  sonuç yuvarlanır (kural satır başına yuvarlama demiyorsa).
- `sum()` `Decimal` listesinde de çalışır; başlangıç değeri `0` (int) sorun
  değil.
