# Yedek ve Felaket Kurtarma

Güvenlik Nedir? CIA Üçlüsü bölümünde güvenliğin üç ayağından birinin
**erişilebilirlik** olduğunu gördük: veri ve sistem, gerektiğinde
kullanılabilir olmalı. Bir diskin bozulması, yanlışlıkla silinen bir
tablo, fidye yazılımının şifrelediği bir sunucu ya da bir binayı etkileyen
bir yangın; hepsinin karşısındaki son savunma aynıdır: **yedek** ve onu
geri yükleyebilme becerisi.

Bu bölüm iyi bir yedeğin kurallarını, "ne kadar veri kaybedebiliriz,
ne kadar sürede dönebiliriz" sorularını ve yedeğin gerçekten çalıştığını
nasıl bileceğimizi anlatıyor. Bütün yedekler, tarihler ve dosyalar sahte.

## 3-2-1 kuralı

Yaygın bir başlangıç kuralı: verinin en az **3** kopyası olsun, bunlar en
az **2** farklı ortamda dursun ve en az **1** tanesi başka bir yerde (bina
dışında) olsun:

```python
COPIES = [
    {"name": "live", "media": "ssd", "offsite": False},
    {"name": "nas", "media": "hdd", "offsite": False},
    {"name": "cloud", "media": "object-storage", "offsite": True},
]
media = {c["media"] for c in COPIES}
offsite = sum(c["offsite"] for c in COPIES)
print("copies:", len(COPIES), "ok" if len(COPIES) >= 3 else "too few")
print("media:", len(media), "ok" if len(media) >= 2 else "too few")
print("offsite:", offsite, "ok" if offsite >= 1 else "missing")
```

```text
copies: 3 ok
media: 3 ok
offsite: 1 ok
```

Üç kopya, üç farklı ortam, biri dışarıda: kural tutuyor. Farklı ortam, aynı
türden bir arızanın (aynı seri disklerin aynı anda bozulması) bütün
kopyaları birden götürmesini; dışarıdaki kopya ise yangın ya da hırsızlık
gibi bütün binayı etkileyen bir olayı önler.

**Fidye yazılımı** bu kurala bir şart ekletti: yedeklerden en az biri
**çevrimdışı** ya da **değiştirilemez** (immutable) olmalıdır. Ağdan
ulaşılabilen bir yedek, sistemi şifreleyen saldırgan tarafından da
şifrelenebilir ya da silinebilir.

## RPO: ne kadar veri kaybedebiliriz?

**RPO** (Recovery Point Objective, kurtarma noktası hedefi), bir felakette
kabul edilebilecek en uzun veri kaybıdır. En kötü durumda kaybedilen
veri, iki yedek arasındaki en uzun **boşluk** kadardır:

```python
from datetime import datetime

BACKUPS = [
    "2026-11-01T00:00",
    "2026-11-01T06:00",
    "2026-11-01T12:00",
    "2026-11-02T00:00",
]
times = [datetime.fromisoformat(t) for t in BACKUPS]
gaps = [(b - a).total_seconds() / 3600 for a, b in zip(times, times[1:])]
print("gaps (hours):", gaps)
print("worst-case data loss:", max(gaps), "hours")
print("meets RPO of 8 hours:", max(gaps) <= 8)
```

```text
gaps (hours): [6.0, 6.0, 12.0]
worst-case data loss: 12.0 hours
meets RPO of 8 hours: False
```

Gündüz altı saatte bir yedek alınıyor ama öğleden gece yarısına kadar
12 saat boşluk var. Hedef 8 saatse bu düzen hedefi tutmuyor:
o aralıkta bir felaket olsa yarım günlük veri kaybolur.

## RTO: ne kadar sürede döneriz?

**RTO** (Recovery Time Objective, kurtarma süresi hedefi), bir felaketten
sonra sistemin en geç ne zaman yeniden çalışması gerektiğidir. Geri
yüklemenin süresi, verinin boyuna ve geri yükleme hızına bağlıdır:

```python
size_gb = 900
speed_gb_per_hour = 150
setup_hours = 1.5
restore_hours = setup_hours + size_gb / speed_gb_per_hour
print("estimated restore:", restore_hours, "hours")
print("meets RTO of 6 hours:", restore_hours <= 6)
```

