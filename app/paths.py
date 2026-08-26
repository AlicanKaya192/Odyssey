"""Uygulamanın kullandığı klasör yolları.

İki ayrı katman var ve bunlar karışmaz:

- **Kurulum klasörü**: uygulama kodu ve müfredat içeriği. Güncellemede
  tamamen değişebilir, üzerine yazılabilir.
- **Kullanıcı verisi klasörü** (`%APPDATA%\\ProjeA`): ilerleme, sınav notları,
  yazılan kodlar, kullanıcı notları, profil, rozetler ve ayarlar. Güncelleme
  buraya asla dokunmaz.

Bu ayrım sayesinde kullanıcı uygulamayı güncellediğinde veya silip yeniden
kurduğunda hiçbir verisi kaybolmaz.
"""

from __future__ import annotations

import os
from pathlib import Path

from .version import APP_DIR_NAME


def install_root() -> Path:
    """Uygulamanın kurulu olduğu klasör (app/ ve content/ burada)."""
    return Path(__file__).resolve().parent.parent


def content_dir() -> Path:
    """Müfredat içeriğinin bulunduğu klasör."""
    return install_root() / "content"


def sandbox_dir() -> Path:
    """Kullanıcı kodunu çalıştıran yardımcı scriptin bulunduğu klasör."""
    return install_root() / "sandbox"


def user_data_dir() -> Path:
    """Kullanıcı verilerinin tutulduğu klasör. Güncellemeden etkilenmez."""
    base = os.environ.get("APPDATA")
    if base:
        path = Path(base) / APP_DIR_NAME
    else:
        # Windows dışında veya APPDATA tanımsızsa ev dizinine düşülür.
        path = Path.home() / f".{APP_DIR_NAME.lower()}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def database_path() -> Path:
    """İlerleme veritabanının tam yolu."""
    return user_data_dir() / "progress.db"


def backups_dir() -> Path:
    """Güncelleme öncesi alınan veritabanı yedeklerinin klasörü."""
    path = user_data_dir() / "backups"
    path.mkdir(parents=True, exist_ok=True)
    return path


def exercise_env_dir() -> Path:
    """Kullanıcı kodunun çalıştığı sanal ortamın klasörü."""
    return user_data_dir() / "exercise-env"


def exercise_python() -> Path:
    """Kullanıcı kodunu çalıştıracak Python yorumlayıcısının yolu."""
    env = exercise_env_dir()
    if os.name == "nt":
        return env / "Scripts" / "python.exe"
    return env / "bin" / "python"


def workspace_dir() -> Path:
    """Alıştırmaların çalıştırıldığı geçici klasör."""
    path = user_data_dir() / "workspace"
    path.mkdir(parents=True, exist_ok=True)
    return path
