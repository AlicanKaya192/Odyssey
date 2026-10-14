# Artifact ve Paketleme

Şimdiye kadar hattımız bir **karar** üretti: testler geçti ya da
düştü. Ama hattın bir de **ürünü** olabilir: kurulabilir bir paket, bir
test raporu, bir kapsam (coverage) raporu. Bu dosyalar işin makinesiyle
birlikte kaybolur; beşinci bölümde gördük, işler dosya paylaşmaz. Bu
bölümde hattın ürettiği dosyaları saklamayı (**artifact**), işler arasında
taşımayı ve bir Python projesini kurulabilir bir pakete dönüştürmeyi
görüyoruz.

## Artifact nedir?

**Artifact**, bir çalışmanın ürettiği ve GitHub'da saklanan dosya ya da
klasördür. Çalışmanın sayfasından zip olarak indirilebilir ve aynı
çalışmadaki başka bir iş tarafından alınabilir. İki eylemle çalışılır:

```yaml
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

```yaml
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
```

- `upload-artifact`: `path` klasörünü (ya da dosyalarını) `name` adıyla
  saklar.
- `download-artifact`: o adla saklananı bu işin makinesine, `path`
  klasörüne indirir. `name` yazılmazsa çalışmanın bütün artifact'leri
  iner.

Önbellekle karıştırılmasın:

<figure class="fig versus">
  <div><h4>Önbellek</h4>Hız için. Anahtarla bulunur, çalışmalar arasında paylaşılır, kaybolabilir; olmasa da iş doğru çalışmalı.</div>
  <div><h4>Artifact</h4>Ürün için. Bir çalışmaya aittir, adla bulunur, sayfadan indirilebilir; saklama süresi bitene kadar durur.</div>
  <figcaption>Önbellek "yeniden indirmeyelim", artifact "bunu saklayalım" der.</figcaption>
</figure>

Artifact'ler varsayılan olarak 90 gün saklanır; `retention-days` ile
kısaltılabilir. Saklanan her bayt deponun depolama kotasından düşer (özel
depolarda); test raporu gibi kısa ömürlü dosyalara birkaç gün yeter.

## Python paketi: tekerlek

Bir Python projesini başkasının `pip install` ile kurabileceği hâle
getirmeye **paketleme** denir. Projenin adı, sürümü ve nasıl
derleneceği `pyproject.toml` dosyasına yazılır:

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "greeter"
version = "0.1.0"
```

Derlemenin ürünü bir **tekerlek** (wheel) dosyasıdır: `.whl` uzantılı,
içinde paketin dosyaları ve bilgileri olan bir zip. Küçük bir proje kurup
tekerleğini gerçekten derleyelim ve içine bakalım. Bu bilgisayar
internetsiz çalıştığı için derlemeyi pip'in kendi tekerlek komutuyla
yapıyoruz; GitHub'daki hatlarda bunun yerine genellikle
`python -m build` kullanılır, ürün aynı biçimdedir.

```python
import subprocess
import sys
import zipfile
from pathlib import Path

project = Path("greeter-project")
(project / "greeter").mkdir(parents=True)
(project / "greeter" / "__init__.py").write_text(
    'def hello():\n    return "Hello from greeter"\n')
(project / "pyproject.toml").write_text(
    '[build-system]\nrequires = ["setuptools"]\n'
    'build-backend = "setuptools.build_meta"\n\n'
    '[project]\nname = "greeter"\nversion = "0.1.0"\n')

subprocess.run([sys.executable, "-m", "pip", "wheel", ".", "--no-deps",
                "--no-build-isolation", "-w", "dist", "-q"],
               cwd=project, check=True)
wheel = next((project / "dist").iterdir())
print(wheel.name)
for name in sorted(zipfile.ZipFile(wheel).namelist()):
    print("  " + name)
```

```text
greeter-0.1.0-py3-none-any.whl
  greeter-0.1.0.dist-info/METADATA
  greeter-0.1.0.dist-info/RECORD
  greeter-0.1.0.dist-info/WHEEL
  greeter-0.1.0.dist-info/top_level.txt
  greeter/__init__.py
```

Dosyanın adı kendi bilgisini taşır:

<figure class="fig anat">
  <div class="anat-row"><span><code>greeter</code></span><span>Paketin adı.</span></div>
  <div class="anat-row"><span><code>0.1.0</code></span><span>Sürüm (onuncu bölümde).</span></div>
  <div class="anat-row"><span><code>py3</code></span><span>Hangi Python: her Python 3.</span></div>
  <div class="anat-row"><span><code>none</code></span><span>C eklentisi yok, Python'un iç yapısına bağlı değil.</span></div>
  <div class="anat-row"><span><code>any</code></span><span>Her işletim sisteminde çalışır.</span></div>
