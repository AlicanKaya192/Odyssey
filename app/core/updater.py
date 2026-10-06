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
from . import log
from .updates import USER_AGENT

_log = log.get(__name__)

# Windows'un "bu dosyayı ben başlatmadım" hataları. 4551: uygulama denetimi
# ilkesi (Akıllı Uygulama Denetimi; 0.9.1'de imzasız kurulumu böyle engelledi,
# ölçüldü), 1260: grup ilkesi / AppLocker, 225-226: virüs koruması.
BLOCKED_ERRORS = {4551, 1260, 225, 226}

# Kurulum dosyası: `Odyssey-0.8.3-setup.exe`.
INSTALLER_PREFIX = "Odyssey-"
INSTALLER_SUFFIX = "-setup.exe"

# Kurulum programına verilen parametreler. Adlar kurulum betiğiyle
# (`installer/odyssey.iss`, `{param:OLDDIR}` / `{param:OLDPID}`) aynı.
#
# - `/VERYSILENT`: soru sormadan ve **hiç pencere açmadan** kurar. 0.8.3'e
#   kadar `/SILENT` vardı: kurulumun kendi ilerleme penceresi açılıyor ve
#   eski sürecin kapanmasını beklerken donuk duruyordu (GitHub #15). Artık
#   hikâyeyi uygulama anlatıyor: güncelleme penceresinde ok hedefe saplanıyor,
#   yeni sürüm açılış animasyonuyla açılıyor.
# - `/SUPPRESSMSGBOXES /NORESTART /SP-`: hiçbir kutu, yeniden başlatma ya da
#   "kurmak istiyor musunuz" sorusu yok.
# - `/OLDPID`: kapanması beklenen bu süreç; dosyaları kilitli tutuyor.
# - `/OLDDIR`: yalnızca uygulama **zip'ten** çalışıyorsa (kurulu değilse)
#   gönderiliyor. Kurulum bittikten sonra o klasördeki `Odyssey.exe` ve
#   `_internal` siliniyor. Kurulu bir uygulama bunu göndermiyor: kendi
#   klasörünü göndermesi kurulumun yeni yazdığı dosyaları silmeye kalkması
#   olurdu (betik ayrıca yolları karşılaştırıyor).
INSTALLER_ARGS = ("/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-")

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


# Fark kurulumu (0.9.1'den itibaren): `Odyssey-<yeni>-patch-<eski>.exe`,
# yalnızca <eski> sürümün değişen dosyaları (`tools/build_installer.py`).
# Eski sürümler bu adı tanımıyor (`-setup.exe` ile bitmiyor), tam kurulumu
# almaya devam ediyorlar.
PATCH_NAME = "Odyssey-{new}-patch-{base}.exe"

# Denenmiş fark kurulumunun kaydı (veri klasöründe, güncellemeler klasörü
# her açılışta temizlendiği için orada değil). Yama başarısız olursa
# (kurulu sürüm beklenen değilse kurulum hiçbir şeye dokunmadan çıkıyor)
# program eski sürümüyle yeniden açılıyor; bir sonraki denemede aynı yama
# yerine tam kurulum iniyor, döngüye girilmiyor.
PATCH_ATTEMPT_FILE = "patch-attempt.txt"


def _patch_attempt_path() -> Path:
    return updates_dir().parent / PATCH_ATTEMPT_FILE


def mark_patch_attempt(version: str) -> None:
    """Bu sürümün yaması başlatılıyor."""
    try:
        _patch_attempt_path().write_text(version, encoding="utf-8")
    except OSError:
        pass


def patch_failed_before(version: str) -> bool:
    """Bu sürümün yaması daha önce denendi ve program hâlâ eski sürümde mi?"""
    from ..version import APP_VERSION

    try:
        denenen = _patch_attempt_path().read_text(encoding="utf-8").strip()
    except OSError:
        return False
    return denenen == version and APP_VERSION != version


def pick_patch(assets, version: str, base: str | None = None) -> Asset | None:
    """Bu sürümden (`base`, varsayılan çalışan sürüm) `version`'a fark kurulumu."""
    from ..version import APP_VERSION

    ad_beklenen = PATCH_NAME.format(new=version, base=base or APP_VERSION)
    for ham in assets or ():
        ad = str(ham.get("name") or "")
        adres = str(ham.get("browser_download_url") or "")
        if ad == ad_beklenen and adres.startswith(DOWNLOAD_PREFIX):
            return Asset(name=ad, url=adres, size=int(ham.get("size") or 0))
    return None


def pick_update(assets, version: str) -> Asset | None:
    """İndirilecek dosya: bu sürümün yaması varsa o, yoksa tam kurulum.

    Yama bir kez denenip tutmadıysa (`patch_failed_before`) tam kurulum.
    """
    if not patch_failed_before(version):
        yama = pick_patch(assets, version)
        if yama is not None:
            return yama
    return pick_installer(assets)


def is_patch(asset: Asset | None) -> bool:
    return asset is not None and "-patch-" in asset.name


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


# Son başlatılan kurulum sürecinin kimliği: "Odyssey güncelleniyor"
# penceresi (`install_bridge`) onun bitişini bekliyor.
last_installer_pid = 0


def start_installer(path: Path) -> str:
    """Kurulum programını sessiz kipte başlatır; başlamadıysa sebebini döndürür.

    Dönüş: "" başladı, "blocked" Windows engelledi (`BLOCKED_ERRORS`),
    "start" başka bir sebeple başlamadı. Başladıysa uygulamanın kapanması
    gerekiyor: kurulum, dosyaların kilidi kalksın diye bu sürecin bitmesini
    bekliyor.
    """
    if not path.exists():
        _log.error("Kurulum dosyası yok: %s", path.name)
        return "start"
    if "-patch-" in path.name:
        # `Odyssey-<yeni>-patch-<eski>.exe`: tutmazsa bir dahaki sefere tam kurulum.
        mark_patch_attempt(path.name.split("-")[1])
    global last_installer_pid
    try:
        surec = subprocess.Popen(installer_command(path), cwd=str(path.parent), close_fds=True)
        last_installer_pid = surec.pid
    except OSError as hata:
        kod = getattr(hata, "winerror", None)
        _log.error("Kurulum başlatılamadı: %s (winerror %s)", path.name, kod, exc_info=True)
        return "blocked" if kod in BLOCKED_ERRORS else "start"
    _log.info("Kurulum başlatıldı: %s", path.name)
    return ""


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
