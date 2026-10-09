`timedelta` gün sayar; ay ve yıl saymaz. Takvimle ilgili iki sık iş için
küçük fonksiyonlar gerekiyor.

## Ay eklemek

31 Ocak'a bir ay eklenince ne olmalı? 31 Şubat yok; yaygın kural ayın son
gününe inmek. Ayın kaç gün çektiğini `calendar.monthrange(yıl, ay)` verir
(ikinci değer).

```python
import calendar
from datetime import date


def add_months(d, n):
    month_index = d.month - 1 + n
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    last = calendar.monthrange(year, month)[1]
    return date(year, month, min(d.day, last))


print(add_months(date(2026, 1, 31), 1))
print(add_months(date(2028, 1, 31), 1))
print(add_months(date(2026, 11, 15), 3))
print(add_months(date(2026, 3, 31), -1))
print(calendar.isleap(2026), calendar.isleap(2028))
print(calendar.monthrange(2026, 2)[1])
```

```text
2026-02-28
2028-02-29
2027-02-15
2026-02-28
False True
28
```

- Ayları 0'dan sayınca (`month_index`) yıl taşması `// 12`, yeni ay `% 12`
  ile bulunur; negatif `n` de çalışır (Mart'tan bir ay geri Şubat).
- 2028 artık yıl: 31 Ocak + 1 ay = 29 Şubat.
- 15 Kasım + 3 ay bir sonraki yılın 15 Şubat'ı.

## Yaş hesaplamak

```python
from datetime import date


def age(birth, today):
    years = today.year - birth.year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1
    return years


print(age(date(2000, 5, 20), date(2026, 5, 19)))
print(age(date(2000, 5, 20), date(2026, 5, 20)))
print((date(2026, 5, 19) - date(2000, 5, 20)).days // 365)
print((date(2026, 5, 19) - date(2000, 5, 20)).days / 365.25)
```

```text
25
26
26
25.9958932238193
```

Doğum gününden bir gün önce kişi 25 yaşında, doğum gününde 26. Yıl farkından
bir çıkarmak gerekip gerekmediğini `(ay, gün)` demetlerini karşılaştırarak
anlıyoruz: demetler önce ilk elemana, eşitse ikinciye göre karşılaştırılır.

Gün farkını 365'e bölmek **yanlış** sonuç verdi (26): aradaki artık yılların
fazladan günleri birikip bir gün öne geçiriyor. 365,25'e bölmek de tam sayı
vermiyor. Takvimle ilgili hesapta günleri bölmek yerine takvimin kendi
parçalarıyla (yıl, ay, gün) hesap yapılır.
