"""İlerleme veritabanının günlük yedeği ve bozulursa geri yüklenmesi.

Bütün ilerleme tek bir dosyada (`progress.db`). Elektrik kesilir ya da disk
hata verirse o dosya bozulabilir ve kişinin haftalarca emeği bir anda gider.

- Her açılışta, o gün yedek alınmadıysa **sağlam** veritabanının bir kopyası
  `backups/progress-YYYY-MM-DD.db` olarak alınıyor; en yeni `KEEP` tanesi
  duruyor. Bozuk dosya yedeklenmiyor, yoksa sağlam eski yedekleri sırayla
  dışarı iterdi.
- Kopya SQLite'ın kendi yedekleme yoluyla (`Connection.backup`) alınıyor:
  dosyayı düz kopyalamak, yazılırken yakalanırsa yarım bir kopya bırakırdı.
- Açılışta veritabanı açılamıyor ya da `PRAGMA quick_check` sorun buluyorsa
  bozuk dosya `progress.broken-<zaman>.db` adıyla kenara alınıyor (silinmiyor)
  ve sağlam olan en yeni yedek yerine konuyor. Kişiye bir kez söyleniyor.
"""

from __future__ import annotations

import os
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from . import log

KEEP = 3
PREFIX = "progress-"

_log = log.get(__name__)


@dataclass
class Restored:
    """Açılışta yedekten dönüldüyse: hangi günün yedeği, bozuk dosya nerede."""

    backup_day: str
    broken_path: Path


def _readonly(path: Path) -> str:
    """Salt okunur SQLite adresi; yoldaki boşluk ve Türkçe harf kodlanıyor."""
    return f"{path.resolve().as_uri()}?mode=ro"


def is_healthy(path: Path) -> bool:
    """Dosya açılıyor ve SQLite'ın hızlı denetiminden geçiyor mu."""
    if not path.exists():
        return False
    try:
        baglanti = sqlite3.connect(_readonly(path), uri=True)
        try:
            satir = baglanti.execute("PRAGMA quick_check").fetchone()
        finally:
            baglanti.close()
    except sqlite3.DatabaseError:
        return False
    return bool(satir) and satir[0] == "ok"


def backups(folder: Path) -> list[Path]:
    """Yedekler, en yeni önce."""
    if not folder.exists():
        return []
    return sorted(folder.glob(f"{PREFIX}*.db"), reverse=True)


def daily_backup(db: Path, folder: Path, today: date | None = None) -> Path | None:
    """O gün yedek yoksa alır; alınan yedeğin yolunu döndürür."""
    gun = (today or date.today()).isoformat()
    hedef = folder / f"{PREFIX}{gun}.db"
    if hedef.exists() or not db.exists():
        return None
    if not is_healthy(db):
        _log.warning("Veritabanı denetimden geçmedi; bugün yedek alınmadı")
        return None
    gecici = hedef.with_suffix(".tmp")
    try:
        folder.mkdir(parents=True, exist_ok=True)
        kaynak = sqlite3.connect(_readonly(db), uri=True)
        try:
            varis = sqlite3.connect(gecici)
            try:
                kaynak.backup(varis)
            finally:
                varis.close()
        finally:
            kaynak.close()
        os.replace(gecici, hedef)
    except (OSError, sqlite3.Error):
        _log.exception("Yedek alınamadı")
        gecici.unlink(missing_ok=True)
        return None
    _prune(folder)
    _log.info("Yedek alındı: %s", hedef.name)
    return hedef


def _prune(folder: Path) -> None:
    for eski in backups(folder)[KEEP:]:
        try:
            eski.unlink()
        except OSError:
            _log.warning("Eski yedek silinemedi: %s", eski.name)


def recover(db: Path, folder: Path) -> Restored | None:
    """Veritabanı bozuksa kenara alır ve sağlam en yeni yedeği yerine koyar.

    Sağlamsa ya da hiç yoksa (ilk açılış) hiçbir şey yapmaz. Sağlam yedek
    yoksa bozuk dosya yine kenara alınıyor: program boş bir veritabanıyla
    açılıyor, eski dosya elle kurtarılmak üzere duruyor.
    """
    if not db.exists() or is_healthy(db):
        return None
    _log.error("Veritabanı bozuk: %s", db)
    damga = datetime.now().strftime("%Y%m%d-%H%M%S")
    bozuk = db.with_name(f"progress.broken-{damga}.db")
    try:
        os.replace(db, bozuk)
        for ek in ("-wal", "-shm", "-journal"):
            yan = db.with_name(db.name + ek)
            if yan.exists():
                os.replace(yan, bozuk.with_name(bozuk.name + ek))
    except OSError:
        _log.exception("Bozuk veritabanı kenara alınamadı")
        return None
    for yedek in backups(folder):
        if not is_healthy(yedek):
            continue
        try:
            shutil.copy2(yedek, db)
        except OSError:
            _log.exception("Yedek geri yüklenemedi: %s", yedek.name)
            continue
        gun = yedek.stem[len(PREFIX):]
        _log.warning("Yedekten geri yüklendi: %s", yedek.name)
        return Restored(backup_day=gun, broken_path=bozuk)
    _log.error("Sağlam yedek bulunamadı; boş veritabanıyla açılıyor")
    return Restored(backup_day="", broken_path=bozuk)
