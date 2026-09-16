"""Güncellemeyi indiren, doğrulayan ve kurulum programını başlatan taraf.

`updates.py` yalnızca "yeni sürüm var mı" diye soruyor; indirme ve kurulum
bu modülde.

## Akış

1. **İndir** — sürümün kurulum programı (`Odyssey-<sürüm>-setup.exe`)
   `%APPDATA%\\Odyssey\\updates` altına iniyor, ilerleme gösteriliyor.
2. **Doğrula** — boyut sunucunun söylediğiyle aynı mı, dosya bir Windows
   programı mı (`MZ`). İndirilen şey çalıştırılacak; sağlamlığına bakmadan
   başlatılmıyor.
3. **Devret** — kurulum programı sessiz kipte başlatılıyor, uygulama
   kapanıyor. Kurulum bu sürecin bitmesini bekliyor, dosyaları yazıyor,
   kısayolları koyuyor ve Odyssey'i yeniden açıyor (`installer/odyssey.iss`).

## Zip'ten kurulum programına geçiş

0.8.2.1'e kadar sürümler zip olarak dağıtılıyordu ve uygulama kendi
klasörünü yerinde değiştiriyordu. 0.8.3'ten itibaren bütün sürümler kurulum
programıyla geliyor; zip yolu kaldırıldı. Zip'ten kurulum programına geçişi
0.8.2.1 köprüsü yapıyor, 0.8.3'ün kodu değil. Etiket ve dosya adı kuralları
için `updates.py` → `SETUP_TAG_PREFIX`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from ..paths import app_dir, updates_dir
from .updates import RELEASES_PAGE, USER_AGENT

# Kurulum dosyası: `Odyssey-0.8.3-setup.exe`.
INSTALLER_PREFIX = "Odyssey-"
INSTALLER_SUFFIX = "-setup.exe"

# Kurulum programına verilen parametreler. Adlar kurulum betiğiyle
# (`installer/odyssey.iss`, `{param:OLDDIR}` / `{param:OLDPID}`) aynı.
#
# - `/SILENT`: soru sormadan kurar, yalnızca ilerleme penceresi görünür.
# - `/SUPPRESSMSGBOXES /NORESTART /SP-`: hiçbir kutu, yeniden başlatma ya da
#   "kurmak istiyor musunuz" sorusu yok.
# - `/OLDPID`: kapanması beklenen bu süreç; dosyaları kilitli tutuyor.
# - `/OLDDIR`: yalnızca uygulama **zip'ten** çalışıyorsa (kurulu değilse)
#   gönderiliyor. Kurulum bittikten sonra o klasördeki `Odyssey.exe` ve
#   `_internal` siliniyor. Kurulu bir uygulama bunu göndermiyor: kendi
#   klasörünü göndermesi kurulumun yeni yazdığı dosyaları silmeye kalkması
#   olurdu (betik ayrıca yolları karşılaştırıyor).
INSTALLER_ARGS = ("/SILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-")

# İndirme adresi yalnızca burada başlayabilir. Sunucudan gelen bir adresi
# doğrulamadan indirmek, güncelleme akışını bir dosya indirme aracına
# çevirirdi.
DOWNLOAD_PREFIX = "https://github.com/AlicanKaya192/Odyssey/releases/download/"

# İndirme parçası. Küçük tutuldu: ilerleme çubuğu akıcı görünsün ve iptal
# isteği en geç bir parça sonra fark edilsin.
CHUNK = 256 * 1024

# Gereken en az boş alan: kurulum dosyası (~350 MB) + kurulu hâli
# (~800 MB), pay bırakılarak.
REQUIRED_SPACE = int(1.5 * 1024 * 1024 * 1024)


@dataclass(frozen=True)
class Asset:
    """Sürümün indirilebilir dosyası."""

    name: str
    url: str
    size: int


def pick_installer(assets) -> Asset | None:
    """Sürümün dosyaları arasından kurulum programını seçer.

    Adres denetimi burada: beklenen adresle başlamayan bir dosya hiç
    değerlendirilmiyor.
    """
    for ham in assets or ():
        ad = str(ham.get("name") or "")
        adres = str(ham.get("browser_download_url") or "")
        if not (ad.startswith(INSTALLER_PREFIX) and ad.endswith(INSTALLER_SUFFIX)):
            continue
        if not adres.startswith(DOWNLOAD_PREFIX):
            continue
        return Asset(name=ad, url=adres, size=int(ham.get("size") or 0))
    return None


# --- ortam denetimleri -------------------------------------------------


def install_dir() -> Path:
    """Uygulamanın çalıştığı klasör (`Odyssey.exe`'nin yanı)."""
    return app_dir()


def is_installed() -> bool:
    """Uygulama kurulum programıyla mı kurulmuş, zip'ten mi çalışıyor?

    Kurulum programı klasöre kendi kaldırıcısını (`unins000.exe`) koyuyor;
    zip'ten açılan klasörde o yok.
    """
    return any(install_dir().glob("unins*.exe"))


def free_space(path: Path) -> int:
    try:
        return shutil.disk_usage(path).free
    except OSError:
        return 0


def can_update() -> tuple[bool, str]:
    """Güncelleme buradan yapılabilir mi?

    Dönen ikinci değer, olmuyorsa sebebin anahtarı: `frozen`, `space`. Sebep
    kullanıcıya söyleniyor — sessizce elle indirmeye yönlendirmek "düğmeye
    bastım, bir şey olmadı" demek olurdu.
    """
    if not getattr(sys, "frozen", False):
        # Kaynak koddan çalışırken kurulacak bir paket yok.
        return False, "frozen"
    if free_space(updates_dir()) < REQUIRED_SPACE:
        return False, "space"
    return True, ""


# --- indirme -----------------------------------------------------------


def download(
    asset: Asset,
    target: Path,
    on_progress=None,
    is_cancelled=None,
) -> str:
    """Dosyayı indirir. Boş metin döndürürse başarılı.

    `on_progress(inen, toplam)` her parçada çağrılıyor; `is_cancelled()`
    True dönerse indirme durduruluyor ve yarım dosya siliniyor.
    """
    istek = urllib.request.Request(
        asset.url, headers={"User-Agent": USER_AGENT, "Accept": "application/octet-stream"}
    )
    target.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(istek, timeout=30) as cevap:
            toplam = int(cevap.headers.get("Content-Length") or asset.size or 0)
            inen = 0
            with target.open("wb") as dosya:
                while True:
                    if is_cancelled is not None and is_cancelled():
                        dosya.close()
                        target.unlink(missing_ok=True)
                        return "cancelled"
                    parca = cevap.read(CHUNK)
                    if not parca:
                        break
                    dosya.write(parca)
                    inen += len(parca)
                    if on_progress is not None:
                        on_progress(inen, toplam)
    except (urllib.error.URLError, TimeoutError, OSError) as hata:
        target.unlink(missing_ok=True)
        return f"network: {hata}"

    return ""


def verify_installer(path: Path, expected_size: int) -> str:
    """İnen kurulum programını denetler. Boş metin döndürürse sağlam.

    Boyut sunucunun söylediğiyle aynı olmalı (yarım inmiş dosya) ve dosya
    bir Windows programı olmalı (`MZ` imzası) — başka bir şey çalıştırılmıyor.
    """
    if not path.exists():
        return "missing"
    if expected_size and path.stat().st_size != expected_size:
        return "size"
    try:
        with path.open("rb") as dosya:
            if dosya.read(2) != b"MZ":
                return "content"
    except OSError:
        return "corrupt"
    return ""


# --- kurulum -----------------------------------------------------------


def installer_command(path: Path) -> list[str]:
    """Kurulum programını başlatacak komut."""
    komut = [str(path), *INSTALLER_ARGS, f"/OLDPID={os.getpid()}"]
    if not is_installed():
        komut.append(f"/OLDDIR={install_dir()}")
    return komut


def start_installer(path: Path) -> bool:
    """Kurulum programını sessiz kipte başlatır.

    Bu çağrıdan sonra uygulamanın kapanması gerekiyor: kurulum, dosyaların
    kilidi kalksın diye bu sürecin bitmesini bekliyor.
    """
    if not path.exists():
        return False
    try:
        subprocess.Popen(installer_command(path), cwd=str(path.parent), close_fds=True)
    except OSError:
        return False
    return True


# --- temizlik ----------------------------------------------------------


def cleanup() -> None:
    """Açılışta çağrılıyor: bir önceki güncellemeden kalan indirmeleri siler.

    Kurulum programı çalışırken kendi dosyasını silemiyor; uygulama bir
    sonraki açılışta temizliyor. Silinemeyen (hâlâ açık) dosya olduğu yerde
    kalıyor, açılış durmuyor.
    """
    try:
        girdiler = list(updates_dir().iterdir())
    except OSError:
        return
    for girdi in girdiler:
        try:
            if girdi.is_dir():
                shutil.rmtree(girdi, ignore_errors=True)
            else:
                girdi.unlink(missing_ok=True)
        except OSError:
            continue


def release_page() -> str:
    """Elle indirme adresi — güncelleme buradan yapılamadığında."""
    return RELEASES_PAGE
