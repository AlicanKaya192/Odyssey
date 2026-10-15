# Sürümleme ve Etiketler

Sekizinci bölümde paketi derledik, dokuzuncuda anahtarları güvenle
tutmayı ve izinleri daraltmayı gördük. Geriye son adım kaldı: paketi bir
**sürüm numarasıyla yayınlamak**. Kullanıcı "hangi sürümdeyim, yenisinde
ne değişti, güncellersem bir şey bozulur mu?" sorularının cevabını sürüm
numarasından okur. Bu bölümde numarayı nasıl seçeceğimizi, git'te nasıl
işaretleyeceğimizi ve o işaretin hattı nasıl tetiklediğini görüyoruz.

## Anlamlı sürümleme

En yaygın kural **anlamlı sürümleme**dir (Semantic Versioning, kısaca
SemVer). Numara üç parçadır: `ANA.YAN.YAMA`, örneğin `2.4.1`.

<figure class="fig anat">
  <div class="anat-row"><span><code>ANA</code> (major)</span><span>Eskiyle uyumsuz değişiklik: eski kodu kullanan biri güncelleyince kodu bozulabilir. <code>1.9.3</code> → <code>2.0.0</code></span></div>
  <div class="anat-row"><span><code>YAN</code> (minor)</span><span>Geriye uyumlu yeni özellik. <code>1.9.3</code> → <code>1.10.0</code></span></div>
  <div class="anat-row"><span><code>YAMA</code> (patch)</span><span>Yalnızca hata düzeltmesi. <code>1.9.3</code> → <code>1.9.4</code></span></div>
</figure>

Bir parça artınca sağındakiler sıfırlanır: `1.9.3`'ten yeni özellikli
sürüm `1.10.0` olur, `1.10.3` değil. `0.x` sürümler "henüz kararlı değil"
demektir; orada her şey değişebilir.

## Sürümler metin gibi sıralanmaz

`1.10.0`, `1.9.0`'dan yenidir. Ama sürümleri metin olarak karşılaştırmak
bunu ters bulur, çünkü metinler harf harf karşılaştırılır ve `"1"` `"9"`'dan
küçüktür:

```python
versions = ["1.9.0", "1.10.0", "1.2.3", "0.9.12"]
print(sorted(versions))


def as_tuple(version):
    return tuple(int(part) for part in version.split("."))


print(sorted(versions, key=as_tuple))
print("1.10.0" > "1.9.0", as_tuple("1.10.0") > as_tuple("1.9.0"))
```

```text
['0.9.12', '1.10.0', '1.2.3', '1.9.0']
['0.9.12', '1.2.3', '1.9.0', '1.10.0']
False True
```

Parçaları sayıya çevirip **demet** (tuple) olarak karşılaştırınca doğru
sıra çıkıyor: demetler de soldan sağa karşılaştırılır ama her parça bir
sayıdır, `10 > 9`.

Python paketlerinin numaraları SemVer'den biraz daha fazlasını tanır
(PEP 440): yayından önceki denemeler `1.2.0b2` (beta), `1.2.0rc1` (sürüm
adayı, release candidate) ve yayından sonraki küçük düzeltme `1.2.0.post1`.
Bunları elle sıralamak zordur; `packaging` kütüphanesi (pip'in kendi
kullandığı) doğru sırayı bilir:

```python
from packaging.version import Version

candidates = ["1.2.0", "1.2.0rc1", "1.2.0b2", "1.1.9", "1.2.0.post1"]
for version in sorted(candidates, key=Version):
    print(version)
```

```text
1.1.9
1.2.0b2
1.2.0rc1
1.2.0
1.2.0.post1
```

Aday sürüm, asıl sürümden **önce** gelir: `1.2.0rc1 < 1.2.0`. pip bu
yüzden aday sürümleri kendiliğinden kurmaz; istenirse `--pre` ile kurar.

## Hangi parça artacak?

Numarayı elle seçmek unutkanlığa açıktır. Yaygın bir çözüm commit
mesajlarına bir önek yazmaktır (**Conventional Commits**):

| Önek | Anlamı | Sürüm |
|---|---|---|
| `fix: ...` | Hata düzeltmesi | YAMA |
| `feat: ...` | Yeni özellik | YAN |
| `feat!: ...` ya da metinde `BREAKING CHANGE` | Uyumsuz değişiklik | ANA |
| `docs: ...`, `test: ...`, `ci: ...` | Kullanıcının gördüğü bir şey değişmedi | Yeni sürüm yok |

Son yayından bu yana gelen commit'lerin en büyüğü kazanır: bir `feat` ve
üç `fix` varsa sürüm YAN artar. Numarayı artırmak küçük bir fonksiyon:

```python
def bump(version, part):
    major, minor, patch = (int(p) for p in version.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


print(bump("1.9.3", "patch"))
print(bump("1.9.3", "minor"))
print(bump("1.9.3", "major"))
```

```text
1.9.4
1.10.0
2.0.0
```

Önekleri okuyup hangi parçanın artacağına karar veren kısım alıştırmada.
Bu kurala göre sürüm numarası ve sürüm notu üreten hazır araçlar da var
(ör. `release-please`, `semantic-release`); hepsinin temeli bu tablo.

## Etiket: commit'e kalıcı bir ad

Git'te bir sürüm **etiketle** (tag) işaretlenir: belirli bir commit'e
verilen, dal gibi ilerlemeyen bir ad. Yayınlanan sürüm hangi koddan
çıktıysa etiket onu gösterir.

