# İş Akışı Dosyasının Anatomisi

İlk bölümde bir iş akışı dosyasının iskeletini gördük: **ne zaman** (`on`),
**nerede** (`runs-on`), **ne** (`steps`). Bu bölümde dosyayı parça parça
açıyoruz: YAML'ın kuralları, bir işin ve bir adımın alabileceği ayarlar,
çok satırlı komutlar, ortam değişkenleri ve YAML'ın sık düşülen tuzakları.

## YAML'ın üç kuralı

İş akışı dosyası **YAML** ile yazılır. YAML, iç içe veriyi az işaretle
yazmak için tasarlanmış bir biçim. Bütün dosyayı üç kural taşıyor:

1. **Anahtar ve değer:** `runs-on: ubuntu-latest`. İki noktadan sonra bir
   boşluk.
2. **Liste:** her eleman `-` ile başlar. Adımlar bir liste.
3. **Girinti iç içeliği gösterir:** bir anahtarın altındaki her şey ondan
   daha içeride başlar. Girinti **boşlukla** yapılır, sekme (Tab) karakteri
   kullanılmaz. Genelde iki boşluk.

Python'un YAML okuyucusu (PyYAML) bir iş akışını nasıl okuyor, görelim.
Sonucu daha kolay okunsun diye JSON biçiminde yazdırıyoruz:

```python
import json

import yaml

text = """
name: CI
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -m pytest
"""
data = yaml.safe_load(text)
print(json.dumps(data, indent=2))
```

```text
{
  "name": "CI",
  "jobs": {
    "test": {
      "runs-on": "ubuntu-latest",
      "steps": [
        {
          "uses": "actions/checkout@v4"
        },
        {
          "run": "python -m pytest"
        }
      ]
    }
  }
}
```

Dosya bir **sözlükler ve listeler ağacı**: `jobs` bir sözlük, içinde
`test` bir sözlük, onun `steps`'i bir liste ve listenin her elemanı yine
bir sözlük. GitHub da dosyayı bu ağaç olarak okur. Girintiyi bir boşluk
kaydırmak, bir anahtarı ağacın başka bir dalına taşır; bu yüzden YAML'da
girinti hatası en sık yapılan hatadır.

## Dosyanın üst düzeyi

<figure class="fig anat">
  <div class="anat-row"><span><code>name</code></span><span>İş akışının adı. GitHub'daki listede görünür. Yazılmazsa dosya yolu görünür.</span></div>
  <div class="anat-row"><span><code>on</code></span><span>Tetikleyiciler: iş akışını hangi olaylar başlatır (dördüncü bölüm).</span></div>
  <div class="anat-row"><span><code>env</code></span><span>Bütün işlerde geçerli ortam değişkenleri.</span></div>
  <div class="anat-row"><span><code>jobs</code></span><span>İşler. Her işin adı kendi anahtarı (<code>test</code>, <code>lint</code>...).</span></div>
</figure>

Bir depoda birden çok iş akışı dosyası olabilir; `.github/workflows/`
klasöründeki her `.yml` ya da `.yaml` dosyası ayrı bir iş akışıdır.

## Bir iş

Her iş kendi temiz makinesinde çalışır. Sık kullanılan ayarlar:

<figure class="fig anat">
  <div class="anat-row"><span><code>runs-on</code></span><span>Makine: <code>ubuntu-latest</code>, <code>windows-latest</code> ya da <code>macos-latest</code>. Zorunlu.</span></div>
  <div class="anat-row"><span><code>name</code></span><span>Ekranda görünecek ad (işin anahtarından farklı olabilir).</span></div>
  <div class="anat-row"><span><code>env</code></span><span>Yalnızca bu işin adımlarında geçerli ortam değişkenleri.</span></div>
  <div class="anat-row"><span><code>timeout-minutes</code></span><span>İş bu kadar dakikadan uzun sürerse durdurulur. Takılıp kalan bir test hattı saatlerce meşgul etmesin.</span></div>
  <div class="anat-row"><span><code>steps</code></span><span>Adımların listesi. Zorunlu.</span></div>
</figure>

Makine seçimi komutların nasıl çalışacağını da değiştirir: Linux ve macOS
makinelerinde `run` komutları **bash** kabuğunda, Windows makinesinde
**PowerShell**'de çalışır. Aynı komut iki kabukta farklı davranabilir;
bu yüzden çoğu proje testlerini Linux'ta çalıştırır.

## Bir adım

<figure class="fig anat">
  <div class="anat-row"><span><code>name</code></span><span>Adımın ekrandaki adı. Kayıtlarda hangi adımın düştüğünü bulmayı kolaylaştırır.</span></div>
  <div class="anat-row"><span><code>uses</code></span><span>Hazır bir eylem, sürümüyle: <code>actions/checkout@v4</code>.</span></div>
  <div class="anat-row"><span><code>with</code></span><span>Eyleme verilen ayarlar.</span></div>
  <div class="anat-row"><span><code>run</code></span><span>Çalışacak komut ya da komutlar.</span></div>
  <div class="anat-row"><span><code>env</code></span><span>Yalnızca bu adımda geçerli ortam değişkenleri.</span></div>
  <div class="anat-row"><span><code>working-directory</code></span><span><code>run</code> komutunun hangi klasörde çalışacağı.</span></div>
