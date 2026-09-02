"""Kip pencerelerin ortak davranışı: sabit boyut, ortada, taşınmaz.

Ayarlar ve profil düzenleme pencereleri uygulamanın **içinde** bir işi
bitirmek için açılıyor; ayrı birer pencere gibi davranmaları gerekmiyor.
Sürüklenebildiklerinde ve boyutlandırılabildiklerinde ekranın bir köşesine
kaçıyor, arkadaki kartlarla karışıyorlardı.

Bu yüzden çerçeve kaldırılıyor (`FramelessWindowHint`): taşıma kolu ve
kenar tutamakları Windows'un başlık çubuğunda duruyor, çubuk olmayınca
ikisi de olmuyor. Elle "taşındıysa geri koy" yazmaya gerek kalmıyor.

Ana pencerede çubuk **duruyor** — orada sürükleme, Snap düzenleri ve
sistem menüsü gerçekten gerekiyor (`app/ui/titlebar.py`).
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QDialog, QWidget

# Arka planın karartma oranı. Daha koyusu uygulamayı kapatılmış gibi
# gösteriyor, daha açığı pencerenin öne çıktığını anlatmıyor.
DIM_ALPHA = 120


class Backdrop(QWidget):
    """Pencere açıkken arkayı karartan katman."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setGeometry(parent.rect())
        self.raise_()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, DIM_ALPHA))
        painter.end()


def prepare(dialog: QDialog) -> None:
    """Pencereyi kip, çerçevesiz ve taşınmaz yapar.

    `__init__` içinde, düzen kurulmadan **önce** çağrılıyor.
    """
    dialog.setModal(True)
    dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
    # Çerçeve gitti; pencerenin nerede bittiğini kenarlık söylüyor.
    dialog.setProperty("role", "modal")


def freeze(dialog: QDialog) -> None:
    """Boyutu içeriğine kilitler.

    Düzen kurulduktan sonra, `__init__` sonunda çağrılıyor. `adjustSize`
    önce çağrılmazsa pencere kendini kurulmamış hâlinin ölçüsüne
    kilitliyor.
    """
    dialog.adjustSize()
    dialog.setFixedSize(dialog.size())


def center(dialog: QDialog) -> None:
    """Pencereyi sahibinin ortasına koyar.

    Sahibi yoksa (ya da görünür değilse) ekranın ortasına. Qt kendiliğinden
    de ortalıyor ama üst pencere kenara yakınken taşabiliyor.
    """
    sahip = dialog.parentWidget()
    if sahip is not None and sahip.isVisible():
        alan = sahip.window().frameGeometry()
    else:
        ekran = dialog.screen()
        if ekran is None:
            return
        alan = ekran.availableGeometry()

    kutu = dialog.frameGeometry()
    kutu.moveCenter(alan.center())
    dialog.move(kutu.topLeft())
