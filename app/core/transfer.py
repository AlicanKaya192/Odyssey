"""İlerlemeyi dışa ve içe aktarma (başka bir bilgisayara taşımak).

Alican iki bilgisayar kullanıyor ve ilerlemesi ikisinde ayrıydı. Dışa
aktarma ilerlemeyi, notları, ayarları ve profil fotoğrafını tek bir
`.odyssey` dosyasına (zip) koyuyor; içe aktarma o dosyadakini bu
bilgisayardakinin **yerine** koyuyor (birleştirme yok: iki ilerlemeyi
satır satır birleştirmek hangisinin doğru olduğunu tahmin etmek demek).

- Veritabanı SQLite'ın kendi yedekleme yoluyla kopyalanıyor (açıkken de
  tutarlı kopya).
- **Gelen dosya başkasından gelebilir:** zip diske açılmıyor, bellekte
  okunuyor; boyut sınırı var, okurken sınırın bir bayt fazlasından çoğu
  okunmuyor (başlıktaki boyut yalan olabilir). Veritabanı ancak
  `quick_check`'ten geçip beklenen tabloları taşıyorsa kabul ediliyor;
  daha yeni bir programdan geldiyse (şeması büyükse) reddediliyor.
- Değiştirme program **kapalıyken** yapılıyor: içe aktarma dosyayı
  `pending-import/` klasörüne koyup programı yeniden başlatıyor, açılış
  (`apply_pending`) veritabanını açmadan önce yerine koyuyor. Açık bir
  veritabanının altını değiştirmek ekranları tutarsız bırakırdı.
- Değiştirmeden önce mevcut ilerleme `backups/progress-before-import-*.db`
  olarak saklanıyor (geri dönülebilsin).
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import tempfile
import time
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from . import log
from .backup import is_healthy

EXTENSION = ".odyssey"
FORMAT = 1
MANIFEST = "manifest.json"
DATABASE = "progress.db"
AVATAR = "avatar.png"
PENDING = "pending-import"

MAX_DATABASE_BYTES = 200 * 1024 * 1024
MAX_AVATAR_BYTES = 8 * 1024 * 1024
MAX_MANIFEST_BYTES = 64 * 1024
REQUIRED_TABLES = {"profile", "settings", "schema_version"}

_log = log.get(__name__)


class TransferError(Exception):
    """Dosya içe aktarılamıyor; `code` arayüzdeki metnin anahtarı."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass
class Archive:
    """Okunmuş, doğrulanmış bir aktarım dosyası."""

    database: bytes
    avatar: bytes | None
    app_version: str
    created_at: str
    schema: int
    name: str
    quizzes_passed: int


# --- dışa aktarma ---------------------------------------------------------


