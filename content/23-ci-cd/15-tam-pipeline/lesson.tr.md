# Bitirme: Bir Python Projesinin Tam Hattı

Bu modülde hattın parçalarını tek tek kurduk: testler, kalite kapıları,
tetikleyiciler, işler, matris, önbellek, paket, gizli değerler, sürüm,
dağıtım, dal kuralları. Bu bölümde hepsini **tek bir projenin tek bir
hattında** birleştiriyoruz. Yeni bir şey öğrenmekten çok, her parçanın
neden orada olduğunu söyleyebilmek amacımız.

## Proje

Sıcaklık çeviren küçük bir Python paketi: `tempconv`.

```text
tempconv-project/
├── .github/workflows/ci.yml
├── pyproject.toml
├── requirements-dev.txt
├── scripts/check_version.py
├── tempconv/
│   ├── __init__.py
│   └── convert.py
└── tests/
    └── test_convert.py
```

```python
def c_to_f(celsius):
    return round(celsius * 9 / 5 + 32, 2)


def f_to_c(fahrenheit):
    return round((fahrenheit - 32) * 5 / 9, 2)
```

```python
import pytest

from tempconv.convert import c_to_f, f_to_c

CASES = [(0, 32), (100, 212), (-40, -40), (37, 98.6)]


@pytest.mark.parametrize("celsius, fahrenheit", CASES)
def test_c_to_f(celsius, fahrenheit):
    assert c_to_f(celsius) == fahrenheit


def test_round_trip():
    assert f_to_c(c_to_f(21.5)) == 21.5
```

Proje klasöründe testler:

```text
> python -m pytest -q
.....                                                                    [100%]
5 passed
```

`requirements-dev.txt` geliştirme araçlarını listeler
(`pytest`, `pytest-cov`); `scripts/check_version.py` onuncu bölümdeki
betik: etiketle `pyproject.toml`'daki sürüm aynı mı?

## Hattın sözleşmesi

YAML'dan önce hattın neyi **garanti edeceğini** yazalım. Her satırın
arkasında bir bölüm var:

| Garanti | Nasıl | Bölüm |
|---|---|---|
| Her PR ve `main` sınanır | `push` + `pull_request` + `merge_group` | 4, 13 |
| Biçim ve lint hatası girmez | `ruff check`, `ruff format --check` | 2 |
| İki Python sürümünde testler geçer | Matris, `fail-fast: false` | 1, 6 |
| Testler kodun en az %90'ına dokunur | `--cov-fail-under=90` | 2 |
| Paket bir kez derlenir | `build` + artifact | 8 |
| Zorunlu kontrol tek ad | `ci-ok` kapı işi | 13 |
| Yayın yalnızca `v` etiketinde, sürüm tutarlı | `if:` + `check_version.py` | 10 |
| En az izin | Üstte `contents: read`, yayında `write` | 9 |
| Boşa çalışma yok, asılı iş yok | `concurrency`, `timeout-minutes`, `cache` | 7 |

## 1. Tetikleyiciler ve genel ayarlar

```yaml
name: CI

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]
  merge_group:

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
```

Yedinci bölümde `cancel-in-progress: true` yazmıştık. Burada yalnızca
PR'da iptal ediyoruz: PR'a yeni commit gelince eski çalışma boşa gider,
ama `main`'in ve etiketin her çalışması bitmeli (her biri bir sürümün
kaydı).

## 2. Lint ve testler

```yaml
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install ruff
      - run: python -m ruff check .
      - run: python -m ruff format --check .
  test:
    needs: lint
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
      - run: python -m pip install -r requirements-dev.txt
      - run: python -m pytest -q --cov=tempconv --cov-fail-under=90
```

- Lint önce: saniyeler süren kapı düşerse dakikalar süren testler hiç
  başlamaz (ikinci bölümdeki "hızlı kapı önce").
- `fail-fast: false`: bir sürümde düşen test, öbür sürümün sonucunu
  gizlemesin.
- `cache: pip` her çalışmada paketleri yeniden indirmez.

## 3. Paket ve kapı

```yaml
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  ci-ok:
    if: always()
    needs: [lint, test, build]
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
        if: >-
          contains(needs.*.result, 'failure')
          || contains(needs.*.result, 'cancelled')
      - run: echo "all checks passed"
```