```text
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
```

- `-a` açıklamalı (annotated) etiket: kimin, ne zaman ve hangi mesajla
  koyduğunu da saklar. Sürüm için önerilen budur.
- Etiketler `git push` ile kendiliğinden gönderilmez; adıyla gönderilir.
- Ad genellikle `v` ile başlar: `v1.2.0`. Paketin kendi numarası
  `pyproject.toml`'da `v`'siz yazılır: `1.2.0`.
- **Yayınlanmış bir etiket taşınmaz.** `v1.2.0`'ı başka bir commit'e
  çevirmek, onu indirmiş herkesin elindekiyle depodakinin farklı olması
  demek. Hata çıktıysa yeni bir sürüm çıkar: `v1.2.1`.

Dördüncü bölümde gördüğümüz gibi etiket gönderimi bir `push` olayıdır ve
`tags` süzgeciyle yakalanır. Çalışma içinde etiketin adı
`GITHUB_REF_NAME` ortam değişkenindedir (iş akışında
`${{ github.ref_name }}`).

## Etiket ile paket aynı numarayı söylemeli

Sık yapılan bir hata: etiket `v1.2.0`, ama `pyproject.toml`'da hâlâ
`version = "1.1.0"` yazıyor. Yayınlanan paket kendine `1.1.0` der ve pip
onu eski sürüm sanar. Hat bunu derlemeden önce denetlemeli:

```python
import tomllib

PYPROJECT = '[project]\nname = "greeter"\nversion = "0.2.0"\n'


def check_tag(tag, pyproject_text):
    version = tomllib.loads(pyproject_text)["project"]["version"]
    if tag != "v" + version:
        return f"tag {tag} does not match version {version}"
    return "ok"


print(check_tag("v0.2.0", PYPROJECT))
print(check_tag("v0.2.1", PYPROJECT))
```

```text
ok
tag v0.2.1 does not match version 0.2.0
```

Hattaki karşılığı küçük bir betik: `pyproject.toml`'u okur, etiketle
karşılaştırır ve uyuşmazsa sıfırdan farklı bir çıkış koduyla biter; iş
orada düşer, yanlış numaralı paket yayınlanmaz.

## Yayın hattı

Hepsi bir arada: etiket gelince test, numara denetimi, derleme ve GitHub
sürümü.

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: read

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
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python scripts/check_version.py "$GITHUB_REF_NAME"
      - run: python -m pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  release:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
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

- Yalnızca `v` ile başlayan etiketler hattı başlatır; `main`'e gönderim
  başlatmaz.
- Paket bir kez derlenir (`build`), `release` işi aynı dosyaları indirir
  (sekizinci bölüm).
- `release` işinde kod çekilmedi; `gh` hangi depoda çalışacağını
  `--repo` ile öğrenir. `GITHUB_REPOSITORY` `sahip/depo` biçiminde adı
  tutar.
- `--generate-notes`, son sürümden bu yana birleştirilen PR'lardan sürüm
  notunu GitHub'ın kendisine yazdırır.
- Yazma izni yalnızca `release` işinde (dokuzuncu bölüm).

## Paket deposuna (PyPI) yüklemek

`pip install greeter` ile kurulabilmesi için paket **PyPI**'a yüklenir.
Eskiden bunun için kalıcı bir PyPI anahtarı gizli değer olarak saklanırdı.
Bugün önerilen yol **güvenilir yayıncı** (trusted publishing): PyPI'da
"bu deponun bu iş akışı yükleyebilir" diye bir kez tanımlanır; iş her
çalışmada GitHub'dan kısa ömürlü bir kimlik (`id-token`) alır ve onunla
yükler. Saklanacak, sızacak bir anahtar yoktur.

```yaml
  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - uses: pypa/gh-action-pypi-publish@release/v1
```

- `environment: pypi` işi GitHub'daki bir **ortama** (environment) bağlar;
  ortama "yüklemeden önce onay iste" gibi kurallar konabilir (on birinci
  bölüm).
- `id-token: write` kısa ömürlü kimliği almak için gereken tek izin.
- PyPI'a yüklenen bir sürüm numarası **bir daha kullanılamaz**, silinse
  bile. Denemeler için ayrı bir sınama deposu (TestPyPI) var.

## Sırada

Paketi yayınladık. On birinci bölümde bir uygulamayı sunucuya dağıtmanın
yollarını görüyoruz: ortamlar, onay adımları ve bir şey ters giderse geri
dönmek.

## Özet

- Anlamlı sürümleme: `ANA.YAN.YAMA`; uyumsuz değişiklik ANA, yeni özellik
  YAN, düzeltme YAMA. Artan parçanın sağı sıfırlanır.
- Sürümler metin olarak sıralanmaz (`"1.10.0" < "1.9.0"`); sayılara
  çevrilip karşılaştırılır. Python'da `packaging.version.Version`
  `rc`, `b`, `post` eklerini de bilir.
- Commit önekleri (`fix:`, `feat:`, `feat!:`) bir sonraki sürümün hangi
  parçayı artıracağını söyler.
- Sürüm, açıklamalı bir etiketle işaretlenir ve adıyla gönderilir;
  yayınlanmış etiket taşınmaz.
- Hat etiketle başlar (`tags: ["v*"]`), etiketin `pyproject.toml` ile
  aynı numarayı söylediğini denetler, bir kez derler ve yayınlar.
- PyPI'a anahtarsız yüklemek için güvenilir yayıncı ve `id-token: write`.
