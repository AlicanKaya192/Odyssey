"""Güncellemeyi indiren, doğrulayan ve kuran taraf.

`updates.py` yalnızca "yeni sürüm var mı" diye soruyor; kurulumu bu modül
yapıyor.

## Akış

1. **İndir** — sürümün zip dosyası `%APPDATA%\\Odyssey\\updates` altına
   iniyor, ilerleme kullanıcıya gösteriliyor.
2. **Doğrula** — boyut, zip bütünlüğü ve içinde beklenen dosyanın olup
   olmadığı. İndirilen şey çalıştırılacak bir program; sağlamlığına
   bakmadan açılmıyor.
3. **Aç** — zip geçici klasöre açılıyor.
4. **Devret** — uygulama, **yeni açılan exe'yi** `--apply-update`
   bayrağıyla başlatıp kendini kapatıyor.
5. **Değiştir** — yeni exe, eski sürecin kapanmasını bekliyor, kurulum
   klasörünü yedek adına taşıyor, yeni dosyaları oraya kopyalıyor ve
   uygulamayı yeniden açıyor.

## Neden bu kadar dolambaçlı

Windows çalışan bir programın klasörünü **yeniden adlandırmıyor**: içindeki
exe açıkken klasöre dokunulamıyor. Yani değişimi yapan süreç ne eski
klasörün ne de taşınacak klasörün içinden çalışabiliyor.

Çözüm, işi yapanın **yeni açılmış kopya** olması ve kendi klasörünü
taşımak yerine dosyaları kurulum klasörüne **kopyalaması**. Kopyalama
taşımaktan yavaş ama kendi ayağının altındaki halıyı çekmiyor; yarıda
kesilse bile eski sürüm yedek klasörde duruyor ve geri alınıyor.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

from ..paths import app_dir, updates_dir
from .updates import RELEASES_PAGE, USER_AGENT

# Uygulamayı `--apply-update <kurulum klasörü> <eski süreç no>` biçiminde
# yardımcı kipe sokan bayrak.
APPLY_FLAG = "--apply-update"

# İndirilecek dosyanın adı bununla bitiyor: `Odyssey-0.7.1-windows-x64.zip`.
ASSET_SUFFIX = "-windows-x64.zip"

# Zip'in içindeki kök klasör ve içinde bulunması beklenen dosya.
TOP_LEVEL = "Odyssey"
EXPECTED_ENTRY = f"{TOP_LEVEL}/Odyssey.exe"

# İndirme adresi yalnızca burada başlayabilir. Sunucudan gelen bir adresi
# doğrulamadan indirmek, güncelleme akışını bir dosya indirme aracına
# çevirirdi.
DOWNLOAD_PREFIX = "https://github.com/AlicanKaya192/Odyssey/releases/download/"

# İndirme parçası. Küçük tutuldu: ilerleme çubuğu akıcı görünsün ve iptal
# isteği en geç bir parça sonra fark edilsin.
CHUNK = 256 * 1024

# Kurulum için gereken en az boş alan: zip (~280 MB) + açılmış hâli
# (~700 MB) + kopyalanan hâli (~700 MB). Cömert bir pay bırakılıyor.
REQUIRED_SPACE = 2 * 1024 * 1024 * 1024

# Eski sürümün kapanması için beklenecek en uzun süre.
EXIT_TIMEOUT_SEC = 60

# Yedeğe verilen ad. Güncelleme sonrası siliniyor; silinemezse bir sonraki
# açılışta temizleniyor.
BACKUP_SUFFIX = ".old"


@dataclass(frozen=True)
class Asset:
    """Sürümün indirilebilir dosyası."""

    name: str
    url: str
    size: int


def pick_asset(assets) -> Asset | None:
    """Sürümün dosyaları arasından Windows paketini seçer.

    Adres denetimi burada: beklenen adresle başlamayan bir dosya hiç
    değerlendirilmiyor.
    """
    for ham in assets or ():
        ad = str(ham.get("name") or "")
        adres = str(ham.get("browser_download_url") or "")
        if not ad.endswith(ASSET_SUFFIX):
            continue
        if not adres.startswith(DOWNLOAD_PREFIX):
            continue
        return Asset(name=ad, url=adres, size=int(ham.get("size") or 0))
    return None


# --- ortam denetimleri -------------------------------------------------


def install_dir() -> Path:
    """Güncellenecek klasör."""
    return app_dir()


def is_writable(path: Path) -> bool:
    """Klasöre gerçekten yazılabiliyor mu?

    `os.access` Windows'ta yanıltıcı olabiliyor; dosya açıp kapatmak
    kesin cevabı veriyor.
    """
    deneme = path / ".odyssey-write-test"
    try:
        deneme.touch()
        deneme.unlink()
        return True
    except OSError:
        return False


def free_space(path: Path) -> int:
    try:
        return shutil.disk_usage(path).free
    except OSError:
        return 0


def can_self_update() -> tuple[bool, str]:
    """Uygulama kendini güncelleyebilir mi?

    Dönen ikinci değer, olmuyorsa sebebin anahtarı: `frozen`, `writable`,
    `space`. Sebep kullanıcıya söyleniyor — sessizce elle indirmeye
    yönlendirmek "düğmeye bastım, bir şey olmadı" demek olurdu.
    """
    if not getattr(sys, "frozen", False):
        # Kaynak koddan çalışırken değiştirilecek bir paket yok.
        return False, "frozen"
    if not is_writable(install_dir()):
        return False, "writable"
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


def verify(path: Path, expected_size: int) -> str:
    """İnen dosyayı denetler. Boş metin döndürürse sağlam.

    Üç şeye bakılıyor: boyut sunucunun söylediğiyle aynı mı, zip açılıyor
    mu, ve içinde beklenen program dosyası var mı. Kontrol yapılmadan
    açılan bir arşiv, yarım inmiş bir indirmeyi kurulum diye kurardı.
    """
    if not path.exists():
        return "missing"
    if expected_size and path.stat().st_size != expected_size:
        return "size"

    try:
        with zipfile.ZipFile(path) as arsiv:
            if arsiv.testzip() is not None:
                return "corrupt"
            adlar = set(arsiv.namelist())
    except (zipfile.BadZipFile, OSError):
        return "corrupt"

    if EXPECTED_ENTRY not in adlar:
        return "content"
    return ""


def extract(path: Path, dest: Path, on_progress=None, is_cancelled=None) -> Path | None:
    """Zip'i açar ve içindeki uygulama klasörünü döndürür."""
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(path) as arsiv:
            girdiler = arsiv.infolist()
            for sira, girdi in enumerate(girdiler, start=1):
                if is_cancelled is not None and is_cancelled():
                    shutil.rmtree(dest, ignore_errors=True)
                    return None
                arsiv.extract(girdi, dest)
                if on_progress is not None:
                    on_progress(sira, len(girdiler))
    except (zipfile.BadZipFile, OSError):
        shutil.rmtree(dest, ignore_errors=True)
        return None

    acilan = dest / TOP_LEVEL
    return acilan if (acilan / "Odyssey.exe").exists() else None


