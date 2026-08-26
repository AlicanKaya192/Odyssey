"""Sanal ortamları kuran yardımcı script.

İki ayrı ortam var:

1. **Uygulama ortamı** (`.venv`) — arayüzün ve uygulamanın kendisinin çalıştığı
   yer. PySide6 burada.
2. **Alıştırma ortamı** (`%APPDATA%\\ProjeA\\exercise-env`) — kullanıcının
   yazdığı kodun çalıştığı yer. numpy, pandas gibi paketler burada.

Bu ikisi kasten ayrı: kullanıcı bir alıştırmada garip bir paket import etse
veya ortamı bozsa bile uygulamanın kendisi çalışmaya devam eder.

Kullanım:
    py -3.14 tools/setup_env.py              # ikisini de kur
    py -3.14 tools/setup_env.py --app        # sadece uygulama ortamı
    py -3.14 tools/setup_env.py --exercises  # sadece alıştırma ortamı

ÖNEMLİ: Sanal ortamı Anaconda'nın Python'u ile kurma. Anaconda kendi
(eski) MSVC runtime kütüphanelerini taşıyor ve Qt'nin DLL'leri onları
yükleyince "Belirtilen yordam bulunamadı" hatası veriyor. Temiz bir
CPython kullan.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.paths import exercise_env_dir, exercise_python  # noqa: E402

# PySide6 tekerlekleri için desteklenen aralık.
MIN_PYTHON = (3, 10)
MAX_PYTHON = (3, 14)

APP_ENV_DIR = PROJECT_ROOT / ".venv"


def app_python() -> Path:
    """Uygulama ortamındaki Python yorumlayıcısının yolu."""
    if sys.platform == "win32":
        return APP_ENV_DIR / "Scripts" / "python.exe"
    return APP_ENV_DIR / "bin" / "python"


def check_python_version() -> None:
    version = sys.version_info[:2]
    if version < MIN_PYTHON:
        sys.exit(
            f"Bu proje Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} veya üstünü "
            f"gerektiriyor. Şu an {version[0]}.{version[1]} kullanılıyor."
        )
    if version > MAX_PYTHON:
        print(
            f"UYARI: Python {version[0]}.{version[1]} kullanıyorsun. PySide6 "
            f"tekerlekleri {MAX_PYTHON[0]}.{MAX_PYTHON[1]} sürümüne kadar "
            f"güvenilir şekilde yayınlanıyor. Kurulum başarısız olursa "
            f"'py -3.13 tools/setup_env.py' ile dene."
        )


def run(command: list[str], description: str) -> None:
    print(f"\n> {description}")
    result = subprocess.run(command)
    if result.returncode != 0:
        sys.exit(f"Başarısız: {description}")


def create_env(env_dir: Path, requirements: Path, python_path: Path, label: str) -> None:
    if python_path.exists():
        print(f"{label} zaten kurulu: {env_dir}")
    else:
        run(
            [sys.executable, "-m", "venv", str(env_dir)],
            f"{label} oluşturuluyor: {env_dir}",
        )

    run(
        [str(python_path), "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
        f"{label}: pip güncelleniyor",
    )
    run(
        [str(python_path), "-m", "pip", "install", "-r", str(requirements)],
        f"{label}: paketler kuruluyor ({requirements.name})",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sanal ortamları kurar.")
    parser.add_argument("--app", action="store_true", help="sadece uygulama ortamı")
    parser.add_argument(
        "--exercises", action="store_true", help="sadece alıştırma ortamı"
    )
    args = parser.parse_args()

    # Hiçbiri seçilmediyse ikisini de kur.
    setup_app = args.app or not args.exercises
    setup_exercises = args.exercises or not args.app

    check_python_version()

    if setup_app:
        create_env(
            APP_ENV_DIR,
            PROJECT_ROOT / "requirements.txt",
            app_python(),
            "Uygulama ortamı",
        )

    if setup_exercises:
        create_env(
            exercise_env_dir(),
            PROJECT_ROOT / "requirements-exercises.txt",
            exercise_python(),
            "Alıştırma ortamı",
        )

    print("\nKurulum tamamlandı.")
    if setup_app:
        print(f"Uygulamayı çalıştırmak için:\n    {app_python()} app\\main.py")


if __name__ == "__main__":
    main()
