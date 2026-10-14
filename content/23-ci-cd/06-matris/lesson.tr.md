# Matris

Kodun yalnızca senin bilgisayarında değil, kullanıcılarının
bilgisayarlarında da çalışması gerekir: başka bir işletim sistemi, başka
bir Python sürümü. Her biri için ayrı bir iş yazmak aynı adımları beş kez
kopyalamak demek. **Matris** (matrix) tek bir iş tanımından, verilen
değerlerin her birleşimi için bir iş üretir.

## Bir iş, birçok kopya

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

- `strategy.matrix` altındaki her anahtar bir **boyut**, listesi o
  boyutun değerleri.
- GitHub her birleşim için işin bir kopyasını çalıştırır: 2 işletim
  sistemi × 2 Python sürümü = **4 iş**.
- Kopyanın içinde o anki değer `${{ matrix.os }}`,
  `${{ matrix.python-version }}` ile okunur. `runs-on` da matristen
  gelebilir.

Birleşimleri Python'la üretelim. Kartezyen çarpım (her değer her değerle)
`itertools.product` ile:

```python
from itertools import product

matrix = {
    "os": ["ubuntu-latest", "windows-latest"],
    "python-version": ["3.12", "3.13"],
}

keys = list(matrix)
combos = [dict(zip(keys, values)) for values in product(*matrix.values())]
for combo in combos:
    print("test (" + ", ".join(combo.values()) + ")")
print(len(combos), "jobs")
```

```text
test (ubuntu-latest, 3.12)
test (ubuntu-latest, 3.13)
test (windows-latest, 3.12)
test (windows-latest, 3.13)
4 jobs
```

GitHub'ın Actions sekmesinde işler tam da bu adlarla görünür:
`test (ubuntu-latest, 3.12)`. Hangi birleşimin düştüğü adından okunur.

İş sayısı boyutların uzunluklarının **çarpımıdır**: 3 işletim sistemi ve
4 Python sürümü 12 iş eder; bir boyut daha eklemek sayıyı katlar. GitHub
bir matristen en fazla 256 iş üretir, ama sınıra gelmeden çok önce
maliyet sorun olur.

## exclude ve include

Her birleşim gerekli olmayabilir. İki anahtar matrisi düzeltir:

<figure class="fig versus">
  <div><h4>exclude</h4>Listedeki girdiye uyan birleşimleri <b>çıkarır</b>. Girdi tam birleşim olmak zorunda değil: <code>os: windows-latest</code> tek başına bütün Windows işlerini çıkarır.</div>
  <div><h4>include</h4>Girdi var olan birleşimlere uyuyorsa onlara <b>yeni anahtar ekler</b>; hiçbirine uymuyorsa <b>yeni bir birleşim</b> olarak eklenir.</div>
  <figcaption>GitHub önce exclude'u, sonra include'u uygular.</figcaption>
</figure>

```yaml
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.12", "3.13"]
        exclude:
          - os: windows-latest
            python-version: "3.12"
        include:
          - os: windows-latest
            slow: true
          - os: ubuntu-latest
            python-version: "3.14"
            experimental: true
```

Bu iki kuralı Python'la yazalım. Basitleştirilmiş bir model: bir
`include` girdisi, matrisin **asıl** anahtarlarındaki değerleri bir
birleşimle aynıysa o birleşime eklenir:

```python
def apply(combos, keys, exclude, include):
    result = [combo for combo in combos
              if not any(all(combo[k] == v for k, v in rule.items())
                         for rule in exclude)]
    for extra in include:
        fits = [combo for combo in result
                if all(combo[k] == v for k, v in extra.items() if k in keys)]
        if fits:
            for combo in fits:
                combo.update(extra)
        else:
            result.append(dict(extra))
    return result


exclude = [{"os": "windows-latest", "python-version": "3.12"}]
include = [{"os": "windows-latest", "slow": True},
           {"os": "ubuntu-latest", "python-version": "3.14", "experimental": True}]
for combo in apply(combos, keys, exclude, include):
    print(combo)
```

```text
{'os': 'ubuntu-latest', 'python-version': '3.12'}
{'os': 'ubuntu-latest', 'python-version': '3.13'}
{'os': 'windows-latest', 'python-version': '3.13', 'slow': True}
{'os': 'ubuntu-latest', 'python-version': '3.14', 'experimental': True}
```

- `exclude` Windows + 3.12'yi çıkardı: 4 → 3.
- İlk `include` girdisi (`os: windows-latest`) kalan Windows işine uydu
  ve ona `slow: True` ekledi; yeni iş açmadı.
