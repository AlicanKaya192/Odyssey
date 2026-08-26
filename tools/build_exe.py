"""Uygulamayı tek klasörlük bir `.exe` olarak paketler.

Çıktı: `dist/Odyssey/Odyssey.exe`

Neden tek dosya değil de klasör: uygulama Chromium (QtWebEngine) taşıyor.
Tek dosyaya sıkıştırılırsa her açılışta yüzlerce megabayt geçici klasöre
açılıyor ve başlangıç saniyeler sürüyor. Klasör hâlinde dağıtım hem hızlı
açılıyor hem de güncelleme sırasında yalnızca değişen dosyalar
değiştirilebiliyor.

Kullanım:
    .venv\\Scripts\\python tools/build_exe.py
    .venv\\Scripts\\python tools/build_exe.py --temiz   # önce eskiyi sil
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
ICON = PROJECT_ROOT / "app" / "resources" / "icon.ico"

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
COLLECT = ["PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets"]

# Gereksiz yere paketi büyüten, kullanılmayan Qt modülleri.
EXCLUDE = [
    "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.Qt3DAnimation",
    "PySide6.QtCharts", "PySide6.QtDataVisualization", "PySide6.QtQuick3D",
    "PySide6.QtMultimedia", "PySide6.QtBluetooth", "PySide6.QtNfc",
    "PySide6.QtSensors", "PySide6.QtSerialPort", "PySide6.QtTest",
    "tkinter", "unittest", "pydoc_data",
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

    for source, target in DATA:
        command += ["--add-data", f"{PROJECT_ROOT / source}{';' if sys.platform == 'win32' else ':'}{target}"]

    for module in COLLECT:
        command += ["--collect-all", module]

    for module in EXCLUDE:
        command += ["--exclude-module", module]

    command.append(str(ENTRY))
    return command


def folder_size(path: Path) -> str:
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return f"{total / 1024 / 1024:.0f} MB"


def main() -> int:
    if not ICON.exists():
        print("Simge bulunamadı. Önce: python tools/build_icon.py")
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
    exe = output / f"{APP_NAME}.exe"

    print()
    if exe.exists():
        print(f"Hazır: {exe}")
        print(f"Klasör boyutu: {folder_size(output)}")
        print()
        print("Dağıtmak için `dist/Odyssey` klasörünün tamamını zip'leyin;")
        print("yalnızca .exe dosyası tek başına çalışmaz.")
    else:
        print("Beklenen çıktı oluşmadı:", exe)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
