# İşler ve Bağımlılıklar

Şimdiye kadarki iş akışlarında çoğunlukla tek bir iş vardı. Gerçek bir
hatta birkaç iş olur: kod denetimi (lint), testler, paket derleme,
dağıtım. Bu bölümde işlerin nasıl **aynı anda** çalıştığını, `needs` ile
nasıl **sıraya** konduğunu, bir iş düşünce ötekilere ne olduğunu ve işin
koşulla (`if`) nasıl atlandığını görüyoruz.

## İşler aynı anda çalışır

Bir iş akışında birden çok iş varsa GitHub hepsini **aynı anda** başlatır.
Her iş kendi temiz makinesinde çalışır:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ruff check .
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest
```

`lint` ve `test` birbirini beklemez. İki şey buradan çıkıyor:

- **Zaman kazanılır:** iki dakikalık lint ile altı dakikalık test toplam
  altı dakikada biter, sekizde değil.
- **İşler dosya paylaşmaz:** her iş ayrı makinede olduğu için her biri
  kodu kendisi çeker (`checkout`). Bir işin ürettiği dosya ötekinde
  yoktur; işler arasında dosya taşımayı sekizinci bölümde göreceğiz.

## needs: sıraya koymak

Bazı işler ötekinin bitmesini beklemeli: testler geçmeden paket
derlenmemeli, paket olmadan dağıtım olmaz. `needs` bunu söyler:

```yaml
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: echo "build"
```

`build`, `lint` ve `test` **ikisi de başarıyla** bitince başlar. Tek iş
için `needs: test` da yazılabilir.

İşler ve aralarındaki `needs` okları bir **yönlü graf** oluşturur
(Algoritma Teknikleri modülündeki DAG). GitHub hangi işin ne zaman
başlayacağını bu graftan çıkarır. Aynı hesabı Python'la yapalım: bir
**dalga**, beklediği bütün işler bitmiş olan işlerin kümesi; bir
dalgadaki işler aynı anda çalışabilir.

```python
needs = {
    "lint": [],
    "test": [],
    "docs": [],
    "build": ["lint", "test"],
    "deploy": ["build"],
}


def waves(needs):
    done = []
    result = []
    while len(done) < len(needs):
        wave = [job for job in needs
                if job not in done and all(n in done for n in needs[job])]
        if not wave:
            raise ValueError("circular needs: " + ", ".join(
                job for job in needs if job not in done))
        result.append(wave)
        done += wave
    return result


for number, wave in enumerate(waves(needs), start=1):
    print(number, wave)
```

```text
1 ['lint', 'test', 'docs']
2 ['build']
3 ['deploy']
```

Üç dalga: önce `lint`, `test` ve `docs` birlikte, sonra `build`, en son
`deploy`.

## Toplam süre ve kritik yol

Bir işin bitiş anı, kendi süresi ile beklediği işlerin **en geç** bitenin
toplamıdır. Süreler dakika olsun:

```python
minutes = {"lint": 1, "test": 6, "docs": 2, "build": 3, "deploy": 2}

finish = {}
for wave in waves(needs):
    for job in wave:
        start = max([finish[n] for n in needs[job]], default=0)
        finish[job] = start + minutes[job]

print("finish:", finish)
print("pipeline:", max(finish.values()), "min")
print("one by one:", sum(minutes.values()), "min")
```

```text
finish: {'lint': 1, 'test': 6, 'docs': 2, 'build': 9, 'deploy': 11}
pipeline: 11 min
one by one: 14 min
```

Hat 11 dakikada bitiyor; işler sırayla çalışsaydı 14 dakika sürerdi.
11 dakikayı belirleyen zincir `test → build → deploy`: buna **kritik yol**
denir. `lint`'i iki kat hızlandırmak hattı bir saniye bile kısaltmaz;
hattı hızlandırmak isteyen kritik yoldaki işe bakar (burada `test`).

## Döngü

`a` işi `b`'yi, `b` de `a`'yı beklerse hiçbiri başlayamaz. GitHub böyle
bir dosyayı çalıştırmaz. Bizim `waves` fonksiyonu da başlayabilecek iş
bulamayınca durur:

```python
try:
    waves({"build": ["test"], "test": ["build"]})
except ValueError as error:
    print(error)
```

```text
circular needs: build, test
```

Olmayan bir işe `needs` yazmak (`needs: tests`, iş adı `test` iken) da
dosyayı geçersiz yapar. Odyssey'in denetimi ikisini de yakalıyor.

## Bir iş düşünce

Varsayılan kural: bir iş, beklediği işlerin **hepsi başarılıysa** çalışır.
Biri düşerse ona bağlı işler **atlanır** (skipped), onlara bağlı olanlar
da. Bu kural işin `if` koşuluyla değiştirilebilir. Koşulda kullanılan üç
**durum fonksiyonu** var:

<figure class="fig anat">
  <div class="anat-row"><span><code>success()</code></span><span>Önceki işlerin hepsi başarılı. <code>if</code> yazılmazsa geçerli olan bu.</span></div>
  <div class="anat-row"><span><code>failure()</code></span><span>Önceki işlerden biri (zincirde daha geride olanlar dahil) düştü. Hata bildirimi için.</span></div>
  <div class="anat-row"><span><code>always()</code></span><span>Ne olursa olsun çalış. Temizlik ya da rapor için.</span></div>
</figure>

Bu kuralları Python'la yazıp `test` düştüğünde her işe ne olduğuna
bakalım. `notify` yalnızca bir şey düşünce, `report` her zaman çalışsın:

```python
pipeline = {
    "lint": [],
    "test": [],
    "build": ["lint", "test"],
    "deploy": ["build"],
    "notify": ["deploy"],
    "report": ["deploy"],
}
conditions = {"notify": "failure()", "report": "always()"}


