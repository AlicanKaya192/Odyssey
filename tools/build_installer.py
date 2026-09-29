"""Paketlenmiş uygulamadan kurulum programını (ve fark kurulumlarını) üretir.

Çıktı:
    dist/Odyssey-<sürüm>-setup.exe            tam kurulum (her zaman)
    dist/Odyssey-<sürüm>-patch-<eski>.exe     fark kurulumu (önceki sürümden)
    installer/manifests/<sürüm>.json.gz       bu paketin dosya kaydı

Önce `tools/build_exe.py` çalışmış olmalı (`dist/Odyssey`). Kurulum betiği
`installer/odyssey.iss`; bu araç Inno Setup derleyicisini (`ISCC.exe`)
bulup sürüm numarasını `app/version.py`'den veriyor.

**Fark kurulumu (0.9.1'den itibaren).** Her tam kurulumda paketin bütün
dosyalarının SHA-256'sı ve boyutu `installer/manifests/<sürüm>.json.gz`
içine yazılıyor. Sonraki sürümde bu kayıt bugünkü paketle karşılaştırılıyor:
değişen ve yeni dosyalar yamaya giriyor, kaldırılanlar yamada siliniyor.
PySide6 ve Qt'nin DLL'leri sürümler arasında aynı kaldığı için yama tam
kurulumun küçük bir kısmı. Kaydın **yayınlanan** paketten alınması
gerekiyor: yayından sonra `dist` yeniden derlenirse kayıt da yenilenir,
bu yüzden araç kaydı yalnızca tam kurulumla birlikte yazıyor.

Varsayılan olarak yalnızca bir önceki sürümün (kaydı olan en yeni eski
sürüm) yaması üretiliyor; `--patch-from 0.9.1 --patch-from 0.9.2` ile
başka sürümlerden de. `--no-patch` yamayı atlıyor.

Inno Setup ücretsiz: https://jrsoftware.org/isinfo.php

Kullanım:
    .venv\\Scripts\\python tools/build_installer.py [--patch-from X] [--no-patch]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.version import APP_VERSION  # noqa: E402

SCRIPT = PROJECT_ROOT / "installer" / "odyssey.iss"
SOURCE = PROJECT_ROOT / "dist" / "Odyssey"
OUTPUT = PROJECT_ROOT / "dist"
MANIFESTS = PROJECT_ROOT / "installer" / "manifests"

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


def version_key(text: str) -> tuple[int, ...]:
    return tuple(int(p) for p in text.split(".") if p.isdigit())


# --- dosya kaydı ---------------------------------------------------------


def manifest_of(root: Path) -> dict[str, list]:
    """Klasördeki her dosya için {göreli yol: [sha256, boyut]}."""
    dosyalar: dict[str, list] = {}
    for yol in sorted(root.rglob("*")):
        if not yol.is_file():
            continue
        ozet = hashlib.sha256()
        with yol.open("rb") as akis:
            for parca in iter(lambda: akis.read(1 << 20), b""):
                ozet.update(parca)
        dosyalar[yol.relative_to(root).as_posix()] = [ozet.hexdigest(), yol.stat().st_size]
    return dosyalar


def write_manifest(version: str, files: dict[str, list]) -> Path:
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    yol = MANIFESTS / f"{version}.json.gz"
    veri = json.dumps({"version": version, "files": files}, separators=(",", ":"))
    yol.write_bytes(gzip.compress(veri.encode("utf-8")))
    return yol


def read_manifest(version: str) -> dict[str, list] | None:
    yol = MANIFESTS / f"{version}.json.gz"
    if not yol.exists():
        return None
    return json.loads(gzip.decompress(yol.read_bytes()))["files"]


def previous_version() -> str | None:
    """Kaydı olan, bugünkünden eski en yeni sürüm."""
    eskiler = [
        p.name[: -len(".json.gz")]
        for p in MANIFESTS.glob("*.json.gz")
        if version_key(p.name[: -len(".json.gz")]) < version_key(APP_VERSION)
    ]
    return max(eskiler, key=version_key) if eskiler else None


# --- fark ----------------------------------------------------------------


def diff(old: dict[str, list], new: dict[str, list]) -> tuple[list[str], list[str]]:
    """(yazılacaklar, silinecekler): değişen + yeni dosyalar, kaldırılanlar."""
    yazilacak = [p for p, bilgi in new.items() if old.get(p) != bilgi]
    silinecek = [p for p in old if p not in new]
    return sorted(yazilacak), sorted(silinecek)


def _inno(path: str) -> str:
    """Inno Setup yolu: ters bölü, `{` sabit başlangıcı sayılmasın diye `{{`."""
    return path.replace("/", "\\").replace("{", "{{")


def patch_list(write: list[str], remove: list[str]) -> str:
    """Betiğe `#include` edilen [InstallDelete] ve [Files] bölümleri."""
    satirlar = ["[InstallDelete]"]
    for yol in remove:
        satirlar.append(f'Type: files; Name: "{{app}}\\{_inno(yol)}"')
    satirlar.append("")
    satirlar.append("[Files]")
    for yol in write:
        klasor = yol.rsplit("/", 1)[0] if "/" in yol else ""
        hedef = "{app}" + ("\\" + _inno(klasor) if klasor else "")
        satirlar.append(
            f'Source: "{{#SourceDir}}\\{_inno(yol)}"; DestDir: "{hedef}"; Flags: ignoreversion'
        )
    return "\n".join(satirlar) + "\n"


# --- derleme -------------------------------------------------------------


def compile_script(compiler: Path, *defines: str) -> int:
    return subprocess.run(
        [str(compiler), f"/DAppVersion={APP_VERSION}", f"/DSourceDir={SOURCE}",
         f"/DOutputDir={OUTPUT}", *defines, str(SCRIPT)],
        cwd=str(SCRIPT.parent),
    ).returncode


def build_patch(compiler: Path, base: str, current: dict[str, list]) -> Path | None:
    eski = read_manifest(base)
    if eski is None:
        print(f"{base} için dosya kaydı yok (installer/manifests); yama atlandı.")
        return None
    yazilacak, silinecek = diff(eski, current)
    hedef = OUTPUT / f"Odyssey-{APP_VERSION}-patch-{base}.exe"
    hedef.unlink(missing_ok=True)
    boyut = sum(current[p][1] for p in yazilacak)
    print(f"{base} → {APP_VERSION}: {len(yazilacak)} dosya yazılacak "
          f"({boyut / 1024 / 1024:.0f} MB), {len(silinecek)} dosya silinecek.")

    with tempfile.TemporaryDirectory(prefix="odyssey_patch_") as tmp:
        liste = Path(tmp) / "patch-files.iss"
        liste.write_text(patch_list(yazilacak, silinecek), encoding="utf-8-sig")
        kod = compile_script(compiler, f"/DPatchFrom={base}", f"/DPatchList={liste}")
    if kod != 0 or not hedef.exists():
        print(f"{base} yaması üretilemedi.")
        return None
    return hedef


def main() -> int:
    ayrac = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ayrac.add_argument("--patch-from", action="append", default=None,
                       help="bu sürümden fark kurulumu üret (birden çok verilebilir)")
    ayrac.add_argument("--no-patch", action="store_true", help="fark kurulumu üretme")
    secenek = ayrac.parse_args()

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
    if compile_script(derleyici) != 0 or not hedef.exists():
        print("Kurulum programı üretilemedi.")
        return 1

    print("Dosya kaydı çıkarılıyor...")
    bugun = manifest_of(SOURCE)
    kayit = write_manifest(APP_VERSION, bugun)

    yamalar = []
    if not secenek.no_patch:
        tabanlar = secenek.patch_from or [v for v in [previous_version()] if v]
        for taban in tabanlar:
            yama = build_patch(derleyici, taban, bugun)
            if yama is not None:
                yamalar.append(yama)

    print(f"\nHazır: {hedef}")
    print(f"Boyut: {hedef.stat().st_size / 1024 / 1024:.0f} MB")
    for yama in yamalar:
        print(f"Yama:  {yama.name}  ({yama.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"Dosya kaydı: {kayit.relative_to(PROJECT_ROOT)} (depoya commit'lenir)")
    print(f"GitHub'a bu dosyaları `setup-{APP_VERSION}` etiketiyle yükleyin (v ile değil).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
