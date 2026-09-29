"""Geçişli sayfa yığını (ui-taslak.md A3).

`QStackedWidget` sayfayı anında değiştiriyor. Bu sınıf aynı işi bir geçişle
yapıyor: eski sayfa söner, yeni sayfa `page` kadar aşağıdan (ya da ileri
gidişte sağdan, geri dönüşte soldan) yay eğrisiyle gelir.

**Nasıl:** sayfalar yerinden oynatılmıyor (yerleşim her an geri yazabilir).
Eski ve yeni sayfanın görüntüsü (`grab`) yığının üstündeki bir katmanda
çiziliyor; gerçek yeni sayfa altta zaten gösteriliyor. Katman fareyi
geçirdiği için geçiş sürerken tıklamalar yeni sayfaya ulaşıyor. Bitince
katman kalkıyor.

Animasyonlar kapalıysa (`motion.enabled()`) sayfa anında değişiyor.

**Tarayıcı içeren sayfanın görüntüsü alınmıyor.** Ders, not, rota gibi
belgeler `QWebEngineView`; yeni gösterilen böyle bir sayfanın `grab`'i o anda
henüz çizilmemiş ya da yarım çıkıyor ve geçişin ilk karelerinde eski ile yeni
sayfanın parçaları karışık görünüyordu (ölçüldü). O durumda katman yeni
sayfayı çizmiyor: gerçek sayfanın üstünde zemin renginde bir örtü söner
(`reveal`), eski sayfanın görüntüsü de hızla kaybolur.

Sekme içi geçişte (`subtle`) eski sekme hemen kalkıyor, yenisi belirir
(prototip: `panes.innerHTML = ''` ve `pgIn`).
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import QStackedWidget, QWidget

try:  # Belge alanları; yoksa (test ortamı) hiçbir sayfa tarayıcı içermiyor sayılır.
    from PySide6.QtWebEngineWidgets import QWebEngineView
except ImportError:  # pragma: no cover
    QWebEngineView = None

from ..resources.theme.motion import DISTANCE, DURATION, in_cubic, out_cubic, spring
from . import motion

NONE, FORWARD, BACK = "none", "forward", "back"


class _Overlay(QWidget):
    """Geçiş boyunca eski ve yeni sayfanın görüntüsünü çizen katman."""

    def __init__(self, parent: QWidget, old: QPixmap, new: QPixmap | None, direction: str,
                 background: QColor, total_ms: int, fade_ms: int) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.reset(old, new, direction, background, total_ms, fade_ms)

    def reset(self, old: QPixmap, new: QPixmap | None, direction: str,
              background: QColor, total_ms: int, fade_ms: int) -> None:
        """Katmanı yeni bir geçiş için kurar.

        Katman her geçişte **yeniden kullanılıyor**: yeni bir widget ilk kez
        gösterilirken uygulamanın stil dosyasıyla eşleştiriliyor ve bu tek
        başına 43 ms sürüyordu (sınavda sonraki soruya geçerken takılma).
        """
        # `new` yoksa örtü kipi: altta gerçek yeni sayfa, üstünde sönen zemin.
        self._old, self._new, self._dir = old, new, direction
        self._bg = background
        self._t = 0.0
        self._fade_part = fade_ms / max(1, total_ms)
        self.setGeometry(self.parentWidget().rect())
        # Zemin doluysa katman opak: Qt altındaki sayfayı her karede yeniden
        # çizmiyor. Önce çiziyordu; kare başına 10 ms katman + 11–24 ms sayfa
        # ile geçişler takılıyordu (ölçüldü).
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent,
                          background.alpha() == 255 and new is not None)

    def set_t(self, t: float) -> None:
        self._t = t
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt adlandırması)
        p = QPainter(self)
        if self._new is None:
            self._paint_reveal(p)
            p.end()
            return
        if self._bg.alpha():
            p.fillRect(self.rect(), self._bg)
        t = self._t
        eski = 1.0 - in_cubic(min(1.0, t / self._fade_part)) if self._fade_part > 0 else 0.0
        if eski > 0:
            p.setOpacity(eski)
            p.drawPixmap(QPointF(0, 0), self._old)
        k = spring(t)
        if self._dir == FORWARD:
            ofs = QPointF(DISTANCE["depth"] * (1 - k), 0)
        elif self._dir == BACK:
            ofs = QPointF(-DISTANCE["depth"] * (1 - k), 0)
        elif self._dir == "fade":
            # Sekme içi (prototip `pgIn`, 180 ms): yeni içerik 16 px aşağıdan belirir.
            ofs = QPointF(0, DISTANCE["page"] * (1 - out_cubic(t)))
        else:
            ofs = QPointF(0, DISTANCE["page"] * (1 - k))
        p.setOpacity(out_cubic(min(1.0, t * 1.6)))
        p.drawPixmap(ofs, self._new)
        p.end()

    def _paint_reveal(self, p: QPainter) -> None:
        """Örtü kipi: zemin renginde örtü söner, eski görüntü önce kaybolur."""
        t = self._t
        ortu = QColor(self._bg if self._bg.alpha() else QColor(0, 0, 0, 0))
        if ortu.alpha():
            # Prototip: sekmede `pgIn` 180 ms out, ekranda `pgFwd` 420 ms yay;
            # saydamlık da aynı eğriyle.
            k = out_cubic(t) if self._dir == "fade" else min(1.0, spring(t))
            ortu.setAlphaF(max(0.0, 1.0 - k))
            p.fillRect(self.rect(), ortu)
        eski = 1.0 - in_cubic(min(1.0, t / self._fade_part)) if self._fade_part > 0 else 0.0
        if eski > 0 and not self._old.isNull():
            p.setOpacity(eski)
            kay = {FORWARD: -1, BACK: 1}.get(self._dir, 0) * DISTANCE["depth"] * 0.5 * out_cubic(t)
            p.drawPixmap(QPointF(kay, 0), self._old)


def grab_clear(widget: QWidget) -> QPixmap:
    """Widget'ın görüntüsü, zemini saydam.

    `grab()` kendi zemini olmayan widget'ın arkasını pencere rengiyle
    dolduruyor; kartın üstünde koyu bir dikdörtgen olarak görünüyordu
    (rozet sayfası).
    """
    oran = widget.devicePixelRatioF()
    pix = QPixmap(max(1, round(widget.width() * oran)), max(1, round(widget.height() * oran)))
    pix.setDevicePixelRatio(oran)
    pix.fill(Qt.GlobalColor.transparent)
    widget.render(pix, QPoint(), QRegion(), QWidget.RenderFlag.DrawChildren)
    return pix


def play_swap(widget: QWidget, old: QPixmap, direction: str = NONE, background: str | None = None) -> None:
    """Bir widget'ın içeriği değişti: eski görüntü söner, yenisi kayarak gelir.

    Sayfalı ızgaralar (rozet duvarı) için; yığın değil, aynı widget yeniden
    dolduruluyor. Katman **opak** (kartın rengi): saydamken altındaki gerçek
    yeni sayfa da görünüyor, eski ve kayan yeni görüntüyle üst üste
    biniyordu.
    """
    if not motion.enabled() or not widget.isVisible():
        return
    from .effects import theme_palette

    yeni = grab_clear(widget)
    zemin = QColor(background or theme_palette()["surface"])
    katman = getattr(widget, "_swap_overlay", None)
    if katman is None:
        katman = _Overlay(widget, old, yeni, direction, zemin, DURATION["spring"], 0)
        widget._swap_overlay = katman
    else:
        motion.stop(katman, "t")
        katman.reset(old, yeni, direction, zemin, DURATION["spring"], 0)
    katman.show()
    katman.raise_()
    motion.animate(katman, "t", 0.0, 1.0, katman.set_t, DURATION["spring"], "linear",
                   on_done=katman.hide)


def after_reveal(widget: QWidget, fn) -> None:
    """`fn`'i, `widget` bekleyen bir geçişin içindeyse geçiş başlarken, değilse hemen çağırır.

    Geçiş belge hazır olana kadar eski ekranın görüntüsünü gösteriyor
    (`slide_to(wait=...)`). Ekranın giriş animasyonları (başlık, sıralı
    satırlar, boş durum simgesi) o sırada başlarsa görünmeden bitiyordu.
    """
    ata = widget.parentWidget()
    while ata is not None:
        if isinstance(ata, FadeStack) and ata._holding is not None and (  # noqa: SLF001
                ata._holding is widget or ata._holding.isAncestorOf(widget)):  # noqa: SLF001
            ata._held_calls.append(fn)  # noqa: SLF001
            return
        ata = ata.parentWidget()
    fn()


class FadeStack(QStackedWidget):
    """`slide_to` ile geçişli sayfa değiştiren yığın."""

    # Geçiş kurulurken doğru: o sırada gösterilen ekranlar (başlık gibi)
    # kendi giriş animasyonlarını oynatmasın. Geçiş katmanı ekranın
    # görüntüsünü alıyor; ekranın içinde ayrıca bir şey hareket ederse
    # katman kalkınca o parça yerinden sıçrıyordu (Notlarım başlığı).
    transitioning = False

    def __init__(self, parent: QWidget | None = None, subtle: bool = False,
                 drop_old: bool = False) -> None:
        super().__init__(parent)
        # `drop_old`: eski sayfa hemen kalkıyor, yenisi kayarak geliyor
        # (sınav sorusu, prototip `.qbody.in`).
        self._drop_old = drop_old
        # `subtle`: sekme içi geçiş — kayma yok, yalnızca kısa bir çapraz sönme.
        self._subtle = subtle
        self._overlay: _Overlay | None = None
        self._spare: _Overlay | None = None
        # Bekleyen geçişin sayfası ve başlarken çağrılacaklar (`after_reveal`).
        self._holding: QWidget | None = None
        self._held_calls: list = []
        # Zemin verilmemişse katman saydam: yığının arkasındaki kart (sınav,
        # ayarlar) görünür. Önce koyu varsayılan renkti ve kartın üstünde
        # siyah kutu olarak görünüyordu.
        self._background = QColor(0, 0, 0, 0)

    def set_background(self, color: str) -> None:
        """Katmanın zemini (tema değişince çağrılır)."""
        self._background = QColor(color)

    @staticmethod
    def _has_web(widget: QWidget) -> bool:
        if QWebEngineView is None:
            return False
        if isinstance(widget, QWebEngineView):
            return True
        return any(v.isVisibleTo(widget) for v in widget.findChildren(QWebEngineView))

    def slide_to(self, widget: QWidget, direction: str = NONE, wait=None) -> None:
        """Sayfayı geçişle değiştirir.

        `wait`: verilirse geçiş hemen başlamıyor; eski ekranın görüntüsü
        yeni sayfanın üstünde donuk duruyor, `wait(basla)` hazır olunca
        `basla()`'yı çağırıyor. Tarayıcı içeren sayfa gizliyken yavaş
        yükleniyor (476 ms, görünürken 48 ms; ölçüldü); sayfa görünür
        yapılıp donuk görüntünün altında yükleniyor, içerik hazır olunca
        kayarak giriyor.
        """
        eski = self.currentWidget()
        if widget is eski or eski is None or not self.isVisible() or not motion.enabled():
            self._drop_overlay()
            self.setCurrentWidget(widget)
            return

        # Opak zeminli yığında (ana ekranlar, bölüm sekmeleri) yeni sayfa
        # **canlı** giriyor: görüntüsü alınmıyor, örtünün altından beliriyor.
        # Görüntü alınınca sayfanın kendi giriş animasyonları (kartların
        # sırayla gelmesi, boş durum simgesi, yol düğümleri) katmanın altında
        # boşa oynuyor, katman kalkınca sıçrıyordu. Tarayıcı içeren sayfanın
        # görüntüsü zaten yarım çıkıyordu. Kartın içindeki yığınlar (sınav)
        # görüntüyle kayıyor.
        ortu = self._background.alpha() == 255 and not self._drop_old
        # Canlı geçişte eski ekranın görüntüsü alınmıyor: örtü ilk karede zemin
        # renginde tam kapalı. Görüntü almak (karşılama kartı, gölgeler) tek
        # başına 60–86 ms sürüyordu; patikaya tıklayınca takılma buydu.
        eski_goruntu = QPixmap() if ortu and wait is None else grab_clear(eski)
        self._drop_overlay()
        FadeStack.transitioning = not ortu
        if wait is not None:
            self._release_held()
            self._holding = widget
        try:
            self.setCurrentWidget(widget)
        finally:
            FadeStack.transitioning = False
        # Yeni sayfa ilk kez görünüyorsa yerleşimi şimdi kurulsun ki görüntüsü doğru çıksın.
        if widget.layout() is not None:
            widget.layout().activate()
        yeni_goruntu = None if ortu else grab_clear(widget)

        if self._subtle:
            # Eski sekme hemen kalkıyor (sönme payı 0), yenisi 180 ms'de belirir.
            direction, toplam, sonme = NONE, DURATION["short"], 0
        else:
            toplam, sonme = DURATION["spring"], DURATION["base"]
            if ortu:
                sonme = DURATION["short"]
            if self._drop_old:
                sonme = 0
        zemin = self._background
        if not zemin.alpha() and yeni_goruntu is not None:
            from .effects import theme_palette

            zemin = QColor(theme_palette()["surface"])
        yon = direction if not self._subtle else NONE
        if self._spare is None:
            self._spare = _Overlay(self, eski_goruntu, yeni_goruntu, yon, zemin, toplam, sonme)
        else:
            self._spare.reset(eski_goruntu, yeni_goruntu, yon, zemin, toplam, sonme)
        katman = self._spare
        if self._subtle:
            katman._dir = "fade"  # noqa: SLF001 — kayma yok
        katman.show()
        katman.raise_()
        self._overlay = katman

        # Canlı geçişte gerçek sayfa kayıyor (görüntüsü değil): ileri
        # giderken 24 px sağdan, geri dönerken soldan (`pgFwd`/`pgBack`),
        # sekmede ve yönsüz geçişte 16 px aşağıdan (`pgIn`). Yerleşim
        # sayfayı araya girip yerine koyarsa bir sonraki kare yeniden taşıyor.
        dx = dy = 0
        if ortu:
            if katman._dir == FORWARD:  # noqa: SLF001
                dx = DISTANCE["depth"]
            elif katman._dir == BACK:  # noqa: SLF001
                dx = -DISTANCE["depth"]
            else:
                dy = DISTANCE["page"]
        yay = katman._dir != "fade"  # noqa: SLF001

        def ilerle(t: float, k=katman, w=widget) -> None:
            k.set_t(t)
            if dx or dy:
                e = spring(t) if yay else out_cubic(t)
                w.move(round(dx * (1 - e)), round(dy * (1 - e)))

        def bitti(k=katman, w=widget) -> None:
            if dx or dy:
                w.move(0, 0)
            self._finish(k)

        ilerle(0.0)

        def basla(k=katman) -> None:
            if self._overlay is not k:
                self._release_held()
                return
            motion.animate(k, "t", 0.0, 1.0, ilerle, toplam, "linear", on_done=bitti)
            self._release_held()

        if wait is None:
            basla()
        else:
            wait(basla)

    def _release_held(self) -> None:
        cagrilar, self._held_calls = self._held_calls, []
        self._holding = None
        for fn in cagrilar:
            try:
                fn()
            except RuntimeError:
                pass  # widget bu arada silinmiş

    def _finish(self, katman: _Overlay) -> None:
        if self._overlay is katman:
            self._overlay = None
        katman.hide()
        # Görüntüler bırakılıyor; katman bir sonraki geçişte yeniden kullanılır.
        katman._old = katman._new = None  # noqa: SLF001

    def _drop_overlay(self) -> None:
        if self._overlay is not None:
            motion.stop(self._overlay, "t")
            self._finish(self._overlay)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        # Pencere geçiş sırasında boyut değiştirirse eski görüntü artık uymuyor.
        self._drop_overlay()
