Terminalde `activate` yazman **editörü etkilemiyor.** VS Code'un "Çalıştır"
düğmesi ya da Jupyter'in hücreleri, kendilerine hangi Python seçildiyse onunla
çalışıyor. Terminalde her şey doğru olduğu hâlde editörde
`ModuleNotFoundError` almanın en sık sebebi bu.

Kural: **ortamı kurduktan sonra editöre de söyle.**

## VS Code

Önce Microsoft'un **Python** eklentisinin kurulu olması gerekiyor
(Eklentiler bölmesinde "Python" ara).

### Yorumlayıcıyı seçmek

1. `Ctrl` + `Shift` + `P` ile komut paletini aç.
2. **Python: Select Interpreter** yaz ve seç.
3. Listeden projenin ortamını seç: `.venv` için `('.venv': venv)`, conda için
   ortamın adı.

Seçilen yorumlayıcı pencerenin sağ alt köşesinde yazıyor. Tıklayınca yeniden
seçebiliyorsun.

Proje klasöründeki `.venv` listede yoksa **Enter interpreter path** seçeneğiyle
doğrudan dosyayı göster:

```text
.venv\Scripts\python.exe
```

### Ortamı VS Code içinden kurmak

Komut paletinde **Python: Create Environment**: `Venv` ya da `Conda` seç,
Python sürümünü seç; varsa `requirements.txt`'yi de kurmayı öneriyor. Sonuç,
terminalde yazacağın komutlarla aynı.

### VS Code'un terminali

Yorumlayıcıyı seçtikten sonra VS Code'da açtığın **yeni** terminal ortamı
kendiliğinden etkinleştiriyor; başında `(.venv)` görünüyor. Seçimden önce
açılmış bir terminal eski hâlinde kalır: onu kapatıp yenisini aç.

## Jupyter

Jupyter'de hücreleri çalıştıran şeye **çekirdek** (kernel) deniyor. Çekirdek
bir Python yorumlayıcısı; hangi ortamdaysa o ortamın paketlerini görüyor.

### Ortamı çekirdek olarak kaydetmek

Ortam etkinken:

```text
python -m pip install ipykernel
python -m ipykernel install --user --name proje-a --display-name "Proje A"
```

Artık Jupyter'in çekirdek listesinde "Proje A" var. Kayıtlı çekirdekleri
görmek ve silmek:

```text
jupyter kernelspec list
jupyter kernelspec uninstall proje-a
```

VS Code'da not defteri (`.ipynb`) açınca sağ üstteki **Select Kernel**
düğmesinden ortamı seçiyorsun; `ipykernel` kurulu değilse VS Code kurmayı
öneriyor. Tarayıcıdaki Jupyter'de menüden **Kernel → Change Kernel**.

### Not defterinde paket kurmak

Hücrede `%pip` yaz, `!pip` değil:

```text
%pip install pandas
```

`%pip`, paketi **not defterini çalıştıran çekirdeğin** ortamına kuruyor.
`!pip` ise terminal komutu çalıştırıyor ve `PATH`'te önce hangi pip varsa ona
gidiyor; paket başka bir Python'a kurulabiliyor. conda ortamında da aynısı:
`%conda install`.

Kurduktan sonra çekirdeği yeniden başlat (**Restart**); çalışan çekirdek yeni
paketi her zaman hemen görmüyor.

## PyCharm

**Settings → Project → Python Interpreter → Add Interpreter**: burada yeni bir
`Virtualenv` ortamı kurabilir ya da var olan bir `.venv` veya conda ortamını
seçebilirsin. PyCharm yeni projede genellikle kendiliğinden bir `.venv`
açıyor.

## Hangi Python'dayım?

Editör ne derse desin, cevabı kod veriyor. Bir hücreye ya da dosyaya yaz:

```python
import sys
print(sys.executable)
```

Çıkan yol projenin ortamını (`...\proje-a\.venv\Scripts\python.exe` ya da
`...\envs\proje-a\python.exe`) göstermiyorsa editör yanlış yorumlayıcıda.
