"""Uygulamanın kullandığı klasör yolları.

İki ayrı katman var ve bunlar karışmaz:

- **Kurulum klasörü**: uygulama kodu ve müfredat içeriği. Güncellemede
  tamamen değişebilir, üzerine yazılabilir.
- **Kullanıcı verisi klasörü** (`%APPDATA%\\Odyssey`): ilerleme, sınav notları,
  yazılan kodlar, kullanıcı notları, profil, rozetler ve ayarlar. Güncelleme
  buraya asla dokunmaz.

Bu ayrım sayesinde kullanıcı uygulamayı güncellediğinde veya silip yeniden
kurduğunda hiçbir verisi kaybolmaz.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from .version import APP_DIR_NAME, LEGACY_APP_DIR_NAMES


def is_frozen() -> bool:
    """Uygulama paketlenmiş bir `.exe` olarak mı çalışıyor?"""
    return getattr(sys, "frozen", False)


def install_root() -> Path:
    """Uygulamanın kurulu olduğu klasör (content/ ve sandbox/ burada).

    Paketlenmiş hâlde dosyalar geçici bir açılım klasöründe duruyor;
    kaynak koddan çalışırken proje kökünde.
    """
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent.parent


def app_dir() -> Path:
    """Uygulamanın **kurulu olduğu** klasör: `Odyssey.exe`'nin durduğu yer.

    `install_root()` ile karıştırılmamalı. Paketlenmiş hâlde `install_root`
    `_internal` klasörünü veriyor (veri dosyaları orada); güncelleme ise
    exe'nin bulunduğu üst klasörü değiştiriyor.

    Kaynak koddan çalışırken ikisi de proje kökü oluyor.
    """
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def content_dir() -> Path:
    """Müfredat içeriğinin bulunduğu klasör."""
    return install_root() / "content"


def sandbox_dir() -> Path:
    """Kullanıcı kodunu çalıştıran yardımcı scriptin bulunduğu klasör."""
    return install_root() / "sandbox"


def _data_root() -> Path:
    """Kullanıcı verilerinin bulunacağı üst klasör."""
    base = os.environ.get("APPDATA")
    if base:
        return Path(base)
    # Windows dışında veya APPDATA tanımsızsa ev dizini kullanılır.
    return Path.home()


def _folder_name(name: str) -> str:
    """Windows'ta düz ad, diğerlerinde nokta ile başlayan gizli klasör."""
    return name if os.environ.get("APPDATA") else f".{name.lower()}"


def _migrate_legacy_data(target: Path) -> None:
    """Uygulamanın eski adıyla açılmış veri klasörünü yenisine taşır.

    Uygulamanın adı değiştiğinde kullanıcının ilerlemesi, yazdığı kodlar ve
    profili eski klasörde kalıyordu; uygulama boş açılıp her şeyi kaybetmiş
    gibi görünüyordu. Taşıma yalnızca bir kez, yeni klasör henüz yokken
    yapılıyor.
    """
    if target.exists():
        return

    root = _data_root()
    for legacy in LEGACY_APP_DIR_NAMES:
        source = root / _folder_name(legacy)
        if not source.is_dir():
            continue
        try:
            source.rename(target)
        except OSError:
            # Taşınamazsa kopyalamayı deniyoruz; eski klasör olduğu yerde
            # kalır, veri hiçbir durumda silinmez.
            shutil.copytree(source, target, dirs_exist_ok=True)
        return


def user_data_dir() -> Path:
    """Kullanıcı verilerinin tutulduğu klasör. Güncellemeden etkilenmez."""
    path = _data_root() / _folder_name(APP_DIR_NAME)
    _migrate_legacy_data(path)
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


def updates_dir() -> Path:
    """İndirilen ve açılan güncellemelerin durduğu klasör.

    Kullanıcı verisiyle aynı yerde ama ayrı bir alt klasörde: güncelleme
    yarıda kalırsa buradaki her şey silinebiliyor, ilerleme etkilenmiyor.
    """
    path = user_data_dir() / "updates"
    path.mkdir(parents=True, exist_ok=True)
    return path


def workspace_dir() -> Path:
    """Alıştırmaların çalıştırıldığı geçici klasör."""
    path = user_data_dir() / "workspace"
    path.mkdir(parents=True, exist_ok=True)
    return path