</figure>

Bir adımda ya `uses` ya `run` olur, ikisi birden olmaz.

## Çok satırlı komut

Bir adımda birden çok komut çalıştırmak için `run: |` yazılır. `|`
işareti "alttaki satırları olduğu gibi al" demek; her satır sırayla
çalışır ve biri hata verirse adım düşer:

```yaml
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
```

## Ortam değişkenleri ve düzeyleri

**Ortam değişkeni** (environment variable), programlara dışarıdan
verilen adlı bir değerdir. Docker patikasında gördüğümüz `-e` ve
`environment:` ile aynı fikir. İş akışında üç düzeyde yazılabilir:

<figure class="fig versus">
  <div><h4>İş akışı</h4>Üst düzeyde <code>env:</code>. Bütün işlerde ve adımlarda geçerli.</div>
  <div><h4>İş</h4>İşin altında <code>env:</code>. O işin bütün adımlarında geçerli.</div>
  <div><h4>Adım</h4>Adımın altında <code>env:</code>. Yalnızca o adımda geçerli.</div>
  <figcaption>Aynı ad birden çok düzeyde yazılırsa adıma en yakın olan kazanır.</figcaption>
</figure>

Bir `run` komutunun içinde değişken, kabuğun yazımıyla okunur: bash'te
`$APP_ENV`. Komutun dışında, örneğin bir `with` değerinde, iş akışının
**ifade** (expression) yazımı kullanılır: `${{ env.APP_ENV }}`. İfadeleri
sonraki bölümlerde sık göreceğiz.

Hepsi bir arada:

```yaml
name: CI

on: push

env:
  APP_ENV: ci

jobs:
  test:
    name: Run the tests
    runs-on: ubuntu-latest
    timeout-minutes: 10
    env:
      APP_ENV: test
    steps:
      - name: Get the code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest
        env:
          PYTEST_ADDOPTS: "-q"
```

`test` işinin adımlarında `APP_ENV` değeri `test`: iş düzeyindeki değer
iş akışı düzeyindekini ezer. `PYTEST_ADDOPTS` yalnızca son adımda var.

## YAML tuzakları

YAML az işaretle yazıldığı için bazı değerler sandığın türde okunmaz.
PyYAML ile ölçtük:

```python
import yaml

print(yaml.safe_load("version: 3.10"))
print(yaml.safe_load('version: "3.10"'))
print(yaml.safe_load("on: push"))
```

```text
{'version': 3.1}
{'version': '3.10'}
{True: 'push'}
```

- **`3.10` bir sayı olarak okunur ve `3.1` olur.** Python sürümünü
  tırnaksız yazmak bu yüzden Python 3.1'i ister. Sürüm her zaman tırnakla
  yazılır: `"3.10"`.
- **`on` kelimesi** PyYAML'da (YAML'ın 1.1 sürümünün kuralları) `True`
  olarak okunur. GitHub'ın kendi okuyucusu `on`'u doğru anlar; ama bir iş
  akışı dosyasını Python'la işleyen kendi aracını yazarsan bunu hesaba
  katman gerekir.

Ve sekme karakteri:

```python
import yaml

try:
    yaml.safe_load("jobs:\n\ttest: 1")
except yaml.YAMLError as error:
    print(type(error).__name__)
    print(error.problem)
```

```text
ScannerError
found character '\t' that cannot start any token
```

Editörün Tab tuşuna basınca boşluk mu sekme mi yazdığına dikkat et;
Odyssey'in editörü boşluk yazıyor.

## GitHub'da bir çalıştırma

Dosya depoya gönderilince GitHub'daki deponun **Actions** sekmesinde
görünür. Her çalıştırma bir satırdır; içine girince işler, her işin içinde
de adımlar listelenir. Her adımın kaydı (log) ayrı açılır; düşen adım
kırmızıyla işaretlenir ve kaydının sonunda hata mesajı durur. Adımlara
`name` vermenin asıl faydası burada görünür: "Run tests" adımının
düştüğünü görmek, "Run python -m pytest" satırını aramaktan kolaydır.

## Özet

- YAML: `anahtar: değer`, `-` ile liste, iç içelik boşlukla girinti.
  Dosya bir sözlükler ve listeler ağacıdır.
- Üst düzey: `name`, `on`, `env`, `jobs`. İş: `runs-on`, `name`, `env`,
  `timeout-minutes`, `steps`. Adım: `name`, `uses` + `with` ya da `run`,
  `env`, `working-directory`.
- `run: |` birden çok komutu sırayla çalıştırır.
- Ortam değişkenleri üç düzeyde; adıma en yakın olan kazanır.
- Sürümleri tırnakla yaz (`"3.10"`); girintide sekme kullanma.
