"""macOS paketinden (`dist/Odyssey.app`) dağıtılacak disk görüntüsünü kurar.

Çıktı: `dist/Odyssey-<sürüm>-macos-arm64.dmg`

Görüntünün içinde `Odyssey.app` ve `Applications` klasörüne bir bağlantı
var: kişi uygulamayı sürükleyip bırakarak kuruyor. Görüntü sıkıştırılmış ve
salt okunur (`UDZO`). İmza `build_exe.py`'de atıldı; burada `.app` olduğu
gibi kopyalanıyor (`ditto` imzayı ve bağlantıları koruyor).

Dosya adı Windows güncelleyicisinin seçtikleriyle çakışmıyor: o yalnızca
`-setup.exe` ile biten tam kurulumu ve `Odyssey-<yeni>-patch-<eski>.exe`
yamasını arıyor (`app/core/updater.py`).

Yalnızca macOS'ta, Apple Silicon'da çalışır (`hdiutil` ve `ditto` macOS
araçları; paket tek mimarili, `arm64`).

Kullanım:
    python tools/build_exe.py --temiz
    python tools/build_dmg.py
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from build_exe import APP_NAME, package_layout  # noqa: E402
from app.version import APP_VERSION  # noqa: E402

ARCHITECTURE = "arm64"


def dmg_path(dist: Path | None = None) -> Path:
    dist = dist or PROJECT_ROOT / "dist"
    return dist / f"{APP_NAME}-{APP_VERSION}-macos-{ARCHITECTURE}.dmg"


def build_dmg(app: Path, staging: Path, target: Path) -> int:
    """`staging` klasörüne `.app` + `Applications` bağlantısını koyup görüntüyü yazar."""
    copy = ["ditto", str(app), str(staging / app.name)]
    result = subprocess.run(copy)
    if result.returncode != 0:
        print("Kopyalanamadı:", " ".join(copy))
        return result.returncode
    os.symlink("/Applications", staging / "Applications")

    create = [
        "hdiutil", "create",
        "-volname", APP_NAME,
        "-srcfolder", str(staging),
        "-ov",                      # aynı adlı eski görüntünün üstüne yaz
        "-format", "UDZO",
        str(target),
    ]
    result = subprocess.run(create)
    if result.returncode != 0:
        print("Disk görüntüsü kurulamadı:", " ".join(create))
        return result.returncode

    verify = ["hdiutil", "verify", str(target)]
    result = subprocess.run(verify)
    if result.returncode != 0:
        print("Disk görüntüsü doğrulanamadı:", " ".join(verify))
    return result.returncode


def main() -> int:
    if sys.platform != "darwin":
        print("Disk görüntüsü yalnızca macOS'ta kurulabiliyor (hdiutil).")
        return 1
    if platform.machine() != ARCHITECTURE:
        print(f"Bu Mac {platform.machine()}; paket ve dosya adı {ARCHITECTURE} için.")
        return 1

    app = package_layout().root
    if not app.is_dir():
        print("Paket bulunamadı:", app)
        print("Önce: python tools/build_exe.py --temiz")
        return 1

    target = dmg_path()
    with tempfile.TemporaryDirectory(prefix="odyssey-dmg-") as staging:
        status = build_dmg(app, Path(staging), target)
    if status != 0:
        return status

    size = target.stat().st_size / 1024 / 1024
    print(f"Hazır: {target}  ({size:.0f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
