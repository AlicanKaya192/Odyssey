"""Günlük kaydı: `%APPDATA%\\Odyssey\\logs\\odyssey.log`.

Bir şey ters gidince sebebi kullanıcının ekranında görünmeyebiliyor. 0.9.1
güncellemesini Windows engellediğinde program "indirilemedi" diyordu; gerçek
sebep ancak Windows'un kendi kayıtlarından bulunabildi. Burada yakalanan
hatalar ve beklenmeyen çöküşler bir dosyaya yazılıyor; hata bildirirken o
dosya eklenebiliyor.

- Dosya en fazla `MAX_BYTES`, yanında `BACKUPS` eski parça; büyümüyor.
- **Kullanıcının içeriği yazılmaz:** kod, not metni, cevaplar. Yalnızca ne
  olduğu ve hata ayrıntısı.
- Ağa hiçbir şey gönderilmiyor.
- Kayıt kurulamazsa (salt okunur disk gibi) program yine açılıyor.
"""

from __future__ import annotations

import logging
import logging.handlers
import platform
import sys
import threading
from pathlib import Path

FILE_NAME = "odyssey.log"
MAX_BYTES = 512 * 1024
BACKUPS = 2
FORMAT = "%(asctime)s %(levelname)s [%(process)d] %(name)s: %(message)s"

_configured = False


def setup(role: str = "app") -> Path | None:
    """Kaydı açar; dosyanın yolunu döndürür (açılamazsa None).

    `role` satırlarda hangi sürecin yazdığını gösteriyor: arayüz (`app`) ya
    da arka plandaki hatırlatma denetleyicisi (`reminder`).
    """
    global _configured
    if _configured:
        return None
    from ..paths import logs_dir
    from ..version import APP_VERSION

    try:
        klasor = logs_dir()
        klasor.mkdir(parents=True, exist_ok=True)
        yol = klasor / FILE_NAME
        handler = logging.handlers.RotatingFileHandler(
            yol, maxBytes=MAX_BYTES, backupCount=BACKUPS, encoding="utf-8", delay=True
        )
    except OSError:
        return None
    handler.setFormatter(logging.Formatter(FORMAT))
    kok = logging.getLogger()
    kok.addHandler(handler)
    kok.setLevel(logging.INFO)
    _configured = True

    _install_hooks()
    logging.getLogger("odyssey").info(
        "%s başladı: Odyssey %s, Python %s, %s %s",
        role, APP_VERSION, platform.python_version(), platform.system(), platform.version(),
    )
    return yol


def _install_hooks() -> None:
    """Yakalanmayan hatalar da kayda düşsün; eski davranış (konsola basma) sürer."""
    onceki = sys.excepthook

    def kanca(tur, deger, iz):
        if not issubclass(tur, KeyboardInterrupt):
            logging.getLogger("odyssey").critical("Yakalanmayan hata", exc_info=(tur, deger, iz))
        onceki(tur, deger, iz)

    sys.excepthook = kanca

    onceki_is = threading.excepthook

    def is_kancasi(args):
        logging.getLogger("odyssey").critical(
            "İş parçacığında yakalanmayan hata (%s)",
            args.thread.name if args.thread else "?",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )
        onceki_is(args)

    threading.excepthook = is_kancasi


def get(name: str) -> logging.Logger:
    """Modül için kayıtçı: `log.get(__name__)`."""
    return logging.getLogger(name)