def ancestors(needs, job):
    found = set()
    for parent in needs[job]:
        found |= {parent} | ancestors(needs, parent)
    return found


def statuses(needs, failed, conditions):
    status = {}
    for wave in waves(needs):
        for job in wave:
            condition = conditions.get(job, "success()")
            if condition == "always()":
                runs = True
            elif condition == "failure()":
                runs = any(status[a] == "failure" for a in ancestors(needs, job))
            else:
                runs = all(status[n] == "success" for n in needs[job])
            if not runs:
                status[job] = "skipped"
            elif job in failed:
                status[job] = "failure"
            else:
                status[job] = "success"
    return status


for job, state in statuses(pipeline, {"test"}, conditions).items():
    print(f"{job:<7} {state}")
```

```text
lint    success
test    failure
build   skipped
deploy  skipped
notify  success
report  success
```

- `test` düştü → `build` atlandı → `deploy` de atlandı.
- `notify`'ın `if: failure()` koşulu geride, zincirin başında düşen
  `test`'i görüyor ve çalışıyor; yalnızca doğrudan beklediği `deploy`'a
  baksaydı (`deploy` atlandı, düşmedi) hiç çalışmazdı.
- `report` `always()` olduğu için çalışıyor.

## if ile koşul

`if` yalnızca durum için değil, olaya ve dala göre karar vermek için de
kullanılır. Koşulda GitHub'ın **bağlam** (context) değerleri okunur:

<figure class="fig anat">
  <div class="anat-row"><span><code>github.event_name</code></span><span>İş akışını başlatan olay: <code>push</code>, <code>pull_request</code>...</span></div>
  <div class="anat-row"><span><code>github.ref</code></span><span>Dal ya da etiket: <code>refs/heads/main</code>, <code>refs/tags/v1.2.0</code>.</span></div>
  <div class="anat-row"><span><code>github.actor</code></span><span>Çalışmayı başlatan kullanıcı.</span></div>
  <div class="anat-row"><span><code>needs.&lt;iş&gt;.result</code></span><span>Beklenen işin sonucu: <code>success</code>, <code>failure</code>, <code>skipped</code>.</span></div>
</figure>

En sık örnek: dağıtım yalnızca `main`'e gönderimde olsun, PR'larda
olmasın.

```yaml
  deploy:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

Koşulun yazımı:

- Metinler **tek tırnakla** yazılır: `'refs/heads/main'`.
- `&&` "ve", `||` "veya", `!` "değil" demek.
- `if` değerinde `${{ }}` yazmak gerekmez; GitHub onu zaten ifade olarak
  okur.
- `success()` dışında bir durum fonksiyonu kullanılmazsa koşulun önüne
  kendiliğinden `success() &&` eklenir: `if: github.ref == ...` yazılan
  iş, beklediği işler düşmüşse yine çalışmaz.

## İşten işe değer aktarmak

İşler dosya paylaşmaz ama küçük bir **değer** aktarabilir. Değer bir
adımda `$GITHUB_OUTPUT` dosyasına `ad=değer` diye yazılır, işin
`outputs` bölümünde dışarı açılır ve öbür işte
`needs.<iş>.outputs.<ad>` ile okunur:

```yaml
jobs:
  version:
    runs-on: ubuntu-latest
    outputs:
      number: ${{ steps.read.outputs.number }}
    steps:
      - uses: actions/checkout@v4
      - id: read
        run: echo "number=$(cat VERSION)" >> "$GITHUB_OUTPUT"
  build:
    needs: version
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building ${{ needs.version.outputs.number }}"
```

Adımın `id`'si (`read`) onun çıktısına ad vermek için. Sürüm numarası,
değişen klasörlerin listesi gibi küçük metinler için uygun; dosya için
değil.

## Hata olsa da devam

Bir işin düşmesi hattı düşürür. Bazen bir iş "bilgi için" çalışır:
örneğin Python'un henüz çıkmamış sürümüyle deneme. O işe
`continue-on-error: true` yazılırsa, düşse bile çalışmanın sonucu başarılı
sayılır. Az kullanılmalı: her şeye yazılırsa hat hiçbir şeyi durdurmaz.

## Hepsi bir arada

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff
      - run: ruff check .
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python -m pytest
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip wheel . -w dist
  deploy:
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
  notify:
    needs: deploy
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: echo "The pipeline failed on ${{ github.ref }}"
```

## Özet

- İşler varsayılan olarak aynı anda, ayrı makinelerde çalışır; dosya
  paylaşmaz.
- `needs` sıra koyar; işler bir yönlü graf oluşturur. Döngü ve olmayan
  işe `needs` geçersizdir.
- Hattın süresini **kritik yol** belirler; hızlandırmak için oradaki işe
  bak.
- Bir iş düşünce ona bağlı işler atlanır. `failure()` zincirde geride
  düşen işi de görür; `always()` her zaman çalışır.
- `if` bağlamı okur: `github.event_name`, `github.ref`. Metinler tek
  tırnakla.
- Küçük değerler `$GITHUB_OUTPUT` → `outputs` → `needs.<iş>.outputs`
  yoluyla aktarılır.
