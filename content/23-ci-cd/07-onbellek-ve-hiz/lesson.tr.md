# Önbellek ve Hız

Hat ne kadar yavaşsa o kadar az çalıştırılır ve geliştirici sonucu
beklerken başka işe geçer; geri bildirim gecikir. Her iş temiz bir
makinede başladığı için en çok zaman **her seferinde baştan yapılan**
işlere gider: Python'u kurmak, paketleri indirmek. Bu bölümde
**önbellek** (cache) ile tekrar eden işi atlamayı, eski çalışmaları
iptal etmeyi ve hattı hızlandırmanın öbür yollarını görüyoruz.

## Zaman nereye gidiyor?

Tipik bir test işinin adımları:

1. Makineyi hazırlamak ve kodu çekmek.
2. Python'u kurmak.
3. Bağımlılıkları indirip kurmak (`pip install`).
4. Testleri çalıştırmak.

Üçüncü adım çoğu zaman en uzunudur ve her çalıştırmada **aynı** paketleri
aynı yerden indirir. `requirements.txt` değişmediyse sonucu da
değişmez: bir önceki çalıştırmanın indirdiklerini saklayıp yeniden
kullanmak mümkün.

## Önbellek nasıl çalışır?

`actions/cache` eylemi bir klasörü bir **anahtarla** (key) saklar:

```yaml
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            pip-${{ runner.os }}-
```

- **Adım çalışınca** bu anahtarla saklanmış bir önbellek arar. Bulursa
  `path` klasörünü geri yükler.
- **İş başarıyla bitince**, anahtar ilk kez kullanılıyorsa klasörü o
  anahtarla saklar.
- `~/.cache/pip`, pip'in indirdiği paketleri tuttuğu klasör (Linux'ta).
  Önbellek doluysa `pip install` paketleri internetten değil oradan
  alır.

Önbellek adımı kurulumdan **önce** gelmeli; geri yüklenen klasör ancak
ondan sonraki adımlarda işe yarar.

## Anahtarı içerikten üretmek

Anahtarın en önemli kuralı: **saklanan şey değişince anahtar da
değişmeli.** Yoksa eski paketler sonsuza kadar geri yüklenir.
`hashFiles('requirements.txt')` dosyanın içeriğinden bir **özet** (hash)
üretir; içerik aynıysa özet aynı, bir harf değişse bambaşka. GitHub bunun
için SHA-256 kullanıyor. Aynı fikri Python'la görelim:

```python
import hashlib


def cache_key(runner_os, requirements):
    digest = hashlib.sha256(requirements.encode()).hexdigest()
    return "pip-" + runner_os + "-" + digest[:12]


before = "pytest==8.4.2\nrequests==2.32.5\n"
after = "pytest==8.4.2\nrequests==2.32.6\n"
print(cache_key("Linux", before))
print(cache_key("Linux", before))
print(cache_key("Linux", after))
print(cache_key("Windows", before))
```

```text
pip-Linux-74c0ae9e3910
pip-Linux-74c0ae9e3910
pip-Linux-84b35b85d419
pip-Windows-74c0ae9e3910
```

- Aynı içerik → aynı anahtar: ikinci çalıştırma önbelleği bulur.
- Tek bir sürüm numarası değişti → yeni anahtar: eski paketler
  kullanılmaz.
- İşletim sistemi de anahtarda: Windows'ta indirilen paketler Linux'a
  uymaz, karışmamalı. `runner.os` iş akışında makinenin işletim
  sistemidir (`Linux`, `Windows`, `macOS`).

## restore-keys: yarım eşleşme

`requirements.txt`'te tek satır değişince tam anahtar tutmaz ve önbellek
bütünüyle boşa gider; oysa paketlerin çoğu aynı. `restore-keys` bir yedek
**önek** listesidir: tam anahtar bulunamazsa, sırayla her önekle başlayan
önbelleklerin **en yenisi** geri yüklenir. pip yalnızca eksik paketleri
indirir. Kuralı Python'la yazalım (`saved` en eskiden en yeniye):

```python
def restore(key, restore_keys, saved):
    if key in saved:
        return "hit: " + key
    for prefix in restore_keys:
        found = [name for name in saved if name.startswith(prefix)]
        if found:
            return "partial: " + found[-1]
    return "miss"


saved = ["pip-Linux-1a2b", "pip-Windows-9f8e", "pip-Linux-3c4d"]
print(restore("pip-Linux-3c4d", ["pip-Linux-"], saved))
print(restore("pip-Linux-5e6f", ["pip-Linux-"], saved))
print(restore("pip-macOS-7a8b", ["pip-macOS-"], saved))
```

```text
hit: pip-Linux-3c4d
partial: pip-Linux-3c4d
miss
```

1. Tam anahtar var → **hit**.
2. Tam anahtar yok, önek tuttu → en yeni Linux önbelleği (**partial**).
   Kısmi geri yüklemede iş sonunda yeni anahtarla yeni bir önbellek
   saklanır.
