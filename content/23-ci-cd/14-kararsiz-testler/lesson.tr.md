# Kararsız Testler ve Hata Ayıklama

Kod değişmediği hâlde bir çalışmada geçip ötekinde düşen teste
**kararsız test** (flaky test) denir. Kararsız test hattın en sinsi
sorunudur: kırmızı çarpıyı gören kişi "yine o test" deyip yeniden
çalıştırır, bir gün gerçek hata da aynı yoldan geçip gider. Bu bölümde
kararsızlığın nereden geldiğini ölçüyor, nasıl düzeltileceğini ve düşen
bir hattın nedenini nasıl bulacağımızı görüyoruz.

## Bir kararsız test ne kadar zarar verir?

Diyelim ki bir test yüz çalışmanın ikisinde nedensiz düşüyor: %98 geçiyor.
Tek başına küçük görünür. Ama hattın yeşil olması için **bütün**
testlerin aynı anda geçmesi gerekir; kararsız testler çoğaldıkça
olasılıklar çarpılır:

```python
for flaky in [1, 5, 20]:
    chance = 0.98 ** flaky
    print(f"{flaky:>2} flaky tests: suite passes {chance:.0%}")
```

```text
 1 flaky tests: suite passes 98%
 5 flaky tests: suite passes 90%
20 flaky tests: suite passes 67%
```

Yirmi kararsız testte hat üç çalışmanın birinde nedensiz kırmızı. O
noktada kimse kırmızıya inanmaz; CI'ın bütün değeri, "kırmızı = bir şey
bozuldu" güvenine dayanıyor.

## Kararsızlığın kaynakları

| Kaynak | Örnek | Düzeltme |
|---|---|---|
| Sıra bağımlılığı | Bir test, öncekinin bıraktığı veriye güveniyor | Her test kendi verisini kurar (fixture) |
| Zaman | `datetime.now()` hafta sonu başka sonuç veriyor | Saati dışarıdan ver |
| Rastgelelik | Tohumsuz `random` | Sabit tohum (`random.Random(42)`) |
| Küme ve sözlük sırası | Metin kümesinin sırası çalışmadan çalışmaya değişiyor | Sırayı `sorted` ile sabitle |
| Bekleme ve yarış | `sleep(1)` "yeter herhalde" | Koşulu bekle, süre değil |
| Ağ | Testte gerçek bir siteye istek | Sahte sunucu ya da kayıtlı cevap |

Üçünü ölçerek görelim.

## Kümenin sırası

Python, metinlerin `hash` değerini her süreçte başka bir tohumla
hesaplar (güvenlik için). Bu yüzden bir metin kümesinin gezilme sırası
**süreçten sürece** değişebilir. Aşağıdaki "testi" yazan kişi, kümenin
sırasını kendi bilgisayarında bir kez görüp öyle yazmış. Testi on ayrı
süreçte, her birinde farklı bir tohumla (`PYTHONHASHSEED`)
çalıştırıyoruz:

```python
import os
import subprocess
import sys

test = 'assert list({"api", "db", "web"}) == ["db", "web", "api"]'
results = []
for seed in range(10):
    env = {**os.environ, "PYTHONHASHSEED": str(seed)}
    run = subprocess.run([sys.executable, "-c", test], env=env)
    results.append("pass" if run.returncode == 0 else "FAIL")
print(" ".join(results))
print("passed:", results.count("pass"), "of", len(results))
```

```text
pass pass FAIL FAIL pass FAIL pass FAIL FAIL FAIL
passed: 4 of 10
```

Kod aynı, sonuç çalışmadan çalışmaya değişiyor: on çalışmanın
4'ünde geçti. Yazan kişinin bilgisayarında geçmesi şanstı. Düzeltme: sıraya güvenme. Karşılaştırmayı
`sorted(...)` ile ya da doğrudan kümeyle (`== {"api", "db", "web"}`) yap.

## Sıra bağımlılığı

İki test aynı modül değişkenini paylaşıyor:

```python
cart = []


def add(item):
    cart.append(item)
    return len(cart)


def test_add_first():
    assert add("apple") == 1


def test_add_second_alone():
    assert add("pear") == 1
```

İkinci test tek başına çalışınca geçiyor, dosyanın tamamı çalışınca
düşüyor (`--tb=no` hata ayrıntısını gizliyor, sona kısa bir özet kalıyor):

```text
> python -m pytest -q --tb=no test_cart.py::test_add_second_alone
.                                                                        [100%]
1 passed

> python -m pytest -q --tb=no
.F                                                                       [100%]
=========================== short test summary info ===========================
FAILED test_cart.py::test_add_second_alone - AssertionError: assert 2 == 1
1 failed, 1 passed
```

Tek başına geçen ama başkalarıyla düşen test, öncekinin bıraktığı
duruma güveniyor demektir. Paralel çalıştırma ya da testlerin sırasını
değiştiren bir eklenti onu bir gün düşürür. Düzeltme: her testin kendi
verisini kuran bir **fixture**:

```python
import pytest


@pytest.fixture
def cart():
    return []


def add(cart, item):
    cart.append(item)
    return len(cart)


def test_add_first(cart):
    assert add(cart, "apple") == 1


def test_add_second_alone(cart):
    assert add(cart, "pear") == 1
```

```text
> python -m pytest -q
..                                                                       [100%]
2 passed
```

## Zaman