# --- kurulum -----------------------------------------------------------


def start_helper(staged: Path, target: Path | None = None) -> bool:
    """Yeni sürümü yardımcı kipte başlatır.

    Bu çağrıdan sonra uygulamanın kapanması gerekiyor: yardımcı, bu
    sürecin bitmesini bekliyor.
    """
    target = target or install_dir()
    yeni_exe = staged / "Odyssey.exe"
    if not yeni_exe.exists():
        return False

    try:
        subprocess.Popen(
            [str(yeni_exe), APPLY_FLAG, str(target), str(os.getpid())],
            cwd=str(staged),
            close_fds=True,
        )
    except OSError:
        return False
    return True


def _wait_for_exit(pid: int, timeout: int = EXIT_TIMEOUT_SEC) -> bool:
    """Eski sürecin kapanmasını bekler.

    Süreç numarası hâlâ ayaktaysa dosyalar kilitli demektir; beklemeden
    değiştirmek yarım bir kurulum bırakırdı.
    """
    son = time.time() + timeout
    while time.time() < son:
        if not _process_alive(pid):
            # Dosya tanıtıcılarının kapanması bir an sürebiliyor.
            time.sleep(1.0)
            return True
        time.sleep(0.25)
    return False


def _process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    import ctypes

    SYNCHRONIZE = 0x00100000
    kernel32 = ctypes.windll.kernel32
    tutamac = kernel32.OpenProcess(SYNCHRONIZE, False, pid)
    if not tutamac:
        return False
    # 0 ms bekleme: "şu an bitmiş mi" sorusu. 0 = bitmiş.
    bitti = kernel32.WaitForSingleObject(tutamac, 0) == 0
    kernel32.CloseHandle(tutamac)
    return not bitti