```text
estimated restore: 7.5 hours
meets RTO of 6 hours: False
```

Verinin kendisi 6 saatte geri geliyor ama hazırlık
(donanımı bulmak, sistemi kurmak) eklenince 7,5 saat ediyor:
6 saatlik hedef tutmuyor. RPO ve RTO hedefleri iş birimleriyle birlikte
belirlenir; daha kısa hedef daha pahalı bir yedek düzeni demektir.

## Denenmemiş yedek, yedek değildir

Bir yedeğin gerçekten işe yaradığını bilmenin tek yolu onu **geri
yüklemeyi denemektir**. Geri yüklenen dosyalar asıllarıyla karşılaştırılır:

```python
import hashlib


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


ORIGINAL = {
    "orders.csv": "1,ada,30\n2,bob,45\n",
    "users.csv": "ada\nbob\n",
    "keys.txt": "k1\n",
}
RESTORED = {
    "orders.csv": "1,ada,30\n2,bob,45\n",
    "users.csv": "ada\n",
}
for name in sorted(ORIGINAL):
    if name not in RESTORED:
        print(name, "missing")
    elif digest(RESTORED[name]) != digest(ORIGINAL[name]):
        print(name, "different")
    else:
        print(name, "ok")
```

```text
keys.txt missing
orders.csv ok
users.csv different
```

Üç dosyadan yalnızca biri sağlam döndü: biri eksik, biri yarım. Bu deneme
yapılmasaydı sorun, gerçek bir felakette, yedeğe en çok ihtiyaç duyulan
anda ortaya çıkacaktı. Geri yükleme denemeleri bu yüzden düzenli ve
takvimli yapılır.

## Ne kadar saklanır?

Her yedeği sonsuza kadar saklamak hem pahalıdır hem de gereksizdir. Yaygın
bir düzen **dede-baba-oğul** (grandfather-father-son) yöntemidir: son
günlerin günlük yedekleri, son haftaların haftalık yedekleri ve ayların
aylık yedekleri saklanır:

```python
from datetime import date, timedelta

TODAY = date(2026, 11, 1)
backups = [TODAY - timedelta(days=i) for i in range(60)]
daily = {d for d in backups if (TODAY - d).days < 7}
weekly = {d for d in backups if d.weekday() == 6 and (TODAY - d).days < 28}
monthly = {d for d in backups if d.day == 1}
keep = daily | weekly | monthly
print(len(backups), "backups,", len(keep), "kept")
print(sorted(d.isoformat() for d in keep - daily))
```

```text
60 backups, 11 kept
['2026-10-01', '2026-10-11', '2026-10-18', '2026-10-25']
```

60 günlük yedekten 11 tanesi kalıyor: son haftanın her günü,
daha eski Pazarlar ve ayın ilk günleri. Fidye yazılımı ya da sessiz bir
bozulma haftalar sonra fark edilirse, eski ama temiz bir yedek hâlâ
yerindedir.

## Felaket kurtarma planı

Yedek bir parçadır; **felaket kurtarma planı** (disaster recovery plan)
bütünü anlatır: hangi sistemler önce geri gelir, kim neyi yapar, yedekler
nerede, hangi parolalar ve belgeler gerekir (ve onlar felakette nereden
bulunur). Plan da yedek gibi düzenli **tatbikatla** sınanır.

## Özet

- **3-2-1:** üç kopya, iki farklı ortam, biri dışarıda; en az biri
  çevrimdışı ya da değiştirilemez.
- **RPO:** kabul edilebilir veri kaybı; en kötü durum, yedekler arasındaki
  en uzun boşluktur.
- **RTO:** kabul edilebilir kesinti süresi; geri yükleme süresi hazırlıkla
  birlikte hesaplanır.
- **Denenmemiş yedek, yedek değildir:** geri yükleme düzenli denenir ve
  asılla karşılaştırılır.
- **Saklama:** dede-baba-oğul gibi bir düzenle eski ama temiz yedekler de
  tutulur.
- **Felaket kurtarma planı** bütünü anlatır ve tatbikatla sınanır.