def export_to(target: Path, database: Path, avatar: Path | None) -> Path:
    """İlerlemeyi `target` dosyasına yazar (uzantı yoksa `.odyssey` eklenir)."""
    from ..version import APP_VERSION

    if target.suffix.lower() != EXTENSION:
        target = target.with_name(target.name + EXTENSION)
    with tempfile.TemporaryDirectory(prefix="odyssey_export_") as tmp:
        kopya = Path(tmp) / DATABASE
        kaynak = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
        try:
            varis = sqlite3.connect(kopya)
            try:
                kaynak.backup(varis)
            finally:
                varis.close()
        finally:
            kaynak.close()
        sema = _schema(kopya)
        bilgi = {
            "format": FORMAT,
            "app_version": APP_VERSION,
            "schema": sema,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        gecici = target.with_name(target.name + ".part")
        with zipfile.ZipFile(gecici, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(MANIFEST, json.dumps(bilgi, ensure_ascii=False, indent=2))
            z.write(kopya, DATABASE)
            if avatar is not None and avatar.is_file():
                z.write(avatar, AVATAR)
        os.replace(gecici, target)
    _log.info("İlerleme dışa aktarıldı (%s, şema %s)", target.name, sema)
    return target


def _schema(path: Path) -> int:
    baglanti = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    try:
        satir = baglanti.execute("SELECT MAX(version) FROM schema_version").fetchone()
        return int(satir[0] or 0)
    finally:
        baglanti.close()


# --- içe aktarma: okuma ve doğrulama --------------------------------------


def _read_limited(z: zipfile.ZipFile, name: str, limit: int) -> bytes:
    with z.open(name) as f:
        veri = f.read(limit + 1)
    if len(veri) > limit:
        raise TransferError("too_big")
    return veri


def read_archive(path: Path) -> Archive:
    """Dosyayı okuyup doğrular; uygun değilse `TransferError`."""
    from ..version import SCHEMA_VERSION

    try:
        z = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile):
        raise TransferError("not_odyssey") from None
    with z:
        adlar = set(z.namelist())
        if MANIFEST not in adlar or DATABASE not in adlar:
            raise TransferError("not_odyssey")
        try:
            bilgi = json.loads(_read_limited(z, MANIFEST, MAX_MANIFEST_BYTES))
        except ValueError:
            raise TransferError("not_odyssey") from None
        if not isinstance(bilgi, dict) or bilgi.get("format") != FORMAT:
            raise TransferError("not_odyssey")
        veri = _read_limited(z, DATABASE, MAX_DATABASE_BYTES)
        avatar = _read_limited(z, AVATAR, MAX_AVATAR_BYTES) if AVATAR in adlar else None

    with tempfile.TemporaryDirectory(prefix="odyssey_import_") as tmp:
        db = Path(tmp) / DATABASE
        db.write_bytes(veri)
        if not is_healthy(db):
            raise TransferError("damaged")
        baglanti = sqlite3.connect(f"{db.resolve().as_uri()}?mode=ro", uri=True)
        try:
            tablolar = {r[0] for r in baglanti.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'")}
            if not REQUIRED_TABLES <= tablolar:
                raise TransferError("not_odyssey")
            sema = int(baglanti.execute("SELECT MAX(version) FROM schema_version").fetchone()[0] or 0)
            profil = baglanti.execute("SELECT * FROM profile WHERE id = 1").fetchone()
            ad = ""
            if profil is not None:
                sutunlar = [d[0] for d in baglanti.execute("SELECT * FROM profile LIMIT 0").description]
                kayit = dict(zip(sutunlar, profil))
                ad = " ".join(str(kayit.get(k) or "") for k in ("first_name", "last_name")).strip()
            biten = 0
            if "section_progress" in tablolar:
                biten = int(baglanti.execute(
                    "SELECT COUNT(*) FROM section_progress WHERE quiz_passed = 1"
                ).fetchone()[0])
        except sqlite3.DatabaseError:
            raise TransferError("damaged") from None
        finally:
            baglanti.close()
    if sema > SCHEMA_VERSION:
        raise TransferError("newer")
    return Archive(
        database=veri,
        avatar=avatar,
        app_version=str(bilgi.get("app_version", "")),
        created_at=str(bilgi.get("created_at", "")),
        schema=sema,
        name=ad,
        quizzes_passed=biten,
    )


# --- içe aktarma: yerine koyma ----------------------------------------------


def stage(archive: Archive, data_dir: Path) -> Path:
    """Doğrulanmış dosyayı bir sonraki açılışta yerine konmak üzere bırakır."""
    klasor = data_dir / PENDING
    shutil.rmtree(klasor, ignore_errors=True)
    klasor.mkdir(parents=True)
    (klasor / DATABASE).write_bytes(archive.database)
    if archive.avatar is not None:
        (klasor / AVATAR).write_bytes(archive.avatar)
    _log.info("İçe aktarma bir sonraki açılışa bırakıldı")
    return klasor


def apply_pending(database: Path, avatar: Path, backups: Path, wait_seconds: float = 15) -> bool:
    """Bekleyen içe aktarma varsa mevcut ilerlemeyi yedekleyip yerine koyar.

    Program yeniden başlatılırken eski süreç birkaç saniye daha veritabanını
    açık tutabiliyor; Windows açık dosyanın yerine yazmaya izin vermediği için
    kısa aralıklarla yeniden deneniyor.
    """
    klasor = database.parent / PENDING
    yeni = klasor / DATABASE
    if not yeni.is_file():
        return False
    damga = datetime.now().strftime("%Y%m%d-%H%M%S")
    son = time.monotonic() + wait_seconds
    while True:
        try:
            backups.mkdir(parents=True, exist_ok=True)
            if database.exists():
                shutil.copy2(database, backups / f"progress-before-import-{damga}.db")
            if avatar.exists():
                shutil.copy2(avatar, backups / f"avatar-before-import-{damga}.png")
            os.replace(yeni, database)
            break
        except PermissionError:
            if time.monotonic() > son:
                _log.error("İçe aktarma uygulanamadı: veritabanı hâlâ açık")
                return False
            time.sleep(0.3)
    gelen_avatar = klasor / AVATAR
    try:
        if gelen_avatar.is_file():
            os.replace(gelen_avatar, avatar)
        elif avatar.exists():
            avatar.unlink()  # gelen ilerlemede fotoğraf yok; eskisi yedekte
    except OSError:
        _log.exception("Profil fotoğrafı içe aktarılamadı")
    shutil.rmtree(klasor, ignore_errors=True)
    _log.warning("İçe aktarılan ilerleme yerine kondu (önceki yedekte: %s)", damga)
    return True

