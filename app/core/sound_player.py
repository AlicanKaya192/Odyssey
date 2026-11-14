"""Bir `.wav` dosyasını arka planda çalan küçük yardımcı (Windows ve macOS).

- **Windows:** sistemin `winsound` modülü (`SND_ASYNC`); ek kütüphane yok.
- **macOS:** sistemle gelen `afplay` komutu ayrı bir süreçte. Qt'nin ses
  modülü pakete girmiyor; `afplay` her macOS'ta `/usr/bin` altında duruyor.

İki sistemde de davranış aynı: yeni ses başlayınca çalan ses kesiliyor
(`winsound` bunu kendisi yapıyor, Mac'te önceki `afplay` süreci
sonlandırılıyor). Yalnızca bu nesnenin kendi başlattığı süreç
sonlandırılır; adla süreç aranmaz.

Hata (aygıt yok, komut açılamadı) `OSError` / `RuntimeError` olarak
çağırana gidiyor; çağıran sesi sessizce atlıyor.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

AFPLAY = "/usr/bin/afplay"


def _afplay_exists() -> bool:
    return Path(AFPLAY).exists()


def supported() -> bool:
    """Bu sistemde ses çalınabiliyor mu?"""
    if sys.platform == "win32":
        return True
    return sys.platform == "darwin" and _afplay_exists()


class SoundPlayer:
    """Tek sesi çalan nesne; Mac'te çalan `afplay` sürecini tutuyor."""

    def __init__(self) -> None:
        self._process: subprocess.Popen | None = None

    def play(self, path: Path) -> bool:
        """Sesi arka planda başlatır; başlattıysa True."""
        if sys.platform == "win32":
            import winsound

            winsound.PlaySound(
                str(path),
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
            )
            return True
        if sys.platform == "darwin" and _afplay_exists():
            self.stop()
            self._process = subprocess.Popen(
                [AFPLAY, str(path)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        return False

    def stop(self) -> None:
        """Çalan sesi susturur."""
        if sys.platform == "win32":
            import winsound

            winsound.PlaySound(None, winsound.SND_PURGE)
            return
        process, self._process = self._process, None
        if process is not None and process.poll() is None:
            process.terminate()
