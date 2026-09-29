# Paketler ve Ortamlar

Bu uygulamada kod yazarken hiçbir şey kurman gerekmiyor; alıştırmalar
uygulamanın içinde çalışıyor. Ama kendi bilgisayarında ilk projeni açtığın
gün karşına çıkan ilk engel genellikle kodun kendisi olmuyor, **kurulum**
oluyor:

- `pip` komutu tanınmıyor.
- Kurduğun kütüphane için `ModuleNotFoundError` alıyorsun.
- Arkadaşının bilgisayarında çalışan proje seninkinde çalışmıyor.

Üçünün de sebebi aynı: **hangi Python'un, hangi paketlerle çalıştığını**
bilmemek. Bu bölüm tam olarak bunu anlatıyor. Buradaki komutları ezbere
bilmelisin; kendi bilgisayarında açtığın her projede kullanacaksın.

Henüz tek satır Python yazmadıysan endişelenme. Bu bölümde kod yazmıyoruz,
Python'un bilgisayarında nasıl yaşadığını öğreniyoruz. Komutların kısa listesi
"Komut Kartı" notunda.

## Önce birkaç kelime

<figure class="fig anat">
  <div class="anat-row"><span>Yorumlayıcı</span><span>Kodunu okuyup çalıştıran program. Windows'ta <code>python.exe</code>. "Python kurdum" dediğinde kurduğun şey bu.</span></div>
  <div class="anat-row"><span>Modül</span><span>Tek bir <code>.py</code> dosyası. <code>import</code> ile başka bir dosyadan çağrılabiliyor.</span></div>
  <div class="anat-row"><span>Paket</span><span>Modüllerin bir araya getirildiği klasör. pandas bir paket; içinde yüzlerce modül var.</span></div>
  <div class="anat-row"><span>Kütüphane</span><span>Günlük dilde paketle aynı anlamda kullanılıyor: başkasının yazıp paylaştığı hazır kod.</span></div>
  <div class="anat-row"><span>PyPI</span><span>Python Package Index (<code>pypi.org</code>). Yüz binlerce paketin durduğu ortak depo. <code>pip</code> paketleri buradan indiriyor.</span></div>
  <div class="anat-row"><span>Ortam</span><span>Bir yorumlayıcı ve ona kurulmuş paketlerin tamamı. Bu bölümün asıl konusu.</span></div>
  <figcaption>Bu altı kelimeyi birbirinden ayırabiliyorsan bölümün geri kalanı kolay.</figcaption>
</figure>

## Bilgisayarında hangi Python var?

Terminali aç (Başlat menüsüne `cmd` ya da `powershell` yaz) ve şunları dene:

```text
python --version
where python
```

İlki sürümü, ikincisi `python` yazınca **hangi dosyanın** çalıştığını
gösteriyor. macOS ve Linux'ta `where` yerine `which python` yazılıyor.

`where python` birden fazla satır gösterebilir. Bu şaşırtıcı değil: Python
python.org'dan, Microsoft Store'dan, Anaconda'dan ya da başka bir programın
içinden gelmiş olabilir. **Çalışan, listedeki ilk satırdır.** Windows komutu
`PATH` denen bir klasör listesinde sırayla arıyor ve bulduğu ilk
`python.exe`'yi çalıştırıyor.

Windows'ta python.org kurulumuyla bir de `py` başlatıcısı geliyor. Kurulu
bütün sürümleri o gösteriyor:

```text
py --list
py -3.12 --version
```

`py -3.12` "listede hangisi önce gelirse gelsin, 3.12'yi çalıştır" demek.

## pip: paket yöneticisi

`pip`, Python'la birlikte gelen paket yöneticisi. Bir paketi PyPI'dan indirip
kuruyor:

```text
python -m pip install pandas
```

Bu komut üç iş yapıyor:

1. pandas'ı PyPI'dan indiriyor.
2. pandas'ın ihtiyaç duyduğu **diğer paketleri** de buluyor ve kuruyor
   (NumPy, python-dateutil gibi). Bunlara **bağımlılık** deniyor.
3. Hepsini, komutu çalıştıran Python'un `site-packages` klasörüne koyuyor.

Üçüncü madde bu bölümün en önemli cümlesi: **paket, onu kuran Python'a
kuruluyor.** Başka bir Python o paketi görmüyor.

