# Kod Kalitesi Kapıları

Testler kodun **doğru** çalışıp çalışmadığını söyler. Ama doğru çalışan
bir kod da okunmaz, tutarsız ya da tehlikeli olabilir: kullanılmayan
içe aktarmalar, unutulmuş `print` satırları, her dosyada başka bir yazım
biçimi, testlerin hiç dokunmadığı dallar. Hattaki **kalite kapıları** bunları
yakalar. Bu bölümde hangi kapıların olduğunu, hatta hangi sırayla
konduğunu ve bir kapının "geç / geçme" kararını nasıl verdiğini görüyoruz.

## Kapı nedir

**Kapı** (gate), bir kuralı denetleyen ve kural tutmazsa hattı durduran
aşamadır. Test aşaması da bir kapı: bir test düşerse hat durur. Kalite
kapıları aynı mantıkla çalışır, yalnızca denetledikleri şey farklıdır.

Her kapının iki parçası vardır:

- **Ölçüm:** bir araç kodu inceler ve bir şey sayar ya da bulur (uzun
  satırlar, kullanılmayan adlar, test edilmemiş satırlar).
- **Eşik:** ölçüm hangi değerin altında ya da üstündeyse kapı kapanır
  ("hiç lint hatası olmayacak", "kapsam en az %80").

Kapı da kararını, testlerde gördüğümüz gibi, **çıkış koduyla** bildirir:
kural tutuyorsa `0`, tutmuyorsa `0` dışında bir sayı.

## Sık kullanılan kapılar

<figure class="fig anat">
  <div class="anat-row"><span>Sözdizimi</span><span>Kod Python olarak okunabiliyor mu? En hızlı kapı.</span></div>
  <div class="anat-row"><span>Biçim</span><span>Girinti, boşluk, tırnak, satır uzunluğu herkeste aynı mı? (biçimlendirici, formatter)</span></div>
  <div class="anat-row"><span>Lint</span><span>Kod çalıştırılmadan bulunabilen hatalar: kullanılmayan içe aktarma, tanımsız ad, gölgelenen değişken. (statik analiz)</span></div>
  <div class="anat-row"><span>Tip denetimi</span><span>Tip belirtimleri (type hints) birbiriyle tutarlı mı?</span></div>
  <div class="anat-row"><span>Test</span><span>Bütün testler geçiyor mu?</span></div>
  <div class="anat-row"><span>Kapsam</span><span>Testler kodun ne kadarını çalıştırdı? (coverage)</span></div>
</figure>

**Statik analiz** (static analysis), kodu çalıştırmadan, yalnızca okuyarak
incelemek demek. Hızlıdır ve programın her yolunu görür; ama programın
çalışırken ne yapacağını bilemez. Testler bunun tersi: kodu gerçekten
çalıştırır ama yalnızca denedikleri yolları görür. İkisi birbirini
tamamlar.

## En hızlı kapı: sözdizimi

Python kurulu her yerde hazır bir kapı var: `py_compile` bir dosyayı
çalıştırmadan derler ve sözdizimi hatası varsa çıkış kodu `1` ile biter.
Kapanmamış bir parantez içeren dosyayı ve sağlam bir dosyayı denedik:

```python
import subprocess
import sys
from pathlib import Path

Path("good.py").write_text("print('hello')\n")
Path("broken.py").write_text("print('hello'\n")

for name in ["good.py", "broken.py"]:
    command = [sys.executable, "-m", "py_compile", name]
    result = subprocess.run(command, capture_output=True, text=True)
    print(name, "-> exit code", result.returncode)
```

```text
good.py -> exit code 0
broken.py -> exit code 1
```

Bu kapı bir saniye bile sürmez, bu yüzden hattın en başına konur: kod
okunamıyorsa testleri kurmaya hiç gerek yok.

## Biçim ve lint: gerçek dünyadaki araçlar

Python projelerinde bugün en yaygın araçlardan biri **ruff**: hem lint
yapıyor hem kodu biçimlendiriyor. Aynı işi yapan eski araçlar da var
(lint için flake8, pylint; biçim için black). Hatta şöyle çalıştırılır:

```text
pip install ruff
ruff check .
ruff format --check .
```

- `ruff check .` klasördeki bütün dosyalarda lint kurallarına bakar. Bir
  kural çiğnenmişse dosyayı, satırı ve kuralın kodunu yazar, çıkış kodu
  `0` olmaz.
- `ruff format .` dosyaları **düzeltir**. Hatta ise `--check` ile çalışır:
  dosyalara dokunmaz, yalnızca "şu dosya biçimsiz" der ve kapıyı kapatır.
  Hattın kodu değiştirmesi istenmez; düzeltmeyi geliştirici kendi
  bilgisayarında yapar.

Bu araçlar Odyssey'de kurulu değil; komutları kendi projende
kullanacaksın. Bu bölümün alıştırmalarında aynı fikri küçük ölçekte kendi
kodunla kuruyorsun: uzun satırları ve unutulmuş `print`'leri bulan bir
kapı.

