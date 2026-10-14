# Tetikleyiciler

Şimdiye kadar yazdığımız her iş akışı `on: push` ile başladı: depoya her
gönderimde çalıştı. Gerçek projede bu çoğu zaman fazla ya da eksik olur.
Belgeleri düzelten bir commit için yirmi dakikalık test hattını
çalıştırmak boşa harcanan zamandır; buna karşılık bir pull request
birleştirilmeden **önce** test edilmelidir. Bu bölümde `on` anahtarının
alabileceği olayları ve bu olayları daraltan **süzgeçleri** (filter)
görüyoruz.

## Olay nedir?

GitHub depoda olan her şeye bir ad verir: bir gönderim `push`, bir pull
request `pull_request`, bir zamanın gelmesi `schedule`, birinin düğmeye
basması `workflow_dispatch`. İş akışının `on` bölümü "şu olaylardan biri
olunca beni çalıştır" der. `on` üç biçimde yazılabilir:

```yaml
on: push
```

```yaml
on: [push, pull_request]
```

```yaml
on:
  push:
    branches: [main]
  pull_request:
```

Üçüncü biçimde her olayın altına ayar yazılabilir. Ayarı olmayan olay
(`pull_request:`) boş bırakılır.

## push ve pull_request

İkisi en sık kullanılan olaylar ve farkları önemli:

<figure class="fig versus">
  <div><h4>push</h4>Bir dala commit gönderilince. İş akışı <b>o commit</b> üzerinde çalışır.</div>
  <div><h4>pull_request</h4>Pull request açılınca, ona yeni commit eklenince ya da yeniden açılınca. İş akışı, PR'ın hedef dalla <b>birleştirilmiş hâli</b> üzerinde çalışır.</div>
  <figcaption>pull_request birleştirmeden önce "birleşince ne olacak" sorusunu cevaplar.</figcaption>
</figure>

İkinci noktayı açalım. Senin dalın testleri geçiyor olabilir; ama sen
çalışırken `main`'e başka biri bir değişiklik eklediyse, ikisi
birleşince testler düşebilir. `pull_request` olayı GitHub'ın önceden
hazırladığı birleştirme commit'i üzerinde çalıştığı için bunu birleştirme
düğmesine basılmadan yakalar.

Çok kullanılan düzen ikisini birlikte kullanır:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

- `push` → `main`'e gelen her commit test edilir (birleştirme sonrası
  dahil).
- `pull_request` → `main`'e açılan her PR, birleştirilmeden önce test
  edilir.