### Neden `pip` değil de `python -m pip`?

İnternette çoğu örnek kısaca `pip install pandas` yazıyor. Tek bir Python
varsa ikisi aynı. Ama birden fazla Python varsa `pip` komutu, `PATH`'te önce
bulunan **başka bir Python'un** pip'i olabilir. Paket bir yere kurulur, kodun
başka bir yerden çalışır ve `ModuleNotFoundError` alırsın.

`python -m pip`, "şu an `python` dediğim yorumlayıcının pip'ini çalıştır"
demek. Paketin nereye gideceği artık belirsiz değil. **Alışkanlık olarak hep
bunu yaz.**

### En sık kullanılan pip komutları

| Komut | Ne yapar |
|---|---|
| `python -m pip install pandas` | Kurar (bağımlılıklarıyla) |
| `python -m pip install pandas==2.2.2` | Tam olarak bu sürümü kurar |
| `python -m pip install --upgrade pandas` | En yeni sürüme yükseltir |
| `python -m pip uninstall pandas` | Kaldırır |
| `python -m pip list` | Kurulu paketleri listeler |
| `python -m pip show pandas` | Sürümü, nereye kurulduğunu, neye bağlı olduğunu gösterir |
| `python -m pip freeze` | Kurulu paketleri `ad==sürüm` biçiminde yazar |
| `python -m pip install -r requirements.txt` | Dosyadaki her şeyi kurar |

### Sürüm yazmak

| Yazım | Anlamı |
|---|---|
| `pandas==2.2.2` | Tam olarak 2.2.2 |
| `pandas>=2.0` | 2.0 ya da daha yenisi |
| `pandas>=2.0,<3.0` | 2 serisinden herhangi biri |
| `pandas~=2.2.0` | 2.2.x, ama 2.3 değil ("uyumlu sürüm") |

**Tuzak:** terminalde `>` işareti "çıktıyı dosyaya yaz" demek.
`python -m pip install pandas>=2.0` yazarsan pip `pandas`'ı kurar, çıktısı
da `=2.0` adında bir dosyaya gider. Karşılaştırma işareti içeren sürümü
**tırnak içinde** yaz:

```text
python -m pip install "pandas>=2.0"
```

## Ortam nedir?

Bilgisayarına Python kurduğun anda bir ortamın oluyor: o Python ve onun
`site-packages` klasörü. Buna **genel** (global) ortam deniyor. Başka bir şey
yapmazsan her `pip install` oraya gidiyor.

Tek proje için sorun yok. Sorun ikinci projede başlıyor.

<figure class="fig">
  <div class="flow">
    <span class="node no"><b>Proje A</b><br>pandas 1.5 ister</span>
    <span class="arrow">→</span>
    <span class="node"><b>Genel ortam</b><br>tek pandas sürümü</span>
    <span class="arrow">←</span>
    <span class="node no"><b>Proje B</b><br>pandas 2.2 ister</span>
  </div>
  <figcaption>Bir ortamda bir paketin yalnızca bir sürümü olabiliyor. B için pandas'ı yükseltince A bozuluyor.</figcaption>
</figure>

Genel ortamı kullanmanın üç zararı var:

- **Çakışma.** Bir ortamda bir paketin yalnızca bir sürümü durabiliyor.
- **"Bende çalışıyordu."** Projenin gerçekte hangi paketlere ihtiyaç
  duyduğunu bilmiyorsun; genel ortamda yıllardır biriken yüz paketin
  hangisini kullandığın belli değil.
- **Temizlik.** Bir projeyi bırakınca kurduğun paketleri ayıklayamıyorsun.

Çözüm, **her projeye ayrı bir ortam** vermek.

## Sanal ortam: `venv`

Sanal ortam, proje klasörünün içinde duran küçük bir klasör. İçinde o
projeye ait bir Python komutu ve **boş** bir `site-packages` var. O ortamda
kurduğun her şey oraya gidiyor; genel ortam ve diğer projeler etkilenmiyor.

`venv` Python'un kendi içinde geliyor, ayrıca kurulmuyor.

### Oluşturmak

Proje klasöründe:

```text
python -m venv .venv
```

Son kelime ortamın klasör adı. `.venv` bir gelenek: VS Code onu kendiliğinden
buluyor, baştaki nokta da klasörü gizli sayıyor. Oluşan yapı (Windows):