Paket her çalışmada derlenir: PR'da da. Böylece "paket derlenmiyor" hatası
yayın gününe kalmaz. `main` için dal kuralında zorunlu kontrol olarak
yalnızca `ci-ok` yazılır.

## 4. Yayın

```yaml
  release:
    needs: ci-ok
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/check_version.py "$GITHUB_REF_NAME"
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: |
          gh release create "$GITHUB_REF_NAME" dist/* \
            --repo "$GITHUB_REPOSITORY" --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- `needs: ci-ok`: yayın, kapının arkasında. Kapı `if: always()` ile
  çalışıyor ama düşerse yayın atlanır.
- Yazma izni yalnızca bu işte; dosyanın üstündeki varsayılan okuma.
- Yayınlanan dosyalar `build`'in derlediği ve test edilen paketin aynısı.

Dört parça alt alta tek dosya: `.github/workflows/ci.yml`.

## Hat ne kadar sürer?

Beşinci bölümdeki kritik yol: bir iş, bağlı olduğu en geç iş bitince
başlar. Dakikaları tahmin edip hesaplayalım (matrisin iki kopyası aynı
anda çalıştığı için `test` tek satır):

```python
jobs = {
    "lint": (1, []),
    "test": (4, ["lint"]),
    "build": (1, ["test"]),
    "ci-ok": (0, ["lint", "test", "build"]),
    "release": (1, ["ci-ok"]),
}


def finish(name):
    minutes, needs = jobs[name]
    return minutes + max((finish(n) for n in needs), default=0)


for name in jobs:
    print(f"{name:<8} done at minute {finish(name)}")

jobs["test"] = (4, [])
print("test without lint first:", finish("release"))
```

```text
lint     done at minute 1
test     done at minute 5
build    done at minute 6
ci-ok    done at minute 6
release  done at minute 7
test without lint first: 6
```

Lint'i testten önce koymak yeşil bir yayını bir dakika uzatıyor; buna
karşılık biçim hatası olan bir PR'da iki test makinesi hiç açılmıyor. Bu
bir seçim: hat yavaşsa ve lint nadiren düşüyorsa ikisi paralel de
çalışabilir. Önemli olan, seçimin bilerek yapılması.

## Depo ayarları

Hattın dosyası yetmez; GitHub'da üç ayar daha:

- **Settings › Rules:** `main` için PR zorunlu, en az bir onay, zorunlu
  kontrol `ci-ok`, zorla gönderim yasak.
- **Settings › Actions › General:** iş akışı izinleri varsayılan olarak
  "yalnızca okuma".
- **Etiket kuralı:** `v*` etiketlerini yalnızca bakımcılar oluşturabilir;
  yoksa etiket atabilen herkes yayın yapar.

## Son kontrol listesi

- PR açınca lint, iki test, paket ve `ci-ok` çalışıyor mu?
- Yalnızca `README.md`'yi değiştiren bir PR'da da `ci-ok` sonuç veriyor
  mu? (Bu hatta yol süzgeci yok, veriyor. Süzgeç eklenirse on üçüncü
  bölümdeki tuzak geri gelir.)
- Bir testi bilerek bozunca `ci-ok` kırmızı ve birleştirme kapalı mı?
- `pyproject.toml` `0.3.0` iken `v0.3.1` etiketi atınca yayın duruyor mu?
- `v0.3.0` etiketiyle sürüm sayfasında `dist` dosyaları var mı?

## Sırada

On altıncı bölüm genel tekrar: bütün modülü sorular ve karma
alıştırmalarla yokluyoruz.

## Özet

- Önce sözleşme, sonra YAML: her garanti bir parçaya, her parça bir
  bölüme dayanıyor.
- Tetikleyiciler `push`, `pull_request`, `merge_group` ve `v*` etiketi;
  iptal yalnızca PR'da.
- Lint önce, testler matrisle ve kapsam eşiğiyle, paket bir kez, tek
  zorunlu kontrol `ci-ok`.
- Yayın yalnızca etikette, kapının arkasında, sürüm denetimiyle ve kendi
  yazma izniyle.
- Kritik yol hattın süresini verir; sıralama bir hız ve maliyet
  seçimidir.
- Dal kuralları ve izin ayarları hattın dosyası kadar önemli.
