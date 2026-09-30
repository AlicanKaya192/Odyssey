"""Çalışma zamanlayıcısı: düzenler ve sayaç.

Kişi bir düzen seçip başlatıyor (Pomodoro, 52/17, derin çalışma, kısa
adımlar ya da kendi süreleri); sayaç odak ve mola evreleri arasında
ilerliyor. Arayüz `app/widgets/study_timer_ui.py`, bağlantı ana pencerede.

Süre **monoton saatten** hesaplanıyor, saniyede bir gelen tıktan değil:
olay döngüsü bir an takılsa da (ağır bir sayfa çizilirken) sayaç kaymıyor.

Tamamlanan odak evresi kaydediliyor (`focus_sessions`), etkinlik takvimine
bir olay düşüyor ve o gün çalışma günü sayılıyor (seri). Yarıda bitirilen
odak da, en az `STUDY_MINUTES` sürdüyse, geçen dakikalarıyla kaydediliyor.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

from PySide6.QtCore import QObject, QTimer, Signal

PRESET_KEY = "timer_preset"
CUSTOM_WORK_KEY = "timer_work"
CUSTOM_BREAK_KEY = "timer_break"

# Yarıda bırakılan odak bu kadar sürdüyse kaydediliyor ve gün çalışma günü
# sayılıyor (bölümde 2 dakika kalmakla aynı ölçü, `topic_view.STUDY_SECONDS`).
STUDY_MINUTES = 2
# Son kaç saniyede sayaç hafifçe büyüyor.
FINAL_SECONDS = 10

CUSTOM_WORK_CHOICES = (10, 15, 20, 25, 30, 40, 45, 50, 60, 75, 90, 120)
CUSTOM_BREAK_CHOICES = (0, 3, 5, 10, 15, 20, 30)


@dataclass(frozen=True)
class Preset:
    id: str
    work: int                 # dakika
    rest: int                 # dakika; 0 → mola yok
    long_rest: int = 0        # uzun mola (dakika); 0 → yok
    long_every: int = 0       # kaç odakta bir uzun mola


PRESETS = (
    Preset("pomodoro", 25, 5, long_rest=15, long_every=4),
    Preset("flow", 52, 17),
    Preset("deep", 90, 20),
    Preset("short", 15, 3),
)
DEFAULT_PRESET = "pomodoro"


def preset(store, preset_id: str | None = None) -> Preset:
    """Seçili (ya da verilen) düzen; kendi düzeni ayarlardan kuruluyor."""
    kimlik = preset_id or store.setting(PRESET_KEY, DEFAULT_PRESET)
    if kimlik == "custom":
        def oku(anahtar, varsayilan, secenekler):
            try:
                deger = int(store.setting(anahtar, str(varsayilan)))
            except ValueError:
                deger = varsayilan
            return deger if deger in secenekler else varsayilan
        return Preset("custom", oku(CUSTOM_WORK_KEY, 30, CUSTOM_WORK_CHOICES),
                      oku(CUSTOM_BREAK_KEY, 5, CUSTOM_BREAK_CHOICES))
    return next((p for p in PRESETS if p.id == kimlik), PRESETS[0])


def format_clock(seconds: float) -> str:
    """Kalan süre: 24:05, bir saati geçince 1:24:05."""
    kalan = max(0, int(seconds + 0.999))
    saat, kalan = divmod(kalan, 3600)
    dakika, saniye = divmod(kalan, 60)
    return f"{saat}:{dakika:02d}:{saniye:02d}" if saat else f"{dakika:02d}:{saniye:02d}"


class StudyTimer(QObject):
    """Sayaç. Durum: `idle` (kurulmamış), `focus`, `break`, `ready`
    (mola bitti, sıradaki odak bekliyor); her biri duraklatılabilir."""

    changed = Signal()              # durum ya da kalan süre değişti
    phase_finished = Signal(str)    # biten evre: "focus" | "break"

    def __init__(self, store, clock=time.monotonic, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._store = store
        self._clock = clock
        self.preset = preset(store)
        self.phase = "idle"
        self.paused = False
        self.round = 0              # tamamlanmış + süren odak sayısı
        self._length = 0.0          # evrenin toplam saniyesi
        self._ends_at = 0.0         # çalışırken bitiş anı
        self._left_when_paused = 0.0
        self._tick = QTimer(self)
        self._tick.setInterval(250)
        self._tick.timeout.connect(self._on_tick)

    # --- okuma ---------------------------------------------------------------

    @property
    def running(self) -> bool:
        return self.phase in ("focus", "break")

    @property
    def remaining(self) -> float:
        if not self.running:
            return 0.0
        if self.paused:
            return self._left_when_paused
        return max(0.0, self._ends_at - self._clock())

    @property
    def length(self) -> float:
        return self._length

    @property
    def ratio(self) -> float:
        """Evrenin geçen kısmı (0–1)."""
        if not self.running or not self._length:
            return 0.0
        return min(1.0, 1.0 - self.remaining / self._length)

    @property
    def is_long_break(self) -> bool:
        p = self.preset
        return bool(p.long_every and p.long_rest and self.round and self.round % p.long_every == 0)

    # --- komutlar ------------------------------------------------------------

    def choose(self, preset_id: str) -> None:
        """Düzeni seçer ve saklar; çalışan sayaç varsa dokunulmuyor."""
        self._store.set_setting(PRESET_KEY, preset_id)
        if not self.running:
            self.preset = preset(self._store, preset_id)
            self.changed.emit()

    def set_custom(self, work: int, rest: int) -> None:
        self._store.set_setting(CUSTOM_WORK_KEY, str(work))
        self._store.set_setting(CUSTOM_BREAK_KEY, str(rest))
        if not self.running and self.preset.id == "custom":
            self.preset = preset(self._store, "custom")
            self.changed.emit()

    def start(self) -> None:
        """Yeni bir odak başlatır (boşta ya da mola bittikten sonra)."""
        if self.phase == "idle":
            self.preset = preset(self._store)
            self.round = 0
        self.round += 1
        self._begin("focus", self.preset.work * 60)

    def pause(self) -> None:
        if self.running and not self.paused:
            self._left_when_paused = self.remaining
            self.paused = True
            self._tick.stop()
            self.changed.emit()

    def resume(self) -> None:
        if self.running and self.paused:
            self._ends_at = self._clock() + self._left_when_paused
            self.paused = False
            self._tick.start()
            self.changed.emit()

    def skip_break(self) -> None:
        """Molayı atlayıp hemen sıradaki odağa geçer."""
        if self.phase in ("break", "ready"):
            self.round += 1
            self._begin("focus", self.preset.work * 60)

    def stop(self) -> None:
        """Sayacı bitirir. Süren odak en az `STUDY_MINUTES` sürdüyse
        geçen dakikalarıyla kaydediliyor."""
        if self.phase == "focus":
            gecen = (self._length - self.remaining) / 60
            if gecen >= STUDY_MINUTES:
                self._record(int(gecen))
        self.phase = "idle"
        self.paused = False
        self.round = 0
        self._tick.stop()
        self.changed.emit()

    # --- iç --------------------------------------------------------------------

    def _begin(self, phase: str, seconds: float) -> None:
        self.phase = phase
        self.paused = False
        self._length = float(seconds)
        self._ends_at = self._clock() + self._length
        self._tick.start()
        self.changed.emit()

    def _on_tick(self) -> None:
        if not self.running or self.paused:
            return
        if self.remaining > 0:
            self.changed.emit()
            return
        biten = self.phase
        if biten == "focus":
            self._record(self.preset.work)
            mola = self.preset.long_rest if self.is_long_break else self.preset.rest
            if mola:
                self._begin("break", mola * 60)
            else:
                self._tick.stop()
                self.phase = "ready"
                self.changed.emit()
        else:
            self._tick.stop()
            self.phase = "ready"
            self.changed.emit()
        self.phase_finished.emit(biten)

    def _record(self, minutes: int) -> None:
        if minutes <= 0:
            return
        self._store.add_focus_session(minutes)
        self._store.record_activity("focus", ref_id=str(minutes))
        self._store.mark_study_day()