```text
proje-a/
├── .venv/
│   ├── pyvenv.cfg          hangi Python'dan kurulduğu
│   ├── Scripts/            python.exe, pip.exe, activate
│   └── Lib/
│       └── site-packages/  bu projenin paketleri
└── main.py
```

macOS ve Linux'ta `Scripts` yerine `bin`, paketler
`lib/python3.x/site-packages` altında.

`venv` Python'u baştan kopyalamıyor; `pyvenv.cfg` dosyasına onu kuran
Python'un yerini yazıyor. Bu yüzden **ortamın Python sürümü, onu kuran
Python'un sürümü.** Başka bir sürüm istiyorsan ortamı o sürümle kur:

```text
py -3.11 -m venv .venv
```

### Etkinleştirmek

| Terminal | Komut |
|---|---|
| Windows `cmd` | `.venv\Scripts\activate` |
| Windows PowerShell | `.venv\Scripts\Activate.ps1` |
| macOS / Linux | `source .venv/bin/activate` |

Başarılı olunca komut satırının başında ortamın adı beliriyor:

```text
(.venv) C:\projeler\proje-a>
```

Bundan sonra yazdığın `python` ve `python -m pip` bu ortamınki. Çıkmak için:

```text
deactivate
```

### Etkinleştirmek aslında ne yapıyor?

Sihir yok. `activate`, ortamın `Scripts` klasörünü `PATH`'in **en başına**
ekliyor. Windows `python` komutunu aradığında önce orayı buluyor. Kontrol
etmek için:

```text
where python
```

İlk satır `...\proje-a\.venv\Scripts\python.exe` olmalı.

Bunu bilmek işe yarıyor, çünkü etkinleştirmek **zorunlu değil**. Ortamın
Python'unu yoluyla da çağırabilirsin:

```text
.venv\Scripts\python main.py
.venv\Scripts\python -m pip install pandas
```

### Yeni terminal, yeni etkinleştirme

Etkinleştirme yalnızca **o terminal penceresi** için geçerli. Terminali
kapatıp açınca ortam yine kapalı. Yeni pencerede ilk iş: `activate`.

### Silmek ve taşımak

Ortamı silmek için klasörü silmen yeterli. Kaldırıcı yok, kayıt yok.

Ortam klasörünü **taşıma ve adını değiştirme**. İçindeki betiklere tam yol
yazılı; başka bir yere taşınan ortam bozuluyor. Proje klasörünü taşıdıysan
`.venv`'i silip yeniden kur. Bu yüzden projenin paket listesini bir dosyada
tutuyoruz.

## İki ortam yan yana

Aynı bilgisayarda iki proje, iki farklı pandas:

```text
cd C:\projeler\proje-a
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas==1.5.3
python -c "import pandas; print(pandas.__version__)"
1.5.3
deactivate

cd C:\projeler\proje-b
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas==2.2.2
python -c "import pandas; print(pandas.__version__)"
2.2.2
```

İki proje de kendi sürümünü görüyor ve birbirinden habersiz. Genel ortamda
hiç pandas yok.

**Ortamla bağlantıyı kuran şey, o anda hangi Python'un çalıştığı.** Terminalde
bunu `activate` belirliyor. Editöre de ayrıca söylemen gerekiyor: VS Code'da
"Python: Select Interpreter", Jupyter'de çekirdek seçimi. Nasıl yapıldığı
"Editörü Ortama Bağlamak" notunda.

Kodun içinden hangi Python'da olduğunu sormak için:

```python
import sys
print(sys.executable)
```

`ModuleNotFoundError` aldığında ilk bakacağın şey bu.

## `requirements.txt`

Ortamın kendisini kimseyle paylaşmıyorsun: büyük, senin bilgisayarına özel ve
başka yerde çalışmıyor. Paylaştığın şey **tarifi**: hangi paketlerin, hangi
sürümlerle kurulacağı. Bu tarifin geleneksel adı `requirements.txt`.

```text
# Proje A'nın paketleri
pandas==2.2.2
numpy==1.26.4
matplotlib>=3.8
```

Her satırda bir paket. `#` ile başlayan satır açıklama.

Ortamdaki paketleri dosyaya yazmak:

