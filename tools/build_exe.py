"""Uygulamayı tek klasörlük bir `.exe` olarak paketler.

Çıktı: `dist/Odyssey/Odyssey.exe`

Neden tek dosya değil de klasör: uygulama Chromium (QtWebEngine) taşıyor.
Tek dosyaya sıkıştırılırsa her açılışta yüzlerce megabayt geçici klasöre
açılıyor ve başlangıç saniyeler sürüyor. Klasör hâlinde dağıtım hem hızlı
açılıyor hem de güncelleme sırasında yalnızca değişen dosyalar
değiştirilebiliyor.

PyInstaller **çapraz derleme yapmıyor**: Windows'ta çalıştırıldığında
yalnızca Windows paketi çıkıyor. macOS için `.app` üretmek isteyen bir
Mac'te aynı komutu çalıştırmalı; script gerekli farkları (simge biçimi,
çalıştırılabilir dosya adı, veri ayıracı) kendisi hallediyor.

Kullanım:
    .venv\\Scripts\\python tools/build_exe.py
    .venv\\Scripts\\python tools/build_exe.py --temiz   # önce eskiyi sil
    .venv\\Scripts\\python tools/build_exe.py --deneme  # yayın dışı deneme
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.version import APP_VERSION  # noqa: E402

APP_NAME = "Odyssey"
ENTRY = PROJECT_ROOT / "app" / "main.py"

# Simge biçimi platforma göre değişiyor: Windows `.ico`, macOS `.icns`,
# Linux `.png`. Yanlış biçim verilirse PyInstaller simgeyi sessizce
# atlıyor ve uygulama genel bir simgeyle çıkıyor.
ICON_BY_PLATFORM = {
    "win32": "icon.ico",
    "darwin": "icon.icns",
}
ICON = (
    PROJECT_ROOT / "app" / "resources"
    / ICON_BY_PLATFORM.get(sys.platform, "icon.png")
)

# Uygulamayla birlikte gidecek klasörler: (kaynak, paket içindeki yer)
DATA = [
    ("content", "content"),
    ("sandbox", "sandbox"),
    ("app/i18n", "app/i18n"),
    ("app/resources", "app/resources"),
    ("LICENSE", "."),
    ("CHANGELOG.md", "."),
    ("CHANGELOG.en.md", "."),
]

# QtWebEngine'in yardımcı süreci ve kaynakları elle toplanmalı; PyInstaller
# bunları kendiliğinden bulamıyor.
#
# NumPy, pandas, matplotlib ve scikit-learn de elle toplanıyor. **Uygulama onları hiç
# import etmiyor** — kullanan taraf, alıştırma kodunu çalıştıran
# denetleyici. PyInstaller import zincirini takip ettiği için onları
# kendiliğinden bulmuyor; `--collect-all` ile açıkça isteniyor.
#
# Neden pakete gömülüyor: Veri Bilimi ve Makine Öğrenmesi bölümlerinin
# alıştırmaları bu kütüphaneleri istiyor. Alternatif, kullanıcıya ilk açılışta bir sanal ortam
# kurdurmaktı; o da internet bağlantısı ve yüz megabaytlık bir indirme
# demek. Uygulamanın sözü "indir ve çalıştır" olduğu için gömme seçildi.
COLLECT = [
    "PySide6.QtWebEngineCore",
    "PySide6.QtWebEngineWidgets",
    # Belge sayfalarının uygulamaya haber verdiği kanal; `qwebchannel.js`
    # bu modülün kaynaklarında duruyor (`document_view.py`).
    "PySide6.QtWebChannel",
    "numpy",
    "pandas",
    "matplotlib",
    "sklearn",
    # Zaman Serileri: durağanlık testi, ayrıştırma, ARIMA, üstel düzleştirme.
    # Yalnızca kullanıcı kodu import ediyor, o yüzden elle toplanıyor.
    "statsmodels",
    "patsy",
    "formulaic",   # statsmodels 0.15 formül arayüzü bununla çalışıyor
    # Temel Kütüphaneler: seaborn bölümü. Saf Python; yalnızca kullanıcı
    # kodu import ediyor.
    "seaborn",
    # SQL alıştırmalarının sunucuya bağlanan katmanı. `sandbox/sql_runner.py`
    # pakete düz veri olarak giriyor ve PyInstaller içindeki `import
    # pyodbc`'yi görmüyor; toplanmazsa paketlenmiş sürüm SQL Server kurulu
    # olsa bile "sürücü yok" diyordu.
    "pyodbc",
    # API alıştırmaları: kullanıcı kodu `requests` ile alıştırma sunucusuna
    # istek atıyor; uygulama import etmediği için elle toplanıyor.
    "requests",
    "urllib3",
    "idna",
    "certifi",
    "charset_normalizer",
    # Docker alıştırmaları: compose.yaml denetleyicide okunuyor
    # (`sandbox/docker_runner.py`); Docker kurulu olmasa da.
    "yaml",
    # API 2 alıştırmaları: kişinin FastAPI uygulaması, denetleyicide
    # TestClient ile (`sandbox/fastapi_sandbox.py`); test bölümünde pytest.
    # Hepsini yalnızca kişinin kodu ve denetleyici import ediyor.
    "fastapi",
    "starlette",
    "pydantic",
    "pydantic_core",
    "annotated_types",
    "annotated_doc",
    "typing_inspection",
    "anyio",
    "httpx2",
    "httpcore2",
    "httpx",
    "httpcore",
    "h11",
    "uvicorn",
    "click",
    "pytest",
    "_pytest",
    "pluggy",
    "iniconfig",
    "pygments",
    "opentelemetry",
    # Büyük Veri alıştırmaları: Parquet (pyarrow), dosyada SQL (duckdb),
    # paralel tablolar (dask ve bağımlılıkları). Yalnızca kişinin kodu
    # import ediyor; pandas'ın `str` sütunları da pyarrow ile çalışıyor.
    "pyarrow",
    "duckdb",
    "dask",
    "fsspec",
    "toolz",
    "partd",
    "locket",
    "cloudpickle",
    "packaging",
]

# Yalnızca denetleyicinin kullandığı standart kütüphane modülleri.
# Denetleyici pakete düz dosya olarak giriyor; PyInstaller içindeki
# import'ları görmüyor. Alıştırma sunucusu (`sandbox/api_sandbox.py`)
# bunlarla kuruluyor; Docker denetleyicisi (`sandbox/docker_runner.py`)
# komutları `shlex` ile ayrıştırıyor, konteynere `urllib.request` ile
# istek atıyor.
HIDDEN = ["http.server", "socketserver", "shlex", "urllib.request"]

# Gereksiz yere paketi büyüten, kullanılmayan Qt modülleri.
#
# `unittest` burada değil: matplotlib pyparsing'i, pyparsing da kendi
# `testing` modülünü paket açılışında import ediyor ve o da `unittest`
# istiyor. Dışarıda bırakılınca paketlenmiş sürümde `import matplotlib`
# `ModuleNotFoundError: No module named 'unittest'` veriyor — ölçüldü.
EXCLUDE = [
    "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.Qt3DAnimation",
    "PySide6.QtCharts", "PySide6.QtDataVisualization", "PySide6.QtQuick3D",
    "PySide6.QtMultimedia", "PySide6.QtBluetooth", "PySide6.QtNfc",
    "PySide6.QtSensors", "PySide6.QtSerialPort", "PySide6.QtTest",
    "tkinter", "pydoc_data",
]


def ensure_pyinstaller() -> None:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller kurulu değil, kuruluyor...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller>=6.0"],
            check=True,
        )


AUTHOR = "Alican Kaya"


def version_file() -> Path:
    """`Odyssey.exe`'nin Windows sürüm bilgisi (Özellikler › Ayrıntılar).

    Kod imzası (SignPath) imzalanan dosyada ürün adı ve sürüm istiyor;
    önce bu bilgi hiç yoktu. Sürüm dört parçalı sayıya tamamlanıyor
    (`0.9.2` → `0.9.2.0`).
    """
    parcalar = [int(p) for p in APP_VERSION.split(".") if p.isdigit()][:4]
    parcalar += [0] * (4 - len(parcalar))
    sayi = tuple(parcalar)
    metin = f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={sayi}, prodvers={sayi}, mask=0x3f, flags=0x0,
                    OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', '{AUTHOR}'),
      StringStruct('FileDescription', '{APP_NAME}'),
      StringStruct('FileVersion', '{APP_VERSION}'),
      StringStruct('InternalName', '{APP_NAME}'),
      StringStruct('LegalCopyright', 'Copyright (c) 2026 {AUTHOR}. MIT License.'),
      StringStruct('OriginalFilename', '{APP_NAME}.exe'),
      StringStruct('ProductName', '{APP_NAME}'),
      StringStruct('ProductVersion', '{APP_VERSION}')])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    yol = PROJECT_ROOT / "build" / "version_info.txt"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(metin, encoding="utf-8")
    return yol


def build_command() -> list[str]:
    command = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--windowed",              # arkada konsol penceresi açılmasın
        "--name", APP_NAME,
        "--icon", str(ICON),
        "--distpath", str(PROJECT_ROOT / "dist"),
        "--workpath", str(PROJECT_ROOT / "build"),
        "--specpath", str(PROJECT_ROOT / "build"),
    ]
    if sys.platform == "win32":
        command += ["--version-file", str(version_file())]

    for source, target in DATA:
        command += ["--add-data", f"{PROJECT_ROOT / source}{';' if sys.platform == 'win32' else ':'}{target}"]

    for module in COLLECT:
        command += ["--collect-all", module]

    for module in HIDDEN:
        command += ["--hidden-import", module]

    for module in EXCLUDE:
        command += ["--exclude-module", module]

    command.append(str(ENTRY))
    return command


UNRELEASED_MARKS = ("yayınlanmadı", "unreleased")


def changelog_dated() -> str:
    """Bu sürümün değişiklik günlüğü tarihlendi mi?

    Boş metin döndürürse sorun yok; değilse eksik dosyanın adı.

    **Neden derlemeden önce bakılıyor:** günlük dosyaları pakete olduğu
    gibi giriyor ve uygulamanın Sürüm Notları ekranı onları gösteriyor.
    0.7.1 tarihlenmeden derlendi ve yayınlanan pakette sürüm
    "yayınlanmadı" yazıyordu — kullanıcı indirdiği sürümün yayınlanmadığını
    okuyordu.
    """
    eksik = []
    for ad in ("CHANGELOG.md", "CHANGELOG.en.md"):
        yol = PROJECT_ROOT / ad
        if not yol.exists():
            continue
        for satir in yol.read_text(encoding="utf-8").splitlines():
            if not satir.startswith(f"## [{APP_VERSION}]"):
                continue
            if any(mark in satir.lower() for mark in UNRELEASED_MARKS):
                eksik.append(ad)
            break
    return ", ".join(eksik)


def folder_size(path: Path) -> str:
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return f"{total / 1024 / 1024:.0f} MB"


def main() -> int:
    if not ICON.exists():
        print(f"Simge bulunamadı: {ICON.name}")
        if sys.platform == "win32":
            print("Önce: python tools/build_icon.py")
        else:
            print(
                f"{sys.platform} için {ICON.name} gerekiyor; "
                "build_icon.py şimdilik yalnızca .ico üretiyor."
            )
        return 1

    eksik = changelog_dated()
    # `--deneme`: yayın olmayan derleme (fark kurulumunu sınamak gibi);
    # tarih denetimi atlanıyor. Bu paket yayınlanmaz.
    if eksik and "--deneme" not in sys.argv:
        print(f"{eksik}: {APP_VERSION} başlığı hâlâ 'yayınlanmadı' diyor.")
        print("Önce tarihi yazın; paket günlüğü olduğu gibi taşıyor ve")
        print("uygulamanın Sürüm Notları ekranı bunu gösteriyor.")
        return 1

    if "--temiz" in sys.argv:
        for folder in ("dist", "build"):
            shutil.rmtree(PROJECT_ROOT / folder, ignore_errors=True)
        print("Eski çıktılar silindi.")

    ensure_pyinstaller()

    print(f"{APP_NAME} {APP_VERSION} paketleniyor — bu birkaç dakika sürer...")
    result = subprocess.run(build_command())
    if result.returncode != 0:
        print("Paketleme başarısız.")
        return result.returncode

    output = PROJECT_ROOT / "dist" / APP_NAME
    exe = output / (
        f"{APP_NAME}.exe" if sys.platform == "win32" else APP_NAME
    )

    print()
    if exe.exists():
        print(f"Hazır: {exe}")
        print(f"Klasör boyutu: {folder_size(output)}")
        print()
        print("Dağıtım kurulum programıyla: python tools/build_installer.py")
    else:
        print("Beklenen çıktı oluşmadı:", exe)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