def apply_update(target: Path, pid: int, on_progress=None) -> str:
    """Yardımcı kip: dosyaları değiştirir. Boş metin döndürürse başarılı.

    Sıra bilinçli: **önce eskiyi yedek adına taşı**, sonra yenisini
    kopyala. Kopyalama yarıda kalırsa yedek geri alınıyor, yani kullanıcı
    en kötü ihtimalle eski sürümüyle kalıyor — açılmayan bir klasörle
    değil.
    """
    kaynak = Path(sys.executable).resolve().parent
    target = Path(target)

    # **Önce kaynağa bak, sonra eskiye dokun.** Kaynak eksikken sıraya
    # devam etmek, eski kurulumu kenara taşıyıp yerine boş bir klasör
    # bırakıyordu: kullanıcı ne eski ne yeni sürümle kalıyordu (ölçüldü).
    if not (kaynak / "Odyssey.exe").exists():
        return "source"

    if not _wait_for_exit(pid):
        return "timeout"

    yedek = target.with_name(target.name + BACKUP_SUFFIX)
    shutil.rmtree(yedek, ignore_errors=True)

    tasindi = False
    try:
        if target.exists():
            target.rename(yedek)
            tasindi = True
    except OSError as hata:
        return f"backup: {hata}"

    try:
        _copy_tree(kaynak, target, on_progress)
        if not (target / "Odyssey.exe").exists():
            raise OSError("kopya eksik")
    except OSError as hata:
        # Geri al: yarım kopyayı sil, eskiyi yerine koy.
        shutil.rmtree(target, ignore_errors=True)
        if tasindi:
            try:
                yedek.rename(target)
            except OSError:
                return f"restore-failed: {hata}"
        return f"copy: {hata}"

    shutil.rmtree(yedek, ignore_errors=True)
    return ""


def _copy_tree(kaynak: Path, hedef: Path, on_progress=None) -> None:
    """Klasörü dosya dosya kopyalar ve ilerlemeyi bildirir.

    `shutil.copytree` tek çağrıda hallediyor ama ilerleme vermiyor;
    700 MB'lık bir kopyada kullanıcının donmuş bir pencereye bakması
    demek olurdu.
    """
    dosyalar = [p for p in kaynak.rglob("*") if p.is_file()]
    if not dosyalar:
        # Boş bir kopya "başarılı" sayılmamalı.
        raise OSError(f"kaynak boş: {kaynak}")
    hedef.mkdir(parents=True, exist_ok=True)

    for sira, dosya in enumerate(dosyalar, start=1):
        goreli = dosya.relative_to(kaynak)
        varis = hedef / goreli
        varis.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dosya, varis)
        if on_progress is not None:
            on_progress(sira, len(dosyalar))


def relaunch(target: Path) -> bool:
    """Güncellenmiş uygulamayı açar."""
    exe = Path(target) / "Odyssey.exe"
    if not exe.exists():
        return False
    try:
        subprocess.Popen([str(exe)], cwd=str(target), close_fds=True)
    except OSError:
        return False
    return True


# --- temizlik ----------------------------------------------------------


def cleanup(target: Path | None = None) -> None:
    """Açılışta çağrılıyor: yedekleri ve indirilmiş dosyaları siler.

    Güncellemeden sonra yardımcı kendi klasörünü silemiyor (o an oradan
    çalışıyor). Bir sonraki açılışta uygulama kendi kurulum klasöründen
    çalışıyor ve burayı temizleyebiliyor.
    """
    target = target or install_dir()
    shutil.rmtree(target.with_name(target.name + BACKUP_SUFFIX), ignore_errors=True)

    try:
        for girdi in updates_dir().iterdir():
            if girdi.is_dir():
                shutil.rmtree(girdi, ignore_errors=True)
            else:
                girdi.unlink(missing_ok=True)
    except OSError:
        # Temizlik hiçbir zaman açılışı durdurmuyor.
        pass


def release_page() -> str:
    """Elle indirme adresi — kendi kendine güncelleme yapılamadığında."""
    return RELEASES_PAGE