**Tip denetimi** için en yaygın araç **mypy**: `mypy .` tip belirtimlerine
bakar ve `int` bekleyen bir yere `str` verildiğini kodu çalıştırmadan
bulur.

## Kapsam: testler kodun ne kadarına dokundu

**Kapsam** (coverage), testler çalışırken kodun hangi satırlarının en az
bir kez çalıştığını ölçer. Yaygın araç **coverage.py**, pytest ile
birlikte `pytest-cov` eklentisiyle kullanılır:

```text
python -m pytest --cov=cart --cov-fail-under=80
```

`--cov-fail-under=80` kapsam yüzde 80'in altındaysa komutu düşürür: işte
bir eşik.

Kapsam aracı içeride ne yapıyor? Python'un kendi `trace` modülüyle aynısını
küçük ölçekte görebiliriz. Önceki bölümdeki `cart.py` şöyleydi (satır
numaralarıyla düşün):

```python
def cart_total(prices, discount=0):
    if discount < 0 or discount > 100:
        raise ValueError("discount must be between 0 and 100")
    total = sum(prices)
    if discount:
        total = total - total * discount / 100
    return round(total, 2)
```

Yalnızca indirimsiz iki testi çalıştırıp hangi satırların çalıştığını
sayalım:

```python
import trace

from cart import cart_total


def test_total_without_discount():
    assert cart_total([10, 20, 30]) == 60


def test_empty_cart():
    assert cart_total([]) == 0


tracer = trace.Trace(count=1, trace=0)
tracer.runfunc(test_total_without_discount)
tracer.runfunc(test_empty_cart)

body = range(2, 8)
ran = sorted(line for (file, line) in tracer.results().counts if file.endswith("cart.py"))
missed = [line for line in body if line not in ran]
print("ran:", ran)
print("missed:", missed)
print("coverage:", round(100 * len(ran) / len(body)), "%")
```

```text
ran: [2, 4, 5, 7]
missed: [3, 6]
coverage: 67 %
```

İki test geçti, ama 3. satır (hata) ve 6. satır (indirim) **hiç**
çalışmadı. Önceki bölümdeki `/ 10` hatası tam 6. satırdaydı: bu iki testle
hat yeşil kalır ve hata kullanıcıya gider. Kapsam bunu görünür yapar.

İndirim testi ve iki hata testi eklenince aynı ölçüm:

```text
ran: [2, 3, 4, 5, 6, 7]
missed: []
coverage: 100 %
```

## Kapsam neyi söylemez

- **%100 kapsam, kodun doğru olduğu anlamına gelmez.** Satır çalıştı, ama
  sonucu denetleyen bir `assert` olmayabilir. `assert` içermeyen bir test
  de kapsamı yükseltir.
- Kapsamı yükseltmek için anlamsız test yazmak kolaydır. Eşik bu yüzden
  makul tutulur (%70–90 sık görülür) ve asıl soru şudur: **önemli dallar
  test ediliyor mu?**
- İyi bir alışkanlık: kapsamın **düşmesine** izin verme. Yeni kod testsiz
  eklenirse kapı kapansın.

## Kapıların sırası

Hızlı düşmek kuralı kapılara da uygulanır. Ucuz kapılar önde:

<figure class="fig">
  <div class="flow">
    <span class="node">Sözdizimi</span>
    <span class="arrow">→</span>
    <span class="node">Biçim</span>
    <span class="arrow">→</span>
    <span class="node">Lint</span>
    <span class="arrow">→</span>
    <span class="node acc">Test</span>
    <span class="arrow">→</span>
    <span class="node">Kapsam</span>
  </div>
  <figcaption>Saniyeler süren kapılar önde, dakikalar süren testler arkada.</figcaption>
</figure>

İş akışında bu, adımların sırası demek:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install ruff
      - run: ruff check .
      - run: ruff format --check .
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

Biçim ya da lint düşerse testler hiç kurulmaz bile; geri bildirim
saniyeler içinde gelir.

## Kapıları yerelde de çalıştır

Hatta düşen bir biçim kapısı, bir dakikalık bir düzeltme için bütün hattı
yeniden beklemek demek. Bu yüzden ekipler aynı komutları göndermeden önce
kendi bilgisayarlarında da çalıştırır. Bunu kendiliğinden yapan araçlar
var (commit'ten önce çalışan **pre-commit** kancaları); fikir aynı: hattın
yakalayacağını hatta gitmeden yakala.

## Özet

- Kapı = ölçüm + eşik; kararını çıkış koduyla verir.
- Statik analiz kodu çalıştırmadan okur (biçim, lint, tip); testler kodu
  çalıştırır. İkisi birbirini tamamlar.
- Hatta biçimlendirici `--check` ile çalışır, dosyaları değiştirmez.
- Kapsam test edilmemiş satırları gösterir; %100 kapsam doğruluk demek
  değildir.
- Ucuz kapılar önde: sözdizimi, biçim, lint, sonra testler.