- İkinci girdinin `python-version: "3.14"` değeri hiçbir birleşimde
  yok: uyamadığı için **yeni bir iş** oldu. 3 → 4.

`include` ile eklenen bir anahtar (`experimental`, `slow`) matristeki öbür
değerler gibi okunur: `${{ matrix.experimental }}`. Eklenmediği işlerde
boştur.

## Deneme sürümü: düşebilir

Python'un henüz çıkmamış sürümünü denemek iyi bir erken uyarıdır, ama o
iş düşünce hat kırmızı olmamalı. Beşinci bölümdeki
`continue-on-error`, matristen gelen değerle yalnızca deneme işine
uygulanır:

```yaml
  test:
    runs-on: ${{ matrix.os }}
    continue-on-error: ${{ matrix.experimental == true }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest]
        python-version: ["3.12", "3.13"]
        include:
          - os: ubuntu-latest
            python-version: "3.14"
            experimental: true
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: python -m pytest
```

`experimental` yalnızca 3.14 işinde `true`; öbür işlerde boş olduğu için
koşul yanlış, onlar düşerse hat düşer.

## fail-fast ve max-parallel

<figure class="fig anat">
  <div class="anat-row"><span><code>fail-fast</code></span><span>Varsayılan <code>true</code>: matristeki bir iş düşünce süren ve sırada bekleyen öbür işler iptal edilir. <code>false</code> ise hepsi sonuna kadar çalışır.</span></div>
  <div class="anat-row"><span><code>max-parallel</code></span><span>Aynı anda en fazla kaç işin çalışacağı. Yazılmazsa GitHub elinden geldiğince çok iş başlatır.</span></div>
</figure>

`fail-fast: true` makine dakikası kazandırır; ama bir hata yalnızca
Windows'ta mı, her yerde mi, bunu öğrenmeden işler durur. Hatanın hangi
birleşimlerde olduğunu görmek istiyorsan `fail-fast: false`.

## Süre ve maliyet

Matris iki farklı süreyi ayırır: **duvar saati** (hattın başından sonuna
geçen süre) ve **makine dakikası** (bütün makinelerin harcadığı süre
toplamı). Her test işi 6 dakika sürsün:

```python
import math

jobs = 6
minutes = 6
print("machine minutes:", jobs * minutes)
for limit in (None, 2):
    parallel = jobs if limit is None else limit
    rounds = math.ceil(jobs / parallel)
    print("max-parallel", limit, "-> wall clock", rounds * minutes, "min")
```

```text
machine minutes: 36
max-parallel None -> wall clock 6 min
max-parallel 2 -> wall clock 18 min
```

Matris duvar saatini kısa tutar (işler aynı anda) ama makine dakikası
iş sayısıyla büyür. Herkese açık depolarda GitHub'ın standart makineleri
ücretsizdir; özel depolarda aylık bir dakika hakkı vardır ve Windows ile
macOS dakikaları Linux'tan daha pahalı sayılır. Bu yüzden matris
genellikle şöyle kurulur: bütün Python sürümleri Linux'ta, öbür işletim
sistemleri yalnızca bir sürümle.

## Hangi değerler?

- **Python sürümleri:** desteklediğini söylediğin en eski ve en yeni
  sürüm en azından. Arada bir sürüm kırılırsa onu da ekle.
- **İşletim sistemleri:** kullanıcıların gerçekten kullandıkları. Dosya
  yolları, satır sonları, büyük-küçük harf duyarlılığı gibi farklar
  genellikle Windows'ta çıkar.
- **Sürümleri tırnakla yaz:** `["3.12", "3.13"]`. Üçüncü bölümdeki tuzak
  matriste de geçerli: `3.10` tırnaksız `3.1` olur.

## Özet

- `strategy.matrix`: her anahtar bir boyut; iş sayısı boyutların
  çarpımı. Değer `${{ matrix.<ad> }}` ile okunur.
- İş adları birleşimi gösterir: `test (ubuntu-latest, 3.12)`.
- `exclude` uyan birleşimleri çıkarır; `include` uyan birleşime anahtar
  ekler, uymayanı yeni iş yapar. Önce exclude, sonra include.
- `fail-fast` varsayılan `true`; hatanın yerini görmek için `false`.
- `continue-on-error: ${{ matrix.experimental == true }}` yalnızca deneme
  işini serbest bırakır.
- Duvar saati kısalır, makine dakikası iş sayısıyla büyür.