Dikkat: `pull_request` altındaki `branches`, PR'ın **hedef** dalıdır
(PR'ın birleştirileceği dal), PR'ı açtığın dal değil.

Bir de **çift çalışma** tuzağı var. Süzgeçsiz `on: [push, pull_request]`
yazılırsa, açık bir PR'ın dalına commit göndermek iki olay doğurur: dala
gönderim (`push`) ve PR'a yeni commit (`pull_request`). Aynı testler iki
kez çalışır. `push`'u `main` ile sınırlamak bunu önler.

## Dal süzgeci

`branches` hangi dallarda çalışılacağını, `branches-ignore` hangi
dallarda çalışılmayacağını söyler. Aynı olayda ikisi birlikte
yazılamaz. Değerler birer **kalıptır** (pattern):

<figure class="fig anat">
  <div class="anat-row"><span><code>main</code></span><span>Yalnızca <code>main</code> dalı.</span></div>
  <div class="anat-row"><span><code>release/*</code></span><span><code>release/1.0</code> gibi, <code>release/</code> ile başlayan ve başka <code>/</code> içermeyen dallar.</span></div>
  <div class="anat-row"><span><code>release/**</code></span><span><code>release/</code> ile başlayan bütün dallar, <code>release/2026/ekim</code> dahil.</span></div>
</figure>

Kalıplardaki iki işaretin farkı şu: `*` eğik çizgi (`/`) dışında her
şeye uyar, `**` eğik çizgi dahil her şeye. Bu kuralı küçük bir Python
fonksiyonuyla taklit edelim. Fonksiyon kalıbı düzenli ifadeye çeviriyor:
`**` → `.*`, `*` → `[^/]*` ("eğik çizgi olmayan herhangi bir şey"):

```python
import re


def matches(pattern, path):
    regex = ""
    i = 0
    while i < len(pattern):
        if pattern[i:i + 2] == "**":
            regex += ".*"
            i += 2
        elif pattern[i] == "*":
            regex += "[^/]*"
            i += 1
        else:
            regex += re.escape(pattern[i])
            i += 1
    return re.fullmatch(regex, path) is not None


for pattern, path in [("release/*", "release/1.0"),
                      ("release/*", "release/2026/oct"),
                      ("release/**", "release/2026/oct"),
                      ("*.md", "README.md"),
                      ("*.md", "docs/guide.md"),
                      ("**.md", "docs/guide.md"),
                      ("docs/**", "docs/img/logo.png")]:
    print(f"{pattern:<11} {path:<18} {matches(pattern, path)}")
```

```text
release/*   release/1.0        True
release/*   release/2026/oct   False
release/**  release/2026/oct   True
*.md        README.md          True
*.md        docs/guide.md      False
**.md       docs/guide.md      True
docs/**     docs/img/logo.png  True
```

En çok şaşırtan satır `*.md`: yalnızca deponun **kökündeki** `.md`
dosyalarına uyar, `docs/guide.md`'ye uymaz. Her klasördeki `.md`
dosyaları için `**.md` yazılır.

Bu fonksiyon basitleştirilmiş bir model. GitHub'ın kalıplarında birkaç
işaret daha var (`?`, `[]`, başta `!` ile "hariç tut"); ama günlük işin
çoğu `*` ve `**` ile görülür.

## Yol süzgeci

`paths`, "yalnızca şu dosyalardan biri değiştiyse çalış" der;
`paths-ignore` "değişen dosyaların **hepsi** bunlardansa çalışma".
Belgeler için test hattını çalıştırmamanın yolu budur:

```yaml
on:
  push:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "**.md"
```

Dal ve yol süzgeci birlikte yazılırsa **iki şart da** tutmalı. GitHub'ın
verdiği kararı Python'la yazalım. Yukarıdaki `matches` fonksiyonunu
kullanıyoruz:

```python
def would_run(branch, changed, branches, ignored):
    if not any(matches(pattern, branch) for pattern in branches):
        return False
    for path in changed:
        if not any(matches(pattern, path) for pattern in ignored):
            return True
    return False


ignored = ["docs/**", "**.md"]
print(would_run("main", ["docs/setup.md"], ["main"], ignored))
print(would_run("main", ["README.md", "app/core.py"], ["main"], ignored))
print(would_run("feature/login", ["app/core.py"], ["main"], ignored))
```

```text
False
True
False
```

1. Yalnızca belge değişti → çalışmaz.
2. Bir belge ve bir kod dosyası değişti → çalışır: değişenlerin hepsi
   yoksayılanlardan değil.
3. Kod değişti ama dal `main` değil → çalışmaz.

## Etiketler

Sürüm çıkarırken commit'e `v1.2.0` gibi bir **etiket** (tag) konur (Git
patikasında gördük). Etiketin gönderilmesi de bir `push` olayıdır ve
`tags` süzgeciyle yakalanır:

```yaml
on:
  push:
    tags: ["v*"]
```

Bir tuzak: bir olayda yalnızca `tags` yazılırsa, dala yapılan gönderimler
artık o iş akışını **başlatmaz**; yalnızca `branches` yazılırsa da etiket
gönderimleri başlatmaz. İkisi isteniyorsa ikisi birden yazılır. Sürüm
çıkaran iş akışlarını sekizinci bölümde göreceğiz.

## Zamanlanmış çalışma

`schedule` iş akışını takvime bağlar. Zaman bir **cron** ifadesiyle
yazılır: boşlukla ayrılmış beş alan.

<figure class="fig anat">
  <div class="anat-row"><span>1. dakika</span><span>0–59</span></div>
  <div class="anat-row"><span>2. saat</span><span>0–23</span></div>
  <div class="anat-row"><span>3. ayın günü</span><span>1–31</span></div>
  <div class="anat-row"><span>4. ay</span><span>1–12</span></div>
  <div class="anat-row"><span>5. haftanın günü</span><span>0–6, <b>0 = Pazar</b>, 1 = Pazartesi</span></div>
</figure>

`*` "her değer" demek. `30 2 * * 1` → her Pazartesi 02:30. Saat her zaman
**UTC**'dir; Türkiye saati UTC'den 3 saat ileridir. Bir cron ifadesinin
ne zaman çalışacağını hesaplayalım. Kısa olsun diye yalnızca `*`, sayı ve
virgüllü liste (`1,3,5`) tanıyan bir eşleştirici yazıyoruz:

```python
from datetime import datetime, timedelta


def field_ok(field, value):
    return field == "*" or str(value) in field.split(",")


def next_runs(cron, start, count):
    minute, hour, day, month, weekday = cron.split()
    runs = []
    moment = start
    while len(runs) < count:
        moment += timedelta(minutes=1)
        cron_weekday = (moment.weekday() + 1) % 7
        if (field_ok(minute, moment.minute) and field_ok(hour, moment.hour)
                and field_ok(day, moment.day) and field_ok(month, moment.month)
                and field_ok(weekday, cron_weekday)):
            runs.append(moment)
    return runs


start = datetime(2026, 10, 14, 12, 0)
for run in next_runs("30 2 * * 1", start, 3):
    turkey = run + timedelta(hours=3)
    print("UTC", run.strftime("%Y-%m-%d %H:%M"), "| TR", turkey.strftime("%H:%M"))
```

```text
UTC 2026-10-19 02:30 | TR 05:30
UTC 2026-10-26 02:30 | TR 05:30
UTC 2026-11-02 02:30 | TR 05:30
```

İki ayrıntı:

- Python'un `weekday()`'i Pazartesi'yi 0 sayar, cron Pazar'ı 0 sayar.
  `(weekday() + 1) % 7` bu kaymayı düzeltiyor.
- 02:30 UTC Türkiye'de 05:30'dur. "Her sabah 06:00'da" isteniyorsa cron'a
  `0 3 * * *` yazılır.

GitHub'ın zamanlanmış çalışmalarında bilinmesi gerekenler:

- Zamanlama yalnızca **varsayılan daldaki** (çoğu zaman `main`) iş akışı
  dosyasından okunur.
- En sık 5 dakikada bir çalışabilir.
- GitHub yoğunken çalışma gecikebilir; en yoğun an saat başlarıdır.
  `0` yerine `17` gibi bir dakika seçmek gecikmeyi azaltır.
- Herkese açık bir depoda 60 gün hiçbir etkinlik olmazsa zamanlanmış iş
  akışları kendiliğinden kapatılır.

Ne için kullanılır? Gece tüm testleri (hızlılar her gönderimde, yavaşlar
gecede), bağımlılıkların yeni sürümleriyle deneme, haftalık rapor.

## Elle başlatma

`workflow_dispatch` olayı iş akışına GitHub'ın Actions sekmesinde bir
**Run workflow** düğmesi ekler. Zamanlanmış bir iş akışını beklemeden
denemek ya da bir dağıtımı elle başlatmak için kullanılır. Düğmeye
basınca sorulacak **girdiler** (inputs) de tanımlanabilir:

```yaml
on:
  workflow_dispatch:
    inputs:
      level:
        description: "How many tests to run"
        type: choice
        options: [quick, full]
        default: quick
```

Girdi iş akışının içinde `${{ inputs.level }}` ile okunur. Düğme de
yalnızca varsayılan daldaki dosyada `workflow_dispatch` varsa görünür.

## Çalışmayı atlamak

Bir commit mesajına `[skip ci]` yazılırsa, o gönderimin başlatacağı
`push` ve `pull_request` çalışmaları atlanır. Yalnızca yazım hatası
düzelten bir commit için işe yarar; ama alışkanlık hâline gelirse test
edilmemiş kod `main`'e girer. Belgeler için `paths-ignore` daha güvenli
bir yol.

## Hepsi bir arada

```yaml
name: CI

on:
  push:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "**.md"
  pull_request:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "**.md"
  schedule:
    - cron: "17 3 * * *"
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

Bu iş akışı `main`'e gelen kod değişikliklerinde, `main`'e açılan
PR'larda, her gece 03:17 UTC'de (Türkiye'de 06:17) ve istenince elle
çalışır; yalnızca belge değişirse çalışmaz.

## Özet

- `on` olayları sayar: `push`, `pull_request`, `schedule`,
  `workflow_dispatch`...
- `pull_request` birleştirilmiş hâli test eder; altındaki `branches`
  hedef daldır. `push`'u `main` ile sınırlamak çift çalışmayı önler.
- Kalıplarda `*` eğik çizgiye uymaz, `**` uyar. `*.md` yalnızca kökteki
  dosyalar.
- `paths-ignore`: değişenlerin hepsi yoksayılanlardansa çalışmaz. Dal ve
  yol süzgeci birlikte: iki şart da tutmalı.
- `tags: ["v*"]` etiket gönderimini yakalar; yalnızca `tags` yazılırsa
  dal gönderimleri başlatmaz.
- cron beş alan, saat **UTC**, haftanın günü 0 = Pazar.
- `workflow_dispatch` elle başlatma düğmesi ve girdiler.
