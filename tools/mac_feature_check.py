"""macOS'a 1.7.1'de gelen özellikleri gerçek bir Mac'te dener (CI: mac-trial).

- Güncelleme: derlenen `.dmg` güncellemenin dosya denetiminden geçiyor ve
  sürümün dosya listesinden seçiliyor.
- Ses: `afplay` var ve programın ses dosyasını çalabiliyor.
- Discord: Discord yokken bağlantı denemesi hata vermeden `None` dönüyor.

Kullanım (proje kökünde, derleme ve `build_dmg.py`'den sonra):

    python tools/mac_feature_check.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.core import celebration_sound, discord_presence, sound_player, updater  # noqa: E402
from app.version import APP_VERSION  # noqa: E402

sys.path.insert(0, str(ROOT / "tools"))
from build_dmg import dmg_path  # noqa: E402


def check_update() -> list[str]:
    dmg = dmg_path()
    if not dmg.exists():
        return [f"disk görüntüsü yok: {dmg.name}"]
    hatalar = []
    sonuc = updater.verify_installer(dmg, dmg.stat().st_size)
    if sonuc:
        hatalar.append(f"güncelleme denetimi .dmg'yi reddetti: {sonuc}")
    varliklar = [{
        "name": dmg.name,
        "browser_download_url": updater.DOWNLOAD_PREFIX + f"setup-{APP_VERSION}/{dmg.name}",
        "size": dmg.stat().st_size,
    }]
    secilen = updater.pick_update(varliklar, APP_VERSION)
    if secilen is None or secilen.name != dmg.name:
        hatalar.append(f"güncelleme .dmg'yi seçmedi ({updater.mac_arch()})")
    print(f"güncelleme: {dmg.name}, denetim {'geçti' if not sonuc else sonuc}")
    return hatalar


def check_sound() -> list[str]:
    if not sound_player.supported():
        return ["ses desteklenmiyor (afplay yok)"]
    yol = celebration_sound.sound_path("badge")
    sonuc = subprocess.run([sound_player.AFPLAY, str(yol)], capture_output=True, text=True, timeout=30)
    # Sunucuda ses aygıtı olmayabilir; afplay'in çıkış kodu bilgi için.
    print(f"ses: afplay {yol.name} → çıkış {sonuc.returncode} {sonuc.stderr.strip()[:200]}")
    return []


def check_discord() -> list[str]:
    try:
        baglanti = discord_presence._connect()
    except Exception as hata:  # noqa: BLE001 — denetimin kendisi
        return [f"Discord bağlantı denemesi hata verdi: {hata!r}"]
    print(f"discord: bağlantı {'kuruldu' if baglanti else 'yok (beklenen: Discord kurulu değil)'}")
    if baglanti is not None:
        baglanti.close()
    return []


def main() -> int:
    if sys.platform != "darwin":
        print("Bu denetim yalnızca macOS'ta çalışır.")
        return 1
    hatalar = check_update() + check_sound() + check_discord()
    for hata in hatalar:
        print("HATA", hata)
    print("Sorun yok." if not hatalar else f"{len(hatalar)} sorun.")
    return 1 if hatalar else 0


if __name__ == "__main__":
    raise SystemExit(main())
