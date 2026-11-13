"""Uygulamanın kullandığı klasör yolları.

İki ayrı katman var ve bunlar karışmaz:

- **Kurulum klasörü**: uygulama kodu ve müfredat içeriği. Güncellemede
  tamamen değişebilir, üzerine yazılabilir.
- **Kullanıcı verisi klasörü** (`%APPDATA%\\Odyssey`; macOS'ta
  `~/Library/Application Support/Odyssey`): ilerleme, sınav notları,
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


def rust_vendor_dir() -> Path:
    """Programla gelen Rust paketlerinin (crate) kaynak kodu."""
    return install_root() / "rust-vendor"


def sandbox_dir() -> Path:
    """Kullanıcı kodunu çalıştıran yardımcı scriptin bulunduğu klasör."""
    return install_root() / "sandbox"


def _uses_mac_layout() -> bool:
    """macOS'un kendi veri klasörü (`~/Library/Application Support`) mi?"""
    return sys.platform == "darwin" and not os.environ.get("APPDATA")


def _data_root() -> Path:
    """Kullanıcı verilerinin bulunacağı üst klasör."""
    base = os.environ.get("APPDATA")
    if base:
        return Path(base)
    if _uses_mac_layout():
        return Path.home() / "Library" / "Application Support"
    # Linux'ta veya APPDATA tanımsızsa ev dizini kullanılır.
    return Path.home()


def _folder_name(name: str) -> str:
    """Windows'ta ve macOS'ta düz ad, diğerlerinde nokta ile başlayan gizli klasör."""
    if os.environ.get("APPDATA") or _uses_mac_layout():
        return name
    return _hidden_name(name)


def _hidden_name(name: str) -> str:
    return f".{name.lower()}"


def _legacy_sources() -> list[Path]:
    """Yeni veri klasörü yokken verisi taşınacak eski klasörler, öncelik sırasıyla."""
    if _uses_mac_layout():
        # 1.7.0'dan önce macOS'ta veri Linux'taki gibi ev dizininde gizli
        # klasördeydi (`~/.odyssey`).
        return [Path.home() / _hidden_name(name) for name in (APP_DIR_NAME, *LEGACY_APP_DIR_NAMES)]
    root = _data_root()
    return [root / _folder_name(name) for name in LEGACY_APP_DIR_NAMES]


def _migrate_legacy_data(target: Path) -> None:
    """Uygulamanın eski adıyla açılmış veri klasörünü yenisine taşır.

    Uygulamanın adı değiştiğinde kullanıcının ilerlemesi, yazdığı kodlar ve
    profili eski klasörde kalıyordu; uygulama boş açılıp her şeyi kaybetmiş
    gibi görünüyordu. Taşıma yalnızca bir kez, yeni klasör henüz yokken
    yapılıyor. macOS'ta veri klasörünün yeri değiştiği için de aynı yol
    kullanılıyor (`_legacy_sources`).
    """
    if target.exists():
        return

    for source in _legacy_sources():
        if not source.is_dir():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            source.rename(target)
        except OSError:
            # Taşınamazsa kopyalamayı deniyoruz; eski klasör olduğu yerde
            # kalır, veri hiçbir durumda silinmez. Kopya önce yandaki geçici
            # klasöre yazılıp bitince adını alıyor: yarıda kesilirse hedef
            # oluşmuyor ve bir sonraki açılışta yeniden deneniyor.
            gecici = target.with_name(target.name + ".tmp")
            shutil.copytree(source, gecici, dirs_exist_ok=True)
            gecici.rename(target)
        return


def rust_build_dir() -> Path:
    """Paketli Rust alıştırmalarının paylaştığı derleme önbelleği."""
    return user_data_dir() / "rust-build"


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
    """İlerleme veritabanının günlük yedekleri (`app/core/backup.py`)."""
    return user_data_dir() / "backups"


def logs_dir() -> Path:
    """Günlük kaydının klasörü (`app/core/log.py`)."""
    return user_data_dir() / "logs"


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


def artifacts_dir() -> Path:
    """Kullanıcının kodunun ürettiği görsellerin durduğu klasör.

    Çalışma klasörü her çalıştırmadan sonra siliniyor; içinde üretilen
    grafik de onunla gidiyordu. Gösterilebilmesi için buraya alınıyor.
    Her çalıştırmada baştan yazılıyor: burada yalnızca **son** çalıştırmanın
    çıktısı duruyor, birikmiyor.
    """
    path = user_data_dir() / "artifacts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def workspace_dir() -> Path:
    """Alıştırmaların çalıştırıldığı geçici klasör."""
    path = user_data_dir() / "workspace"
    path.mkdir(parents=True, exist_ok=True)
    return path