```text
python -m pip freeze > requirements.txt
```

Buradaki `>` işte o "çıktıyı dosyaya yaz" işareti. `freeze` her paketi tam
sürümüyle yazıyor, **bağımlılıkları da dahil**: pandas kurduysan dosyada
NumPy, python-dateutil, pytz de görünür. Bu, projeyi başka yerde birebir aynı
kurmayı sağlıyor. İstersen dosyayı elle de yazabilirsin; o zaman yalnızca
doğrudan kullandığın paketleri yazarsın.

Dosyadaki her şeyi kurmak:

```text
python -m pip install -r requirements.txt
```

**Genel ortamda `freeze` çalıştırma.** Orada yıllardır biriken her şey
dosyaya girer. `freeze` ancak projenin kendi ortamında anlamlı.

### Git ile paylaşırken

`.venv` klasörü depoya konmaz, `requirements.txt` konur. Projenin
`.gitignore` dosyasına şu satır yazılır:

```text
.venv/
```

Başkasının projesini aldığında adımlar hep aynı:

```text
git clone https://github.com/kisi/proje.git
cd proje
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Anaconda ve conda

Veri bilimi kaynaklarında sık sık **Anaconda** önerilir. Anaconda bir
**dağıtım**: tek kurulumda Python, `conda` adlı yönetici, veri bilimi için
yüzlerce hazır paket, Jupyter ve Anaconda Navigator adında bir arayüz
geliyor.

Aynı ailenin iki küçük kardeşi var:

- **Miniconda:** yalnızca Python ve conda. Paketleri sen kuruyorsun.
- **Miniforge:** Miniconda gibi küçük; paketleri topluluğun `conda-forge`
  kanalından alıyor.

### conda neyi farklı yapıyor?

`conda` hem paket yöneticisi hem ortam yöneticisi. pip ile üç önemli farkı
var:

1. **Yalnızca Python paketi kurmuyor.** C ve C++ kütüphaneleri, ekran kartı
   araçları (CUDA), hatta R gibi başka diller de conda paketi olabiliyor.
   Bir Python paketinin arkasında böyle bir sistem kütüphanesi varsa conda
   onu da getiriyor.
2. **Python'un kendisini kuruyor.** `venv` hangi Python'la kurulduysa onu
   kullanıyor; conda ise istediğin sürümü indirip ortama koyuyor.
3. **Ortamlar proje klasöründe değil, merkezde duruyor.** Adıyla çağırıyorsun;
   dosyaları `anaconda3\envs\<ad>` altında.

### conda ile ortam

```text
conda create -n proje-a python=3.11
conda activate proje-a
conda install pandas
conda deactivate
```

`-n` ortamın adı. Etkin ortam yine komut satırının başında görünüyor:
`(proje-a)`.

Kurulumla birlikte bir **`base`** ortamı geliyor ve terminal açılınca o
etkin oluyor. **`base`'e proje paketi kurma.** Orası conda'nın kendi
çalışma alanı; bozulursa conda da bozuluyor. Her proje için
`conda create` ile yeni ortam aç.

Windows'ta conda en kolay **Anaconda Prompt** penceresinde çalışıyor. Normal
PowerShell'de `conda activate` hata veriyorsa bir kez şunu çalıştırıp
terminali yeniden aç:

```text
conda init powershell
```

### Ortam dosyası: `environment.yml`

conda'nın `requirements.txt` karşılığı. Python sürümünü de yazıyor:

```text
name: proje-a
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pandas=2.2
  - pip
  - pip:
      - bir-pypi-paketi==1.0
