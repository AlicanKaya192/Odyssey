# Kütüphane Kurmak

`math` ve `datetime` Python'la birlikte geliyor. Ama `pandas`, `numpy`,
`requests` gelmiyor — onları kurman gerekiyor.

Bu not o işi anlatıyor. Veri Bilimi patikasına geçtiğinde ilk yapacağın şey
bu olacak.

## `pip` nedir?

`pip`, Python'un paket yöneticisi. Python'la birlikte kuruluyor. Terminale
yazıyorsun:

```bash
pip install pandas
```

Kütüphaneyi internetten indirip bilgisayarına kuruyor. Sonra kodunda
kullanabiliyorsun:

```python
import pandas
```

Sık kullanacağın komutlar:

| Komut | Ne yapar |
|---|---|
| `pip install ad` | Kurar |
| `pip install ad==2.1.0` | Belirli bir sürümü kurar |
| `pip install --upgrade ad` | Günceller |
| `pip uninstall ad` | Kaldırır |
| `pip list` | Kurulu olanları listeler |
| `pip show ad` | Sürümünü ve nereye kurulduğunu gösterir |

## Terminal nerede?

- **Windows:** Başlat menüsüne `cmd` ya da `powershell` yaz.
- **VS Code içinde:** `Ctrl` + `` ` `` (üstteki ters tırnak tuşu).

Komut çalışmıyorsa `pip` yerine şunu dene:

```bash
python -m pip install pandas
```

Bu yazım daha güvenilir: "şu anda `python` dediğim yorumlayıcının `pip`'ini
kullan" demek. Bilgisayarda birden fazla Python varsa fark ediyor.

## Asıl mesele: sanal ortam

Bir sorun var. Kütüphaneleri doğrudan kurunca hepsi **aynı yere** gidiyor:

<figure class="fig">
  <div class="flow">
    <span class="node no"><b>Proje A</b><br>pandas 1.5 ister</span>
    <span class="arrow">→</span>
    <span class="node"><b>Tek Python</b><br>tek pandas sürümü</span>
    <span class="arrow">←</span>
    <span class="node no"><b>Proje B</b><br>pandas 2.1 ister</span>
  </div>
  <figcaption>İki proje farklı sürüm istediğinde birini kurmak diğerini bozuyor. Sanal ortam her projeye kendi kütüphane klasörünü veriyor.</figcaption>
</figure>

**Sanal ortam**, proje klasörünün içinde duran ayrı bir Python kurulumu. O
projede kurduğun her şey oraya gidiyor, dışarıyı etkilemiyor.

### Kurmak

Proje klasöründe:

```bash
python -m venv .venv
```

`.venv` adında bir klasör oluşuyor. İçinde projenin kendi Python'u var.

### Etkinleştirmek

```bash
.venv\Scripts\activate
```

Terminalin başında `(.venv)` yazısı beliriyor — artık o ortamdasın. Bundan
sonra `pip install` yaptığın her şey oraya kuruluyor.

Çıkmak için:

```bash
deactivate
```

### Neden her seferinde?

Yeni bir terminal açtığında ortam etkin değil. Yeniden etkinleştirmen
gerekiyor. VS Code klasördeki `.venv`'i genelde kendisi buluyor ve seçiyor.

## `requirements.txt`

Projenin hangi kütüphaneleri kullandığını bir dosyada tutuyorsun:

```
pandas==2.1.0
numpy==1.26.0
```

Kurulu olanları bu dosyaya yazmak:

```bash
pip freeze > requirements.txt
```

Başka bir bilgisayarda hepsini birden kurmak:

```bash
pip install -r requirements.txt
```

Bu, projeni paylaştığında karşı tarafın "hangi kütüphaneler gerekiyordu"
diye sormasını engelliyor.

## Sık karşılaşılan hatalar

**`ModuleNotFoundError: No module named 'pandas'`**

Kütüphane kurulu değil ya da **yanlış ortamda** kurulu. Önce ortamı
etkinleştir, sonra kur. En sık sebebi bu: kurulum bir terminalde, çalıştırma
başka bir ortamda yapılıyor.

**`pip is not recognized`**

`pip` yolda bulunamıyor. `python -m pip install ...` yazımını kullan.

**`Permission denied`**

Sistem Python'una kurmaya çalışıyorsun. Sanal ortam kur, sorun kalkıyor.
Yönetici olarak çalıştırmak da işe yarıyor ama **doğru çözüm değil** — sistem
Python'unu kirletiyor.

## Özet

- Standart kütüphane dışındaki her şey `pip install` ile kuruluyor.
- Komut çalışmazsa `python -m pip install` daha güvenilir.
- **Her proje için sanal ortam kur.** İki proje farklı sürüm istediğinde
  tek çözüm bu.
- `python -m venv .venv` kurar, `.venv\Scripts\activate` etkinleştirir.
- `requirements.txt` projenin ihtiyaçlarını kayda geçirir.
- `ModuleNotFoundError` genelde "yanlış ortamdasın" demek.
