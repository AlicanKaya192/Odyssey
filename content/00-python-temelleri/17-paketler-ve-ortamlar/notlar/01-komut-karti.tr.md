Bu sayfa ezberlemen gereken komutların tamamı. Dersi okuduktan sonra buraya
dönüp her satırın ne yaptığını söyleyebiliyor musun, diye kendini dene.

Örneklerde Windows yazımı var. macOS ve Linux farkları tabloda ayrıca
yazılı.

## En önemli on komut

Bunları uykunda yazabilmelisin:

```text
python --version
where python
python -m venv .venv
.venv\Scripts\activate
deactivate
python -m pip install pandas
python -m pip list
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
python -c "import sys; print(sys.executable)"
```

## Python ve terminal

| Komut | Ne yapar |
|---|---|
| `python --version` | Çalışan Python'un sürümü |
| `where python` | `python` yazınca hangi dosyaların bulunduğu; ilk satır çalışan (macOS/Linux: `which python`) |
| `py --list` | Windows'ta kurulu bütün Python sürümleri |
| `py -3.12` | Belirli bir sürümü çalıştırır |
| `python main.py` | Bir dosyayı çalıştırır |
| `python -m ad` | Bir modülü program gibi çalıştırır (`-m pip`, `-m venv`) |
| `python -c "kod"` | Tek satırlık kodu çalıştırır |
| `cd klasor` | Klasöre girer; `cd ..` bir üste çıkar |
| `dir` | Klasördekileri listeler (macOS/Linux ve PowerShell: `ls`) |
| `mkdir proje` | Yeni klasör açar |

## pip

| Komut | Ne yapar |
|---|---|
| `python -m pip --version` | pip sürümü **ve hangi Python'a ait olduğu** |
| `python -m pip install ad` | Kurar |
| `python -m pip install ad1 ad2 ad3` | Birden fazlasını birden kurar |
| `python -m pip install ad==1.2.3` | Tam sürüm |
| `python -m pip install "ad>=1.2"` | En az bu sürüm (tırnak şart) |
| `python -m pip install --upgrade ad` | Yükseltir (kısası `-U`) |
| `python -m pip install --upgrade pip` | pip'in kendisini yükseltir |
| `python -m pip uninstall ad` | Kaldırır (`-y` ile onay sormaz) |
| `python -m pip list` | Kurulu paketler |
| `python -m pip list --outdated` | Yeni sürümü çıkmış olanlar |
| `python -m pip show ad` | Sürüm, konum, bağımlılıklar |
| `python -m pip freeze` | `ad==sürüm` listesi |
| `python -m pip check` | Kurulu paketlerin birbirine uyup uymadığını denetler |

## Sanal ortam (`venv`)

| Komut | Ne yapar |
|---|---|
| `python -m venv .venv` | Ortamı kurar |
| `py -3.11 -m venv .venv` | Belirli bir Python sürümüyle kurar |
| `.venv\Scripts\activate` | Etkinleştirir (`cmd`) |
| `.venv\Scripts\Activate.ps1` | Etkinleştirir (PowerShell) |
| `source .venv/bin/activate` | Etkinleştirir (macOS/Linux) |
| `deactivate` | Ortamdan çıkar |
| `.venv\Scripts\python main.py` | Etkinleştirmeden, ortamın Python'uyla çalıştırır |
| `rmdir /s .venv` | Ortamı siler (`cmd`; PowerShell: `Remove-Item -Recurse .venv`, macOS/Linux: `rm -rf .venv`) |

## `requirements.txt`

| Komut | Ne yapar |
|---|---|
| `python -m pip freeze > requirements.txt` | Ortamdaki paketleri dosyaya yazar |
| `python -m pip install -r requirements.txt` | Dosyadakilerin hepsini kurar |
| `python -m pip install -r requirements.txt --upgrade` | Dosyadakileri izin verilen en yeni sürüme çeker |

Dosyanın içi:

```text
pandas==2.2.2       # tam sürüm
numpy>=1.26         # en az
matplotlib~=3.8.0   # 3.8.x
requests            # sürüm yok: en yenisi
```

## conda

| Komut | Ne yapar |
|---|---|
| `conda --version` | conda sürümü |
| `conda create -n ad python=3.11` | Ortam kurar |
| `conda create -n ad python=3.11 pandas numpy` | Ortamı paketleriyle birlikte kurar |
| `conda activate ad` | Etkinleştirir |
| `conda deactivate` | Çıkar |
| `conda env list` | Bütün ortamlar; etkin olanın yanında `*` |
| `conda list` | Etkin ortamdaki paketler |
| `conda install ad` | Kurar |
| `conda install -c conda-forge ad` | `conda-forge` kanalından kurar |
| `conda install ad=1.2` | Belirli sürüm (tek `=`) |
| `conda update ad` | Yükseltir |
| `conda remove ad` | Kaldırır |
| `conda env remove -n ad` | Ortamı bütünüyle siler |
| `conda env export > environment.yml` | Ortamı dosyaya yazar |
| `conda env export --from-history > environment.yml` | Yalnızca senin kurduklarını yazar; başka işletim sisteminde de kurulur |
| `conda env create -f environment.yml` | Dosyadan ortam kurar |
| `conda env update -f environment.yml --prune` | Ortamı dosyaya göre günceller, fazlaları siler |
| `conda init powershell` | PowerShell'de `conda activate`'i çalışır hâle getirir (bir kez) |
| `conda config --set auto_activate_base false` | Terminal açılınca `base` etkinleşmesin |
| `conda clean --all` | İndirilmiş paket önbelleğini temizler |

## Jupyter ve ortamlar

| Komut | Ne yapar |
|---|---|
| `python -m pip install ipykernel` | Ortamı Jupyter'e bağlamak için gereken paket |
| `python -m ipykernel install --user --name proje-a` | Etkin ortamı "proje-a" adlı çekirdek olarak kaydeder |
| `jupyter kernelspec list` | Kayıtlı çekirdekler |
| `jupyter kernelspec uninstall proje-a` | Çekirdek kaydını siler |
| `%pip install ad` | Not defteri hücresinde: **o çekirdeğin** ortamına kurar |

## Karıştırılanlar

| Bu | Şu değil |
|---|---|
| `python -m pip install` | `pip install` (başka Python'a gidebilir) |
| `"pandas>=2.0"` | `pandas>=2.0` (terminal `>`'yi dosyaya yönlendirme sanar) |
| pip'te `pandas==2.2` | conda'da `pandas=2.2` |
| `requirements.txt` paylaşılır | `.venv` paylaşılmaz |
| `%pip install` (Jupyter) | `!pip install` (başka Python'a gidebilir) |
| `pip install scikit-learn`, kodda `import sklearn` | `pip install sklearn` (kurulum adı ile içe aktarma adı farklı olabilir) |
