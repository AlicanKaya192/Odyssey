"""Okuma ve kod yazısının o anki ölçeği; değişince açık bileşenlere iletir.

Belge, editör ve terminal kurulurken `listen` ile kayıt oluyor ve ölçeği
hemen alıyor. Kayıt zayıf: bileşen silinince listeden kendiliğinden düşüyor,
ayar penceresi her açılışta yeni dinleyici biriktirmiyor.
"""

from __future__ import annotations

import weakref
from typing import Callable

_scale = 1.0
_listeners: list[weakref.WeakMethod] = []


def scale() -> float:
    return _scale


def listen(method: Callable[[float], None]) -> None:
    """Bileşenin yöntemini kaydeder ve o anki ölçekle bir kez çağırır."""
    _listeners.append(weakref.WeakMethod(method))
    method(_scale)


def set_scale(value: float) -> None:
    global _scale
    _scale = float(value)
    for ref in list(_listeners):
        method = ref()
        try:
            if method is None:
                raise RuntimeError("sahibi silindi")
            method(_scale)
        except RuntimeError:
            # Python nesnesi duruyor ama Qt nesnesi silinmiş olabilir.
            _listeners.remove(ref)