</figure>

İçinde kodun kendisi (`greeter/__init__.py`) ve `dist-info` klasöründe
paketin bilgileri var: `METADATA` adı ve sürümü, `RECORD` her dosyanın
özetini (kurulumda dosyaların bozulmadığı buradan denetlenir).

## Kurulunca çalışıyor mu?

Testler geçti diye paket de doğrudur denemez: bir dosya pakete girmemiş
olabilir, kod yalnızca proje klasöründen çalıştırılınca bulunan bir şeye
dayanıyor olabilir. **Duman testi** (smoke test) paketi temiz bir yere
kurup en temel işini yapıyor mu diye bakar. Yukarıdaki tekerleği boş bir
klasöre kurup oradan içe aktaralım:

```python
target = Path("clean-install")
subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "-q",
                "--target", str(target), str(wheel)], check=True)
result = subprocess.run(
    [sys.executable, "-c", "import greeter; print(greeter.hello())"],
    cwd=target, capture_output=True, text=True)
print(result.stdout.strip())
print(sorted(path.name for path in target.iterdir()))
```

```text
Hello from greeter
['greeter', 'greeter-0.1.0.dist-info']
```

Paket, proje klasörünün dışında, yalnızca kurulan dosyalardan çalıştı.
Hattaki karşılığı ayrı bir iştir: tekerleği artifact olarak alır, temiz
makineye kurar ve bir komut dener.

## Bir kez derle, aynısını kullan

Hattın önemli bir kuralı: **paket bir kez derlenir; test edilen, dağıtılan
ve yayınlanan hep o dosyadır.** Her işte yeniden derlemek, test edilen
dosyayla yayınlanan dosyanın farklı olma ihtimalini açar (bu arada bir
bağımlılık yeni sürüm çıkarmış olabilir). Artifact bunu sağlar: derleme
işi yükler, öbür işler indirir.

Taşınan dosyanın değişmediğini **SHA-256 özeti** gösterir. Yayınlanan
paketlerin yanında bu yüzden özetleri de verilir:

```python
import hashlib


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


original = sha256_of(wheel)
copy = Path("downloaded.whl")
copy.write_bytes(wheel.read_bytes())
print("same file:   ", sha256_of(copy) == original)

data = bytearray(copy.read_bytes())
data[100] ^= 1
copy.write_bytes(bytes(data))
print("one bit flip:", sha256_of(copy) == original)
```

```text
same file:    True
one bit flip: False
```

Tek bir bitin değişmesi bile özeti bambaşka yapar.

## Hatta paketleme

```yaml
name: Package

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
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
          retention-days: 7
  smoke-test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: pip install dist/*.whl
      - run: python -c "import greeter; print(greeter.hello())"
```

- `python -m build`, `dist/` klasörüne tekerleği ve kaynak paketini
  (`.tar.gz`) yazar.
- `smoke-test` işinde `checkout` **yok**: kodu değil, yalnızca paketi
  kullanıyor. Paket eksik bir dosya yüzünden bozuksa burada ortaya çıkar.

## Test raporunu saklamak

Testler düşünce ayrıntı kayıtta kalır, ama uzun bir kaydı kaydırmak zor.
pytest sonucu bir dosyaya da yazabilir; o dosya artifact olarak saklanır.
Önemli olan, testler **düşünce de** saklamaktır; yoksa en çok gereken
anda rapor olmaz. Beşinci bölümdeki `always()` adım düzeyinde de çalışır:

```yaml
      - run: python -m pytest --junitxml=report.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-report
          path: report.xml
          retention-days: 14
```

Bir çalışmada aynı adla iki artifact yüklenemez. Matriste her iş kendi
raporunu yüklüyorsa ad matristen gelir: `name: report-${{ matrix.os }}`.

## Sırada

Paketi derledik, test ettik, sakladık. Onu bir sürüm numarasıyla
**yayınlamak** (GitHub sürümü, paket deposu) yetki ve gizli değer ister;
bunlar dokuzuncu (gizli değerler) ve onuncu (sürümleme) bölümlerde.

## Özet

- Artifact bir çalışmanın ürettiği, saklanan dosyadır;
  `upload-artifact` / `download-artifact` ile işler arasında taşınır.
- Önbellek hız içindir, artifact ürün içindir.
- `pyproject.toml` paketi tanımlar; ürün `.whl` tekerleğidir (bir zip).
  Adı: ad, sürüm, Python, ABI, platform.
- Duman testi paketi temiz bir yere kurup dener.
- Bir kez derle; test edilen ve yayınlanan aynı dosya olsun. SHA-256
  özeti dosyanın değişmediğini gösterir.
- Raporu `if: always()` ile sakla; matriste adı matristen al.
