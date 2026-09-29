"""Açılış animasyonunu ayrı bir süreçte başlatır ve onunla konuşur.

Animasyon neden ayrı süreçte: ana pencere kurulurken arayüz iş parçacığı
saniyelerce kilitli (bkz. `app/ui/intro.py`). Program kendini `--intro`
bayrağıyla bir kez daha başlatıyor; o süreç yalnızca çiziyor.

Akış:
  1. `launch()` en başta, Qt kurulmadan önce çağrılıyor: iki süreç aynı anda
     açılıyor, animasyon ana pencereyi beklemeden başlıyor.
  2. Ana pencere hazır olunca `reveal(window)`: `ready` gönderiliyor ve
     animasyonun `reveal` demesi bekleniyor (hedefin merkezi ekranı
     kapladığı an). Pencere o an beliriyor, animasyon penceresi üstünde
     sönüyor.
  3. Animasyon hiç görünmediyse, çöktüyse ya da cevap vermiyorsa pencere
     beklemeden gösteriliyor. Açılış hiçbir koşulda animasyona takılmıyor.

Ana süreç kapanınca borunun öbür ucu kapanıyor ve animasyon da kapanıyor.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

INTRO_FLAG = "--intro"

# Animasyon `shown` demezse bu kadar beklenip vazgeçiliyor (süreç açılamadı).
SHOWN_TIMEOUT_S = 4.0
# `ready`'den sonra geçişin gelmesi için en uzun süre. Animasyonun kendisi
# en fazla ~5 sn; bunun ötesi bir takılmadır.
REVEAL_TIMEOUT_S = 9.0
FADE_IN_MS = 220


class IntroLink:
    """Animasyon sürecinin tutamağı."""

    def __init__(self, process: subprocess.Popen) -> None:
        self._process = process
        self._started = time.monotonic()
        self._shown = threading.Event()
        self._reveal = threading.Event()
        self._ended = threading.Event()
        threading.Thread(target=self._read, daemon=True).start()

    @classmethod
    def launch(cls, theme: str, language: str, sound: bool = False) -> IntroLink | None:
        """Animasyonu başlatır; başlatılamazsa None (eski açılış ekranı kullanılır)."""
        payload = json.dumps({"theme": theme, "lang": language, "pid": os.getpid(), "sound": sound})
        if getattr(sys, "frozen", False):
            command = [sys.executable, INTRO_FLAG, payload]
        else:
            command = [sys.executable, str(Path(sys.argv[0]).resolve()), INTRO_FLAG, payload]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        try:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                creationflags=flags,
            )
        except OSError:
            return None
        return cls(process)

    def _read(self) -> None:
        stream = self._process.stdout
        try:
            for raw in stream:
                line = raw.decode("utf-8", "replace").strip()
                if line == "shown":
                    self._shown.set()
                elif line == "reveal":
                    self._reveal.set()
        except (OSError, ValueError):
            pass
        self._ended.set()
        self._reveal.set()  # süreç bitti: beklemenin anlamı yok

    def _send(self, message: str) -> None:
        try:
            self._process.stdin.write((message + "\n").encode())
            self._process.stdin.flush()
        except (OSError, ValueError):
            self._reveal.set()

    def reveal(self, window) -> None:
        """Pencere hazır: animasyonun sonunu bekler, sonra pencereyi gösterir.

        Beklerken olay döngüsü dönüyor (pencerenin belge alanları ısınmaya
        devam ediyor); ama akış burada duruyor, beta uyarısı gibi pencereler
        animasyon bitmeden açılmıyor.
        """
        from PySide6.QtCore import QEventLoop, QTimer

        self._send("ready")
        ready_at = time.monotonic()
        loop = QEventLoop()

        def check() -> None:
            now = time.monotonic()
            if self._reveal.is_set():
                loop.quit()
            elif not self._shown.is_set() and now - self._started > SHOWN_TIMEOUT_S:
                loop.quit()  # animasyon hiç görünmedi
            elif now - ready_at > REVEAL_TIMEOUT_S:
                loop.quit()

        timer = QTimer()
        timer.setInterval(10)
        timer.timeout.connect(check)
        timer.start()
        check()
        if not self._reveal.is_set():
            loop.exec()
        timer.stop()

        if not self._shown.is_set():
            self.stop()
        show_window(window, fade_ms=FADE_IN_MS if self._shown.is_set() else 0)

    def stop(self) -> None:
        try:
            self._process.stdin.close()
        except OSError:
            pass
        try:
            self._process.terminate()
        except OSError:
            pass


def show_window(window, fade_ms: int = 0) -> None:
    """Görünmez açılmış ana pencereyi görünür yapar (isteğe bağlı solarak)."""
    window.show()
    window.raise_()
    window.activateWindow()
    if fade_ms <= 0:
        window.setWindowOpacity(1.0)
        return
    from PySide6.QtCore import QAbstractAnimation, QEasingCurve, QVariantAnimation

    anim = QVariantAnimation(window)
    anim.setDuration(fade_ms)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    anim.valueChanged.connect(window.setWindowOpacity)
    anim.finished.connect(lambda: window.setWindowOpacity(1.0))
    anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