```

```text
conda env export > environment.yml
conda env create -f environment.yml
```

Burada sürüm tek `=` ile yazılıyor (`pandas=2.2`); pip'te `==` idi. En sık
karıştırılan ayrıntılardan biri.

### Kanallar ve lisans

conda paketleri **kanallardan** geliyor. Anaconda'nın kendi kanalı
`defaults`; topluluğun kanalı `conda-forge`. Belirli bir kanaldan kurmak:
`conda install -c conda-forge paket`.

Anaconda'nın kendi kanalı ve dağıtımı büyük kurumlarda ticari lisansa bağlı.
Bir şirkette kullanacaksan önce şirketin kuralına bak. Miniforge ve
`conda-forge` bu şarta bağlı değil.

## pip mi, conda mı?

<figure class="fig">
  <div class="versus">
    <div>
      <h5>PIP + VENV</h5>
<pre><code class="language-text">python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas</code></pre>
    </div>
    <div>
      <h5>CONDA</h5>
<pre><code class="language-text">conda create -n demo python=3.11
conda activate demo
conda install pandas</code></pre>
    </div>
  </div>
  <figcaption>Aynı iş iki araçla: ortam kur, etkinleştir, paket kur. İkisi de aynı sorunu çözüyor; fark neyi kurabildikleri ve ortamı nerede tuttukları.</figcaption>
</figure>

| | pip + venv | conda |
|---|---|---|
| Geldiği yer | Python'un içinde | Anaconda / Miniconda / Miniforge |
| Paket kaynağı | PyPI | `defaults`, `conda-forge` kanalları |
| Ne kurabilir | Python paketleri | Python paketleri **ve** Python dışı kütüphaneler |
| Python sürümü | Ortamı kuran Python'unki | `python=3.11` diye seçilir, conda indirir |
| Ortam nerede | Proje klasöründe (`.venv`) | Merkezde (`envs\<ad>`) |
| Etkinleştirme | `.venv\Scripts\activate` | `conda activate <ad>` |
| Tarif dosyası | `requirements.txt` | `environment.yml` |

### İkisini birlikte kullanmak

conda ortamının içinde pip de kullanılabiliyor; conda'da olmayan bir paket
için gerekebilir. Kural şu:

1. Önce bulabildiğin her şeyi **conda** ile kur.
2. conda'da olmayanları en sonda **pip** ile kur.
3. pip'ten sonra aynı ortama yeniden `conda install` yapma. conda, pip'in
   kurduklarını tam bilmiyor ve üzerlerine yazabiliyor.

Karmaşa çıkarsa ortamı onarmaya uğraşma; silip dosyadan yeniden kur.
Ortamların ucuz olmasının anlamı bu.

Bir de şu: komut satırında `(.venv) (base)` gibi **iki ortam birden**
görünüyorsa biri fazla. Önce birini `deactivate` / `conda deactivate` ile
kapat.

## Hangisiyle başlamalı?

**python.org'dan temiz bir Python, her proje için `venv` ve `pip`.** Standart
bu; iş ilanlarındaki projelerin, açık kaynak depoların ve belgelerin büyük
kısmı böyle kuruluyor. Burada öğrendiğin her şey conda'ya geçince de işine
yarıyor.

conda'yı şu durumlarda seç:

- Bilgisayarında olmayan bir Python sürümüne hızlıca ihtiyacın varsa.
- Ekran kartıyla çalışan kütüphaneler ya da Python dışı sistem kütüphaneleri
  gerekiyorsa.
- Ekibin ya da kursun conda kullanıyorsa.

## Bir projeye başlarken

Her yeni projede aynı beş adım:

```text
mkdir proje-a
cd proje-a
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas
```

Paketler değiştikçe:

```text
python -m pip freeze > requirements.txt
```

## Özet

- **Yorumlayıcı** kodu çalıştıran program; **ortam** o yorumlayıcı ve ona
  kurulu paketler.
- Paket, onu kuran Python'a kuruluyor. Bu yüzden `pip` değil,
  **`python -m pip`** yaz.
- Terminalde karşılaştırma işaretli sürüm tırnak içinde:
  `"pandas>=2.0"`.
- **Her projeye ayrı ortam.** `python -m venv .venv` kurar,
  `.venv\Scripts\activate` etkinleştirir, `deactivate` kapatır.
- Etkinleştirme `PATH`'in başına ortamı ekliyor ve yalnızca o terminal
  penceresi için geçerli.
- Ortam paylaşılmaz, tarifi paylaşılır: `requirements.txt`
  (`pip freeze >` yazar, `pip install -r` kurar). `.venv/` `.gitignore`'a.
- **Anaconda** bir dağıtım, **conda** paket ve ortam yöneticisi. Python dışı
  kütüphaneleri ve Python'un kendisini de kurabiliyor; ortamları merkezde
  tutuyor. `base`'e paket kurma.
- conda ortamında önce conda, en sonda pip.
- `ModuleNotFoundError` aldığında ilk soru: **hangi Python çalışıyor?**
