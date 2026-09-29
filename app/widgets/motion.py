"""Animasyon yardımcıları.

Arayüzdeki bütün hareket buradan başlar; ekranlar kendi `QPropertyAnimation`
kurgusunu yazmaz. Üç sebebi var:

1. **Ayar tek yerde.** "Animasyonlar" kapalıyken (`set_enabled(False)`)
   hiçbir şey hareket etmez: değer doğrudan son hâline yazılır ve bitiş
   geri çağrısı hemen çalışır. Her ekranın ayarı ayrı ayrı okuması yok.
2. **Yay eğrileri.** Qt'nin eğrileri yay vermiyor; burada animasyon
   doğrusal koşuyor ve ilerleme `theme.motion.EASING` içinden geçiriliyor.
3. **Aynı değere yeni animasyon eskisini durdurur.** Qt aynı özellikte yeni
   animasyon başlayınca eskisini durduruyor; eski bir gruptaysa grubun
   geri kalanı da duruyordu (kutlama kartında kart yerine gidip saydam
   kalmıştı). Burada her (sahip, anahtar) çiftinin tek animasyonu var ve
   grup kullanılmıyor.
"""

from __future__ import annotations

from typing import Any, Callable

from PySide6.QtCore import (
    QAbstractAnimation,
    QObject,
    QPoint,
    QPointF,
    QRectF,
    QTimer,
    QVariantAnimation,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel

from ..resources.theme.motion import DURATION, EASING

_enabled = True
_listeners: list[Callable[[bool], None]] = []


def enabled() -> bool:
    """Animasyonlar açık mı (Ayarlar › Görünüm › Animasyonlar)."""
    return _enabled


def set_enabled(value: bool) -> None:
    global _enabled
    value = bool(value)
    if value == _enabled:
        return
    _enabled = value
    for dinleyici in list(_listeners):
        try:
            dinleyici(value)
        except RuntimeError:
            # Sahibi silinmiş (C++ nesnesi yok); listeden düşür.
            if dinleyici in _listeners:
                _listeners.remove(dinleyici)


def on_enabled_changed(callback: Callable[[bool], None], owner: QObject | None = None) -> None:
    """Döngüsel animasyonu olan widget'lar ayar değişince durmak için dinler.

    `owner` verilirse o nesne silinince dinleyici de listeden çıkar; yoksa
    silinmiş bir widget'a çağrı gidip program çöküyordu (yol testinde oldu).
    """
    _listeners.append(callback)
    if owner is not None:
        owner.destroyed.connect(lambda *_: callback in _listeners and _listeners.remove(callback))


def duration(name: str | int) -> int:
    return name if isinstance(name, int) else DURATION[name]


def _lerp(a: Any, b: Any, k: float) -> Any:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + (b - a) * k
    if isinstance(a, QPointF):
        return QPointF(a.x() + (b.x() - a.x()) * k, a.y() + (b.y() - a.y()) * k)
    if isinstance(a, QPoint):
        return QPoint(round(a.x() + (b.x() - a.x()) * k), round(a.y() + (b.y() - a.y()) * k))
    if isinstance(a, QRectF):
        return QRectF(_lerp(a.x(), b.x(), k), _lerp(a.y(), b.y(), k),
                      _lerp(a.width(), b.width(), k), _lerp(a.height(), b.height(), k))
    if isinstance(a, QColor):
        c = max(0.0, min(1.0, k))
        return QColor(round(a.red() + (b.red() - a.red()) * c), round(a.green() + (b.green() - a.green()) * c),
                      round(a.blue() + (b.blue() - a.blue()) * c), round(a.alpha() + (b.alpha() - a.alpha()) * c))
    if isinstance(a, tuple):
        return tuple(_lerp(x, y, k) for x, y in zip(a, b))
    return b if k >= 1 else a


class Tween(QVariantAnimation):
    """0 → 1 doğrusal koşan, değeri eğriden geçirip `setter`'a veren animasyon."""

    def __init__(self, owner: QObject, start: Any, end: Any, setter: Callable[[Any], None],
                 ms: int, easing: str) -> None:
        super().__init__(owner)
        self._start, self._end, self._setter = start, end, setter
        self._ease = EASING[easing]
        self.setStartValue(0.0)
        self.setEndValue(1.0)
        self.setDuration(max(1, ms))
        self.valueChanged.connect(self._step)

    def _step(self, t: float) -> None:
        self._setter(_lerp(self._start, self._end, self._ease(float(t))))

    @property
    def end(self) -> Any:
        return self._end


def _registry(owner: QObject) -> dict:
    kayit = getattr(owner, "_motion_tweens", None)
    if kayit is None:
        kayit = {}
        owner._motion_tweens = kayit  # noqa: SLF001 (PySide nesnesine Python özniteliği)
    return kayit


def stop(owner: QObject, key: str) -> None:
    """Sahibin o anahtardaki animasyonunu durdurur (değer olduğu yerde kalır)."""
    eski = _registry(owner).pop(key, None)
    if eski is not None:
        eski.stop()
        eski.deleteLater()


def running(owner: QObject, key: str) -> bool:
    t = _registry(owner).get(key)
    return t is not None and t.state() == QAbstractAnimation.State.Running


def animate(
    owner: QObject,
    key: str,
    start: Any,
    end: Any,
    setter: Callable[[Any], None],
    duration_name: str | int = "base",
    easing: str = "out",
    delay: int = 0,
    on_done: Callable[[], None] | None = None,
) -> Tween | None:
    """`start`'tan `end`'e bir değeri canlandırır.

    Animasyonlar kapalıysa `setter(end)` hemen çağrılır. Aynı (sahip, anahtar)
    için çalışan bir animasyon varsa önce o durdurulur.
    """
    stop(owner, key)
    if not _enabled:
        setter(end)
        if on_done:
            on_done()
        return None

    tween = Tween(owner, start, end, setter, duration(duration_name), easing)
    _registry(owner)[key] = tween

    def bitti() -> None:
        if _registry(owner).get(key) is tween:
            _registry(owner).pop(key, None)
        setter(end)
        if on_done:
            on_done()
        try:
            tween.deleteLater()
        except RuntimeError:
            pass  # `on_done` sahibini silmiş olabilir

    tween.finished.connect(bitti)
    if delay > 0:
        setter(start)
        def gecikmeli() -> None:
            # Beklerken durdurulup silinmiş olabilir (yerine yenisi başladı).
            if _registry(owner).get(key) is not tween:
                return
            try:
                if tween.state() == QAbstractAnimation.State.Stopped:
                    tween.start()
            except RuntimeError:
                pass

        QTimer.singleShot(delay, owner, gecikmeli)
    else:
        tween.start()
    return tween


def animate_property(
    obj: QObject,
    prop: str,
    end: Any,
    duration_name: str | int = "base",
    easing: str = "out",
    start: Any = None,
    delay: int = 0,
    on_done: Callable[[], None] | None = None,
) -> Tween | None:
    """Bir Qt özelliğini (`Property`) canlandırır."""
    baslangic = obj.property(prop) if start is None else start
    return animate(obj, "prop:" + prop, baslangic, end, lambda v: obj.setProperty(prop, v),
                   duration_name, easing, delay, on_done)


def count_up(label: QLabel, old: float, new: float, fmt: Callable[[float], str] = lambda v: str(round(v))) -> None:
    """Etiketteki sayıyı eskiden yeniye sayar; değişmediyse sayma yok."""
    if old == new or not _enabled:
        label.setText(fmt(new))
        return
    animate(label, "count", float(old), float(new), lambda v: label.setText(fmt(v)), "count", "out")