3. Hiçbiri yok → **miss**: her şey indirilir.

## Daha kısası: setup-python'un kendi önbelleği

pip önbelleği o kadar yaygın ki `actions/setup-python` bunu kendisi
yapabiliyor:

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
          cache: pip
```

Anahtarı `requirements.txt`'nin özetinden kendisi üretir. Bağımlılıklar
başka bir dosyadaysa `cache-dependency-path` ile gösterilir. Basit
projelerde ayrı bir `actions/cache` adımına gerek kalmaz.

## Önbelleğin sınırları

- Bir deponun önbellekleri varsayılan olarak toplam **10 GB**. Dolunca en
  uzun süre kullanılmayanlar silinir; 7 gün hiç kullanılmayan önbellek de
  silinir.
- Önbellek **dala bağlıdır**: bir dalda saklanan önbelleği o dal ve
  varsayılan dal (`main`) kullanır; bir pull request, birleştirileceği
  dalın önbelleğini de okuyabilir. Kardeş dallar birbirininkini görmez.
- Önbelleğe **gizli değer koyma**: pull request'lerden okunabilir.
- Önbellek bir hızlandırmadır, garanti değil. Önbellek boşken de iş
  doğru çalışmalı.

## Eski çalışmaları iptal etmek

Bir dala art arda üç commit gönderdin. Üç çalışma başlar; ama yalnızca
sonuncusunun sonucu önemli. **concurrency** (eşzamanlılık) aynı
gruptaki çalışmaların ancak birinin sürmesine izin verir;
`cancel-in-progress: true` yenisi gelince eskisini iptal eder:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Grup adı iş akışı + dal: farklı dallar birbirini iptal etmez. Ne kadar
kazandırdığını bir modelle görelim: her çalışma 10 dakika, gönderimler
0., 3. ve 5. dakikada.

```python
def machine_minutes(pushes, duration, cancel):
    total = 0
    for i, start in enumerate(pushes):
        end = start + duration
        if cancel and i + 1 < len(pushes):
            end = min(end, pushes[i + 1])
        total += end - start
    return total


pushes = [0, 3, 5]
print("without cancel:", machine_minutes(pushes, 10, False), "min")
print("with cancel:   ", machine_minutes(pushes, 10, True), "min")
```

```text
without cancel: 30 min
with cancel:    15 min
```

Sonuç aynı anda (15. dakikada) gelir, ama 30 yerine 15 makine dakikası
harcanır. Dağıtım iş akışlarında `cancel-in-progress` dikkatle kullanılır:
yarıda kesilen bir dağıtım sistemi yarım bırakabilir; orada grup yine
yazılır ama iptal kapalı kalır: süren çalışma bitmeden yenisi başlamaz ve
grupta en fazla bir çalışma bekler.

## Süre sınırı

Bir iş varsayılan olarak 360 dakika (6 saat) çalışabilir. Sonsuz döngüye
giren bir test o kadar makineyi meşgul eder. Üçüncü bölümdeki
`timeout-minutes` işe gerçekçi bir sınır koyar; normalde 5 dakika süren
bir test işine 15 dakika yeterli bir paydır.

## Öbür hızlandırmalar

Önceki bölümlerde gördüklerimiz de hızla ilgili:

- **Yol süzgeci** (dördüncü bölüm): belge değişikliğinde hiç çalışmamak.
- **Paralel işler ve kritik yol** (beşinci bölüm): bağımsız işleri aynı
  anda çalıştırmak, hızlandırmaya kritik yoldan başlamak.
- **Matrisi kırpmak** (altıncı bölüm): her birleşim gerekli değil.
- **Hızlı olan önce:** `pytest -x` ilk düşen testte durur; hatalı bir
  PR'da bütün testleri beklemek gerekmez.

Ölçmeden hızlandırma: GitHub her adımın süresini kaydında gösterir. Önce
en uzun adıma bak; çoğu zaman orası bağımlılık kurulumudur.

## Hepsi bir arada

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            pip-${{ runner.os }}-
      - run: pip install -r requirements.txt
      - run: python -m pytest -x
```

## Özet

- Her iş temiz makinede başlar; tekrar eden en pahalı iş bağımlılık
  kurulumudur.
- `actions/cache`: `path` klasörünü `key` ile saklar ve geri yükler.
  Kurulumdan önce gelir.
- Anahtar içerikten üretilir: `hashFiles('requirements.txt')`; işletim
  sistemi de anahtarda.
- `restore-keys`: tam anahtar yoksa önekle başlayan en yeni önbellek.
- `setup-python`'da `cache: pip` aynı işi kısaca yapar.
- `concurrency` + `cancel-in-progress` eski çalışmaları iptal eder
  (dağıtımda dikkat). `timeout-minutes` takılan işi durdurur.
