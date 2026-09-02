"""Güncelleme denetimini arka planda çalıştıran iş parçacığı.

Denetim ağa çıkıyor ve ağ, açılışın en yavaş parçası olabiliyor: DNS
çözülmezse zaman aşımı doluyor. Bu yüzden arayüzde değil, ayrı bir iş
parçacığında yapılıyor — kullanıcı denetimin yapıldığını fark etmiyor.

Sonuç `finished_with` sinyaliyle geliyor; sinyal arayüz iş parçacığında
işleniyor, yani alan taraf widget'lara dokunabiliyor.

**Bu iş parçacığı veritabanına dokunmuyor.** `sqlite3` bağlantısı kendisini
kuran iş parçacığına bağlı; buradan okumak "SQLite objects created in a
thread can only be used in that same thread" hatası veriyor ve denetim
sessizce hiç çalışmıyordu (ölçüldü). Ayara bakmak ve sonucu kaydetmek
çağıran tarafta — `updates.should_check` ve `updates.record`.
"""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from ..core import updates
from ..core.updates import UpdateInfo


class UpdateWorker(QThread):
    """Tek bir denetim yapıp sonucu bildiriyor."""

    finished_with = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def run(self) -> None:  # noqa: D102
        try:
            sonuc = updates.fetch_latest()
        except Exception as hata:  # noqa: BLE001
            # Denetim hiçbir koşulda uygulamayı düşürmemeli: burası
            # kullanıcının istemediği, arka planda yapılan bir iş.
            sonuc = UpdateInfo(status="error", detail=repr(hata))
        self.finished_with.emit(sonuc)
