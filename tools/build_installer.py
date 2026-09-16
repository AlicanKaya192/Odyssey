"""Paketlenmiş uygulamadan kurulum programı üretir.

Çıktı: `dist/Odyssey-<sürüm>-setup.exe`

Önce `tools/build_exe.py` çalışmış olmalı (`dist/Odyssey`). Kurulum betiği
`installer/odyssey.iss`; bu araç Inno Setup derleyicisini (`ISCC.exe`)
bulup sürüm numarasını `app/version.py`'den veriyor.

Inno Setup ücretsiz: https://jrsoftware.org/isinfo.php

Kullanım:
    .venv\\Scripts\\python tools/build_installer.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.version import APP_VERSION  # noqa: E402

SCRIPT = PROJECT_ROOT / "installer" / "odyssey.iss"
SOURCE = PROJECT_ROOT / "dist" / "Odyssey"
OUTPUT = PROJECT_ROOT / "dist"

# Inno Setup 6'nın olağan kurulum yerleri.
CANDIDATES = (
    Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Inno Setup 6" / "ISCC.exe",
    Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Inno Setup 6" / "ISCC.exe",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe",
)


def find_compiler() -> Path | None:
    bulunan = shutil.which("ISCC") or shutil.which("iscc")
    if bulunan:
        return Path(bulunan)
    for aday in CANDIDATES:
        if aday.exists():
            return aday
    return None


def main() -> int:
    if not (SOURCE / "Odyssey.exe").exists():
        print("dist/Odyssey bulunamadı. Önce: python tools/build_exe.py")
        return 1

    derleyici = find_compiler()
    if derleyici is None:
        print("Inno Setup (ISCC.exe) bulunamadı. Kurun: https://jrsoftware.org/isinfo.php")
        return 1

    hedef = OUTPUT / f"Odyssey-{APP_VERSION}-setup.exe"
    hedef.unlink(missing_ok=True)

    print(f"Odyssey {APP_VERSION} kurulum programı üretiliyor — birkaç dakika sürer...")
    sonuc = subprocess.run(
        [
            str(derleyici),
            f"/DAppVersion={APP_VERSION}",
            f"/DSourceDir={SOURCE}",
            f"/DOutputDir={OUTPUT}",
            str(SCRIPT),
        ],
        cwd=str(SCRIPT.parent),
    )
    if sonuc.returncode != 0 or not hedef.exists():
        print("Kurulum programı üretilemedi.")
        return 1

    print(f"\nHazır: {hedef}")
    print(f"Boyut: {hedef.stat().st_size / 1024 / 1024:.0f} MB")
    print(f"GitHub'a bu dosyayı `setup-{APP_VERSION}` etiketiyle yükleyin (v ile değil).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
