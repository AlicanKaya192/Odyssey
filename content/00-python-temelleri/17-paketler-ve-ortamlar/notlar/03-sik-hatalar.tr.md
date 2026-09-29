Kurulum hatalarının neredeyse hepsi iki sorudan birine çıkıyor: **hangi
Python çalışıyor** ve **paket hangi Python'a kuruldu**. Aşağıdaki her hatada
önce bunlara bak.

## `ModuleNotFoundError: No module named 'pandas'`

Kod çalışıyor ama paketi bulamıyor. Ya hiç kurulmadı ya da **başka bir
Python'a** kuruldu. Sırayla:

1. Kod hangi Python'da çalışıyor?
   `import sys; print(sys.executable)`
2. Terminal hangi Python'u çalıştırıyor? `where python`
3. Paket o Python'da var mı? `python -m pip show pandas`

Yollar tutmuyorsa: doğru ortamı etkinleştir (ya da editörde doğru
yorumlayıcıyı seç) ve kurulumu `python -m pip install pandas` ile **orada**
yap.

Not defterindeysen çekirdek başka bir ortam olabilir; hücrede
`%pip install pandas`, sonra çekirdeği yeniden başlat.

## Kurulum adı ile içe aktarma adı farklı

`pip install sklearn` hata veriyor ya da `import scikit_learn` bulunamıyor.
Bazı paketlerin PyPI'daki adı ile koddaki adı aynı değil:

| Kurarken | Kodda |
|---|---|
| `scikit-learn` | `import sklearn` |
| `opencv-python` | `import cv2` |
| `Pillow` | `import PIL` |
| `beautifulsoup4` | `import bs4` |
| `python-dateutil` | `import dateutil` |
| `PyYAML` | `import yaml` |

Emin değilsen paketin PyPI sayfasına ya da belgesinin ilk sayfasına bak.

## `'pip' is not recognized...` / `pip: command not found`

`pip` komutu `PATH`'te yok. Çözüm zaten alışkanlığın olmalı:

```text
python -m pip install pandas
```

`python` da tanınmıyorsa Python kurulurken **Add python.exe to PATH**
işaretlenmemiş. Kurulum dosyasını yeniden çalıştırıp "Modify" ile ekleyebilir
ya da Windows'ta `py` başlatıcısını kullanabilirsin: `py -m pip install
pandas`.

## `python` yazınca Microsoft Store açılıyor

Windows'un kendi "uygulama yürütme diğer adları" `python` komutunu Store'a
yönlendiriyor. **Ayarlar → Uygulamalar → Gelişmiş uygulama ayarları →
Uygulama yürütme diğer adları** altında `python.exe` ve `python3.exe`
satırlarını kapat.

## PowerShell: "running scripts is disabled on this system"

`.venv\Scripts\Activate.ps1` çalışmıyor, çünkü PowerShell varsayılan olarak
betik çalıştırmıyor. Yalnızca kendi kullanıcın için izin vermek:

```text
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Bunu istemiyorsan `cmd` penceresinde `.venv\Scripts\activate` kullan ya da
etkinleştirmeden `.venv\Scripts\python` ile çalış.

## `conda: The term 'conda' is not recognized`

conda normal PowerShell'e tanıtılmamış. **Anaconda Prompt** penceresini kullan
ya da bir kez `conda init powershell` çalıştırıp terminali yeniden aç (bu
komutu Anaconda Prompt'ta yaz).

## `error: externally-managed-environment`

macOS'ta Homebrew'un ya da Linux'ta sistemin Python'una `pip install`
yaptığında çıkıyor. İşletim sistemi kendi Python'unu korumak istiyor. Çözüm
sanal ortam:

```text
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas
```

İnternette önerilen `--break-system-packages` bayrağını kullanma; adı ne
yaptığını anlatıyor.

## `Access is denied` / `Permission denied`

Paketi kurmaya yetkin olmayan bir yere, genellikle bütün kullanıcıların
Python'una kuruyorsun. Terminali yönetici olarak açmak işe yarar ama doğru
çözüm değil: sistemin Python'u kirleniyor. Sanal ortam kur; ortam kendi
klasöründe olduğu için izin sorunu kalmıyor.

## `No matching distribution found for ...`

pip istenen paketi bulamadı. Üç olası sebep:

- Adı yanlış yazdın (yukarıdaki tabloya da bak).
- İstediğin sürüm yok: `pandas==9.0` gibi.
- Paketin **senin Python sürümün için** hazır hâli yok. Çok yeni çıkmış bir
  Python sürümünde bu sık oluyor; birkaç ay önceki bir Python sürümüyle
  ortam kur (`py -3.12 -m venv .venv`).

## `ResolutionImpossible` / "conflicting dependencies"

İstediğin sürümler birbirine uymuyor: A paketi `numpy<2` istiyor, B paketi
`numpy>=2`. `requirements.txt`'de tam sabitlenmiş (`==`) sürümleri gevşet
(`>=`), pip uyan bir birleşim arasın. Olmuyorsa iki paketi ayrı ortamlara
ayırman gerekebilir.

## Klasörde `=2.0` adında garip bir dosya

`python -m pip install pandas>=2.0` yazdın; terminal `>`'yi "dosyaya yaz"
anladı. Dosyayı sil ve sürümü tırnakla yaz: `"pandas>=2.0"`.

## Proje klasörünü taşıdım, ortam çalışmıyor

`Fatal error in launcher: Unable to create process` ya da `activate` sonrası
yanlış Python. Ortamın içinde eski tam yollar yazılı. Ortamı sil ve yeniden
kur:

```text
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## `AttributeError: partially initialized module 'pandas'`

Dosyana `pandas.py` (ya da `random.py`, `math.py`, `numpy.py`) adını
verdin. `import pandas` yazınca Python önce **kendi klasöründeki** dosyayı
buluyor ve gerçek kütüphane yerine senin dosyanı içe aktarıyor. Dosyanın
adını değiştir, yanında oluşmuş `__pycache__` klasörünü de sil.

## Komut satırında iki ortam: `(.venv) (base)`

Hem conda'nın `base` ortamı hem senin `.venv`'in etkin. Hangi Python'un
çalışacağı belirsizleşiyor. İkisinden birini kapat; terminal her açıldığında
`base` gelmesin istiyorsan:

```text
conda config --set auto_activate_base false
```