`datetime.now()` çağıran bir fonksiyonun testi, testin **hangi gün**
çalıştığına bağlıdır. Hattın makinesi de UTC saatinde çalışır; senin
saatinle gece yarısında farklı bir gün olabilir. Düzeltme: saati
fonksiyona dışarıdan vermek. Testte sabit bir tarih verilir, programda
verilmez:

```python
from datetime import datetime


def is_weekend(now=None):
    now = now or datetime.now()
    return now.weekday() >= 5


print(is_weekend(datetime(2026, 10, 17)))
print(is_weekend(datetime(2026, 10, 19)))
```

```text
True
False
```

## Kararsız testle ne yapılır?

**Yeniden çalıştırmak çözüm değil.** GitHub'ın "Re-run failed jobs"
düğmesi ya da testi kendiliğinden birkaç kez deneyen eklentiler
kırmızıyı yeşile çevirir ama nedeni saklar; aynı yoldan gerçek bir hata
da geçer.

Hemen düzeltilemiyorsa test **karantinaya** alınır: bir işaretle ayrılır,
ana hattı durdurmaz ama çalışmaya ve görünmeye devam eder:

```python
import pytest


@pytest.mark.flaky
def test_payment_timeout():
    assert True
```

```yaml
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q -m "not flaky"
  quarantine:
    runs-on: ubuntu-latest
    continue-on-error: true
    steps:
      - uses: actions/checkout@v4
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q -m flaky
```

- `-m "not flaky"` işaretli testleri dışarıda bırakır; `-m flaky`
  yalnızca onları çalıştırır.
- `continue-on-error: true`: karantina işi düşse de çalışma kırmızı olmaz.
- İşaret `pyproject.toml`'da tanıtılır (`markers = ["flaky: ..."]`);
  yoksa pytest bilinmeyen işaret uyarısı verir.
- Karantina bir çöp kutusu değil: her karantinadaki testin bir sahibi ve
  bir son tarihi olur. Yoksa "geçici" liste büyür ve testler yeniden
  hiçbir şey denetlemez olur.

## Düşen hattın nedenini bulmak

Kırmızı bir çalışmada sıra şöyle:

1. **Hangi iş, hangi adım?** Çalışma sayfasında kırmızı adımı aç.
2. **İlk hata satırı.** Günlüğün sonu çoğu zaman sonuçtur ("exit code 1");
   neden yukarıdadır. pytest'te `FAILED` satırı ve onun üstündeki
   `assert` satırı.
3. **Yerelde tekrar et.** Aynı Python sürümü, aynı paket sürümleri
   (`requirements.txt` sabitse kolay), aynı komut.
4. **Tekrar edilemiyorsa farklara bak:** işletim sistemi, saat dilimi,
   paket sürümü, sıra.

Hattı hata ayıklamaya hazırlamak da mümkün:

```yaml
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest -q --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-report
          path: report.xml
```

- `timeout-minutes: 15` (yedinci bölüm): asılı kalan bir test işi saatlerce
  bekletmez. GitHub'ın varsayılan sınırı 360 dakika.
- `--junitxml=report.xml` sonuçları makinenin okuyabileceği bir dosyaya
  yazar; hangi testin ne kadar sürdüğü, hangisinin düştüğü içinde.
- `if: failure()` ile rapor yalnızca düşünce saklanır (sekizinci
  bölümdeki artifact).
- Daha ayrıntılı günlük için depoda `ACTIONS_STEP_DEBUG` adında, değeri
  `true` olan bir değişken ya da gizli değer tanımlanır, sonra çalışma
  "debug logging" seçilerek yeniden başlatılır.

## "Bende çalışıyor"

| Fark | Senin bilgisayarın | Hattın makinesi |
|---|---|---|
| İşletim sistemi | Çoğu zaman Windows | `ubuntu-latest` (Linux) |
| Dosya adında büyük-küçük harf | `Data.csv` = `data.csv` | Farklı dosyalar |
| Saat dilimi | Senin saatin | UTC |
| Paket sürümü | Kurduğun gün ne geldiyse | Bugün ne geliyorsa (sabit değilse) |
| Önceden kalan dosyalar | Var | Yok, makine sıfırdan |

Son satır en sık olanı: bilgisayarında elle oluşturduğun bir klasör ya da
önceden indirilmiş bir dosya testleri geçiriyordur; hattın temiz
makinesinde yoktur.

## Sırada

On beşinci bölüm bitirme projesi: bir Python projesinin bütün hattını
baştan sona kuruyoruz.

## Özet

- Kararsız test kod değişmeden geçip düşer; kararsız testler çoğaldıkça
  hattın yeşil olma olasılığı çarpılarak düşer ve kırmızıya güven kalmaz.
- Kaynaklar: sıra, zaman, rastgelelik, küme sırası, bekleme, ağ.
- Metin kümesinin sırası süreçten sürece değişir; sıraya güvenme.
- Tek başına geçip birlikte düşen test sıraya bağlıdır; fixture ile her
  test kendi verisini kurar.
- Saat dışarıdan verilir; testte sabit tarih.
- Yeniden çalıştırmak nedeni saklar; düzeltilemiyorsa sahibi ve son
  tarihi olan bir karantina (`-m "not flaky"`, `continue-on-error`).
- Hata ayıklarken: hangi adım, ilk hata satırı, yerelde tekrar, farklar.
  `timeout-minutes`, `--junitxml` ve düşünce rapor saklamak.
