"""Ayarlar penceresi.

Seçimler anında uygulanır — kaydet düğmesine basıp uygulamayı yeniden
başlatmak gerekmiyor.

**Neden açılır kutu değil de anahtar?** Önce dil ve tema birer `QComboBox`
idi. Ayar sayısı ikiden fazlaya çıkınca bu düzen dağıldı: her satırda
kapalı bir kutu duruyor, kutunun içindeki değeri görmek için tıklamak
gerekiyor ve iki seçenekli bir ayar için bu fazladan bir adım. Şimdi her
ayar tek bakışta okunuyor: solda adı ve ne işe yaradığı, sağda açık mı
kapalı mı olduğunu konumuyla gösteren bir anahtar.

Ayarlar gruplara ayrıldı; hepsi tek listede olunca hangisinin görünümle
hangisinin öğrenmeyle ilgili olduğu ayırt edilmiyordu.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Property, QPointF, QRectF, QSize, QThread, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..widgets import motion
from ..widgets.fade_stack import FadeStack
from ..core.language import LanguageManager
from ..core import animations, discord_presence
from ..core.quiz_timing import UNTIMED_QUIZ_KEY, untimed_quiz
from ..core.unlock import UNLOCK_ALL_KEY, unlock_all
from ..core.theme import ThemeManager
from ..core import updates
from ..core import celebration_sound, reminder_service, reminders
from .reminder_prompt import TIMES as REMINDER_TIMES
from ..widgets.common import DropdownBox
from .update_check import UpdateWorker
from ..core import docker_admin
from ..core.runner import sql_admin
from .confirm_dialog import ConfirmDialog
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.segmented import SegmentedControl
from ..widgets.toggle_switch import ToggleSwitch
from ..widgets.effects import repolish
from ..resources.icons import icon as make_icon
from ..version import APP_VERSION
from . import modal

# Kilit ve süre ayarlarının veritabanındaki anahtarları.

# Dil bir aç/kapa ayarı değil, iki seçenek arasında seçim. Anahtar
# kullanıldığında hangi tarafın hangi dil olduğu ancak açıklamayı okuyunca
# anlaşılıyordu; artık iki seçenek de ekranda yazılı.
# Dil adları kendi dillerinde yazılıyor; çevrilmiyor.
LANGUAGE_OPTIONS = [("tr", "Türkçe"), ("en", "English")]

# Tema seçicisi: yazı yerine simge. Ay koyu, güneş açık tema.
#
# Önce aç/kapa anahtarıydı ama anahtar iki durumlu bir **ayar** için doğru
# bileşen, iki seçenek arasında **seçim** için değil: "kapalı"nın koyu tema
# demek olduğu ancak açıklamayı okuyunca anlaşılıyordu. Dil seçicisiyle
# aynı bileşen kullanılıyor.
# Prototipte simge ve yazı birlikte ("☀ Açık", "☾ Koyu"); yazı `retranslate`te.
THEME_OPTIONS = [("light", "", "sun"), ("dark", "", "moon")]

# Soldaki kategoriler ve simgeleri. Sıra ekranda görünen sıra.
# SQL ve Docker ayrı sayfalardı; ikisi de "alıştırmaların kapladığı yer"
# olduğu için tek sayfada, ayrı kartlarda (Alican 7 Ekim).
PAGES = ["appearance", "learning", "notifications", "storage", "data", "updates"]
PAGE_ICONS = {
    "appearance": "palette",
    "learning": "graduation-cap",
    "notifications": "bell",
    "storage": "database",
    "data": "folder",
    "updates": "refresh",
}

# Pencere **sabit boyutlu**: hangi sayfa açılırsa açılsın aynı boy.
#
# Önce yükseklik en uzun sayfaya göre ölçülüyordu; hatırlatma satırları
# eklenince Öğrenme sayfası altı satıra çıktı ve iki satırlık Görünüm
# sayfasının altında pencerenin yarısı boş kaldı (Alican bildirdi). Şimdi
# kategoriler solda, ayarlar sağda gruplanmış bir kartın içinde; kısa
# sayfada boşluk kartın altında kalıyor, uzun sayfa kendi içinde kayıyor.
DIALOG_WIDTH = 820
DIALOG_HEIGHT = 560
SIDEBAR_WIDTH = 230
NAV_ICON_SIZE = 18


# Sunucu bu oturumda aranıp bulunamadıysa bir daha aranmıyor.
#
# `find_server` dört adayı sırayla deniyor ve her birinde beş saniye
# bekliyor; SQL Server kurulu olmayan birinde ayarları her açış yirmi
# saniyelik bir arama başlatıyordu. Kullanıcı arada sunucuyu kurarsa
# uygulamayı yeniden açması gerekiyor — kurulum zaten yeniden başlatma
# gerektiren bir iş.
_SUNUCU_YOK = False


def _size_label(megabytes: float) -> str:
    """Boyutu okunur bir metne çevirir.

    Bin megabaytın üstünde MB yazmak okunmuyor: 1280 MB yerine 1,3 GB.
    """
    if megabytes >= 1024:
        return f"{megabytes / 1024:.1f} GB".replace(".", ",")
    return f"{megabytes:.0f} MB"


class SqlAdminWorker(QThread):
    """Veritabanı listeleme/silme işini arka planda yürütür.

    İş denetleyici sürecine gidiyor ve silme onlarca saniye sürebiliyor;
    ayarlar penceresinin donmaması gerekiyor.
    """

    completed = Signal(dict)

    def __init__(
        self,
        action: str,
        names: list[str] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        # Sahibi ayarlar penceresi: sahipsiz bir QThread yalnızca Python
        # tarafında tutuluyordu ve pencere silinince çalışırken yok
        # edilebiliyordu.
        super().__init__(parent)
        self._action = action
        self._names = list(names or [])

    def run(self) -> None:  # noqa: D102
        try:
            self.completed.emit(sql_admin(self._action, self._names))
        except Exception:
            # Sunucu yoksa ya da beklenmedik bir şey olursa ayarlar
            # penceresi çökmüyor; satır "bulunamadı" diyor.
            self.completed.emit({"status": "crashed", "databases": []})


class DockerAdminWorker(QThread):
    """Docker'ın durumunu ve Odyssey'nin kapladığı yeri okur ya da siler.

    `docker info` Docker Desktop açılırken birkaç saniye sürebiliyor;
    pencere donmasın. İşler: `list`, `remove` (alıştırma imajları),
    `remove_base` (taban imajlar), `prune` (derleme önbelleği). Sonuç:
    {"status", "images", "base", "cache_mb", "action", "removed"}.
    """

    completed = Signal(dict)

    def __init__(self, action: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._action = action

    def run(self) -> None:  # noqa: D102
        bos = {"status": {"state": "stopped", "version": ""}, "images": [], "base": [],
               "cache_mb": 0.0, "action": self._action, "removed": 0}
        try:
            durum = docker_admin.status()
            sonuc = dict(bos, status=durum)
            if durum["state"] == "ok":
                if self._action == "remove":
                    sonuc["removed"] = docker_admin.remove_images()
                elif self._action == "remove_base":
                    sonuc["removed"] = docker_admin.remove_base_images()
                elif self._action == "prune":
                    docker_admin.prune_build_cache()
                sonuc["images"] = docker_admin.list_images()
                sonuc["base"] = docker_admin.list_base_images()
                sonuc["cache_mb"] = docker_admin.build_cache_mb()
            self.completed.emit(sonuc)
        except Exception:
            from ..core import log

            log.get(__name__).exception("Docker bilgisi okunamadı")
            self.completed.emit(bos)


class SettingRow(QWidget):
    """Bir ayar satırı: solda ad ve açıklama, sağda denetim.

    Denetim varsayılan olarak bir anahtar; `control` verilirse onun yerine
    o yerleştiriliyor (dil satırındaki segment seçici gibi).
    """

    def __init__(
        self, control: QWidget | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(16)

        metinler = QVBoxLayout()
        metinler.setSpacing(2)
        self.title = QLabel()
        self.title.setProperty("role", "srow-title")
        self.description = QLabel()
        self.description.setProperty("role", "srow-desc")
        self.description.setWordWrap(True)
        metinler.addWidget(self.title)
        metinler.addWidget(self.description)

        layout.addLayout(metinler, 1)

        self.switch = control if control is not None else ToggleSwitch()
        # Denetim metnin ilk satırıyla hizalanıyor; açıklama uzayınca
        # ortalanmış bir denetim aşağı kayıp başlıktan kopuyordu.
        layout.addWidget(self.switch, 0, Qt.AlignmentFlag.AlignVCenter)


class CloseX(QPushButton):
    """Sağ üstteki kapatma çarpısı: üzerine gelince zemin belirir, çarpı döner."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(32, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("role", "bare")
        self._turn = 0.0
        self._hover = 0.0

    def _get_turn(self) -> float:
        return self._turn

    def _set_turn(self, v: float) -> None:
        self._turn = v
        self.update()

    turn = Property(float, _get_turn, _set_turn)

    def enterEvent(self, event) -> None:  # noqa: N802
        self._hover = 1.0
        motion.animate_property(self, "turn", 1.0, "spring", "spring")
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self._hover = 0.0
        motion.animate_property(self, "turn", 0.0, "spring", "spring")
        super().leaveEvent(event)

    def paintEvent(self, event) -> None:  # noqa: N802
        from ..widgets.effects import theme_palette

        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._hover:
            g.setPen(Qt.PenStyle.NoPen)
            g.setBrush(QColor(p["surface_hover"]))
            g.drawEllipse(QRectF(self.rect()))
        g.translate(self.width() / 2, self.height() / 2)
        g.rotate(90 * self._turn)
        kalem = QPen(QColor(p["text"] if self._hover else p["text_muted"]), 1.8)
        kalem.setCapStyle(Qt.PenCapStyle.RoundCap)
        g.setPen(kalem)
        g.drawLine(QPointF(-5, -5), QPointF(5, 5))
        g.drawLine(QPointF(5, -5), QPointF(-5, 5))


class NavIndicator(QWidget):
    """Ayarlar kenar çubuğunda seçili kategorinin kayan zemini."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._rect = QRectF()

    def reset(self) -> None:
        self._rect = QRectF()

    def _set(self, r: QRectF) -> None:
        self._rect = r
        self.update()

    def move_to(self, button: QWidget) -> None:
        self.setGeometry(self.parentWidget().rect())
        hedef = QRectF(button.geometry())
        if self._rect.isEmpty():
            self._set(hedef)
            return
        motion.animate(self, "r", QRectF(self._rect), hedef, self._set, "spring", "spring")

    def paintEvent(self, event) -> None:  # noqa: N802
        if self._rect.isEmpty():
            return
        from ..widgets.effects import theme_palette

        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        g.setPen(Qt.PenStyle.NoPen)
        g.setBrush(QColor(p["surface_alt"]))
        g.drawRoundedRect(self._rect, 10, 10)


class SettingsDialog(QDialog):
    """Görünüm ve öğrenme ayarları."""

    # Kilit ayarı değişince ekranların o an yenilenmesi gerekiyor; yoksa
    # açık olan bölüm ekranı eski kilit durumunu göstermeye devam ediyor
    # ve kullanıcı çıkıp girmeden fark görmüyordu.
    lock_changed = Signal()
    # Öğrenme › Tanıtım turu: pencere kapanıyor, tur başlıyor.
    tour_requested = Signal()
    # Veri › İçe aktar: dosya hazırlandı, program yeniden başlamalı
    # (veritabanı açılmadan önce yerine konuyor).
    restart_requested = Signal()
    # Sınav süresi ayarı: açık bir sınav varken de o an uygulanıyor.
    timing_changed = Signal()

    presence_changed = Signal()
    # Animasyonlar ayarı: açık ekranlardaki döngüsel hareketler hemen duruyor.
    animations_changed = Signal(bool)
    # Elle yapılan denetimin sonucu: şeritteki duyuruyu da güncelliyor.
    update_found = Signal(object)
    # Kullanıcı ayarlardan güncellemeyi başlatmak istedi.
    update_requested = Signal(object)

    def __init__(
        self,
        language: LanguageManager,
        theme: ThemeManager,
        store,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._theme = theme
        self._store = store
        self._worker: UpdateWorker | None = None
        # Elle denetimde bulunan sürüm; düğme buna göre "Güncelle" oluyor.
        self._found = None
        self._sql_worker: SqlAdminWorker | None = None
        self._sql_databases: list[dict] = []
        self._docker_worker: DockerAdminWorker | None = None
        self._docker_images: list[dict] = []
        self._docker_result: dict | None = None
        self._docker_base: list[dict] = []
        self._docker_cache_mb = 0.0
        self._current_page = PAGES[0]

        modal.prepare(self)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(1, 1, 1, 1)  # modal çerçevesi görünsün
        outer.setSpacing(0)

        # --- sol: başlık, kategoriler, sürüm -----------------------------
        side = QFrame()
        side.setProperty("role", "settings-sidebar")
        side.setFixedWidth(SIDEBAR_WIDTH)
        side_layout = QVBoxLayout(side)
        side_layout.setContentsMargins(12, 20, 12, 18)
        side_layout.setSpacing(4)

        self._title = QLabel()
        self._title.setProperty("role", "modal-title")
        self._title.setContentsMargins(12, 4, 0, 0)
        side_layout.addWidget(self._title)
        side_layout.addSpacing(10)

        # Seçili kategorinin zemini: düğmelerin arkasında kayan tek katman (C14).
        self._nav_indicator = NavIndicator(side)
        self._nav_indicator.lower()
        self._nav_buttons: dict[str, QPushButton] = {}
        for name in PAGES:
            button = QPushButton()
            button.setProperty("variant", "settings-nav")
            button.setProperty("active", "false")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setIconSize(QSize(NAV_ICON_SIZE, NAV_ICON_SIZE))
            button.clicked.connect(lambda _=False, n=name: self._show_page(n))
            side_layout.addWidget(button)
            self._nav_buttons[name] = button
        # Bildirimler yalnızca Windows'ta; başka yerde kategori hiç görünmüyor.
        self._nav_buttons["notifications"].setVisible(reminder_service.supported())

        side_layout.addStretch(1)
        self._version = QLabel(f"Odyssey {APP_VERSION}")
        self._version.setProperty("role", "modal-version")
        self._version.setContentsMargins(12, 0, 0, 0)
        side_layout.addWidget(self._version)
        outer.addWidget(side)

        # --- sağ: sayfa başlığı, sayfalar, kapat ---------------------------
        content = QWidget()
        content.setProperty("role", "bare")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 26, 30, 26)
        content_layout.setSpacing(4)

        self._page_title = QLabel()
        self._page_title.setProperty("role", "modal-page-title")
        content_layout.addWidget(self._page_title)
        self._page_description = QLabel()
        self._page_description.setProperty("role", "modal-page-desc")
        self._page_description.setWordWrap(True)
        content_layout.addWidget(self._page_description)
        content_layout.addSpacing(14)

        # Pencere sabit boyutlu olduğu için yığın kullanılabiliyor; her
        # sayfa kendi kaydırma alanında (sığmayan sayfa kendi içinde kayar).
        self._stack = FadeStack(subtle=True)
        self._stack.setProperty("role", "bare")
        self._page_widgets = {
            "appearance": self._build_appearance(),
            "learning": self._build_learning(),
            "notifications": self._build_notifications(),
            "storage": self._build_storage(),
            "data": self._build_data(),
            "updates": self._build_updates(),
        }
        for name in PAGES:
            self._stack.addWidget(self._scrollable(self._page_widgets[name]))
        content_layout.addWidget(self._stack, 1)

        # Kapatma sağ üstte bir çarpı (prototip `.mpage .x`); Esc de kapatıyor.
        self._close_button = CloseX(content)
        self._close_button.clicked.connect(self.accept)
        self._close_button.move(DIALOG_WIDTH - SIDEBAR_WIDTH - 32 - 14 - 2, 14)
        self._close_button.raise_()
        outer.addWidget(content, 1)

        self._load_state()
        self._paint_switches(self._theme.effective_mode)
        self.retranslate()
        self._show_page(PAGES[0])

        # Odak kapatma düğmesinde başlıyor. Varsayılan haliyle ilk anahtara
        # gidiyor ve etrafındaki odak halkası, o ayar seçiliymiş gibi
        # duruyordu.
        self._close_button.setFocus()

        # Tema bu pencereden değiştiriliyor; anahtarların ve simgelerin
        # renkleri elle veriliyor, değişimi dinleyip yeniliyoruz.
        theme.theme_changed.connect(self._on_theme_changed)

    # --- sayfalar ---------------------------------------------------------
    #
    # Her sayfa kendi ayarlarını taşıyor ve sonunda esneme payı var: kısa
    # bir sayfa, uzun sayfanın yüksekliğine kadar gerildiğinde içerik
    # ortada değil **üstte** duruyor.

    def _page(self) -> tuple[QWidget, QVBoxLayout]:
        widget = QWidget()
        # Yalnızca yerleşim için: genel `QWidget` zemin kuralı burada
        # pencerede leke bırakıyordu.
        widget.setProperty("role", "bare")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["md"])
        return widget, layout

    def _group(self, rows: list[QWidget]) -> QFrame:
        """Satırları tek bir kartta, aralarında ince çizgiyle toplar."""
        card = QFrame()
        card.setProperty("role", "settings-group")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for index, row in enumerate(rows):
            if index:
                layout.addWidget(self._separator())
            layout.addWidget(row)
        return card

    def _scrollable(self, page: QWidget) -> QScrollArea:
        """Sayfa pencereye sığmazsa kendi içinde kaysın; pencere büyümesin."""
        area = QScrollArea()
        area.setWidgetResizable(True)
        area.setFrameShape(QFrame.Shape.NoFrame)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        area.setWidget(page)
        return area

    def _build_appearance(self) -> QWidget:
        sayfa, layout = self._page()

        self._theme_picker = SegmentedControl(THEME_OPTIONS)
        self._theme_picker.selected.connect(self._on_theme)
        self._theme_row = SettingRow(self._theme_picker)

        self._language_picker = SegmentedControl(LANGUAGE_OPTIONS)
        self._language_picker.selected.connect(self._on_language)
        self._language_row = SettingRow(self._language_picker)

        # Discord'da görünme bir görünüm ayarı: öğrenmeyi değil, başkalarının
        # ne gördüğünü değiştiriyor. Önce Öğrenme sayfasındaydı (Alican taşıttı).
        self._presence_row = SettingRow()
        self._presence_row.switch.toggled.connect(self._on_presence)

        self._animations_row = SettingRow()
        self._animations_row.switch.toggled.connect(self._on_animations)

        layout.addWidget(self._group(
            [self._theme_row, self._language_row, self._presence_row,
             self._animations_row]
        ))
        layout.addStretch(1)
        return sayfa

    def _build_learning(self) -> QWidget:
        sayfa, layout = self._page()

        self._unlock_row = SettingRow()
        self._unlock_row.switch.toggled.connect(self._on_unlock)

        self._untimed_row = SettingRow()
        self._untimed_row.switch.toggled.connect(self._on_untimed)

        self._tour_button = QPushButton()
        self._tour_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._tour_button.clicked.connect(self._on_tour)
        self._tour_row = SettingRow(self._tour_button)

        layout.addWidget(self._group([self._unlock_row, self._untimed_row, self._tour_row]))
        layout.addStretch(1)
        return sayfa

    def _on_tour(self) -> None:
        self.tour_requested.emit()
        self.accept()

    def _build_notifications(self) -> QWidget:
        """Seri hatırlatmaları: anahtar, saat ve deneme bildirimi.

        Önce Öğrenme sayfasındaydı; o sayfa altı satıra çıkınca pencerenin
        boyunu büyütüyordu. Yalnızca Windows'ta (bildirim ve Görev
        Zamanlayıcı Windows'a özgü); başka yerde kategori gizli.
        """
        sayfa, layout = self._page()

        self._reminder_row = SettingRow()
        self._reminder_row.switch.toggled.connect(self._on_reminders)

        self._reminder_time = DropdownBox(
            color=PALETTES.get(self._theme.effective_mode, PALETTES["dark"])["text_muted"]
        )
        self._reminder_time.addItems(REMINDER_TIMES)
        self._reminder_time.setFixedWidth(110)
        self._reminder_time.currentTextChanged.connect(self._on_reminder_time)
        self._reminder_time_row = SettingRow(self._reminder_time)

        self._reminder_test = QPushButton()
        self._reminder_test.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reminder_test.clicked.connect(self._on_reminder_test)
        self._reminder_test_row = SettingRow(self._reminder_test)

        layout.addWidget(self._group(
            [self._reminder_row, self._reminder_time_row, self._reminder_test_row]
        ))

        # Kutlama kartlarının sesi program açıkken çalıyor; hatırlatmalarla
        # ilgisi yok, o yüzden ayrı bir kartta.
        self._sound_row = SettingRow()
        self._sound_row.switch.toggled.connect(self._on_sound)
        layout.addWidget(self._group([self._sound_row]))
        layout.addStretch(1)
        return sayfa

    def _build_storage(self) -> QWidget:
        """Alıştırmaların bilgisayarda kapladığı yer: SQL ve Docker ayrı kartlarda.

        SQL: her alıştırma kendi veritabanını açıyor, her biri ~16 MB
        (ölçüldü); patikanın tamamında bir gigabaytı geçiyor. Docker: her
        alıştırma kendi imajını kuruyor; yalnızca `odyssey=1` etiketliler ve
        iki taban imaj sayılıp siliniyor, kişinin kendi imajlarına
        dokunulmuyor. Derleme önbelleği etiketle ayrılamıyor, ortak.
        """
        sayfa, layout = self._page()

        def baslik() -> QLabel:
            etiket = QLabel()
            etiket.setProperty("role", "section")
            etiket.setContentsMargins(4, 0, 0, 0)
            return etiket

        def dugme(slot) -> QPushButton:
            button = QPushButton()
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(slot)
            return button

        self._sql_heading = baslik()
        self._sql_button = dugme(self._on_sql_clear)
        self._sql_row = SettingRow(self._sql_button)
        self._sql_status = self._sql_row.description
        layout.addWidget(self._sql_heading)
        layout.addWidget(self._group([self._sql_row]))

        # SQL kartı gibi yalnızca depolama satırları. Önce üstte bir durum
        # satırı vardı ve Docker kapalıyken satırlar gizlenip yalnızca o
        # kalıyordu; kart "silme" kartı gibi okunmuyordu (Alican). Şimdi
        # satırlar hep yerinde, Docker kapalıysa açıklamaları bunu söylüyor.
        self._docker_heading = baslik()
        self._docker_button = dugme(self._on_docker_clear)
        self._docker_row = SettingRow(self._docker_button)
        self._docker_base_button = dugme(self._on_docker_base_clear)
        self._docker_base_row = SettingRow(self._docker_base_button)
        self._docker_cache_button = dugme(self._on_docker_prune)
        self._docker_cache_row = SettingRow(self._docker_cache_button)
        self._docker_autostop_row = SettingRow()
        self._docker_autostop_row.switch.toggled.connect(self._on_docker_autostop)
        layout.addWidget(self._docker_heading)
        # Pencere sabit boyutlu; sayfa kaydırma çubuğu çıkarmadan sığsın diye
        # kapatma anahtarı ayrı kart değil, Docker kartının son satırı ve bu
        # sayfadaki satırların dikey iç boşluğu 14 yerine 10 (ölçüldü: ayrı
        # kartla 471 piksel gerekiyordu, görünen alan 416).
        for row in (self._sql_row, self._docker_row, self._docker_base_row,
                    self._docker_cache_row, self._docker_autostop_row):
            row.layout().setContentsMargins(18, 10, 18, 10)
        layout.addWidget(self._group([self._docker_row, self._docker_base_row,
                                      self._docker_cache_row, self._docker_autostop_row]))
        layout.addStretch(1)
        return sayfa

    def _on_docker_autostop(self, checked: bool) -> None:
        # Odyssey kapanırken okunuyor; açık ekrana sinyal gerekmiyor.
        docker_admin.set_autostop(self._store, checked)

    def _build_data(self) -> QWidget:
        """İlerlemeyi başka bir bilgisayara taşımak ve otomatik yedekler.

        Alican iki bilgisayar kullanıyor; ilerlemesi ikisinde ayrıydı.
        Ayrıntı `app/core/transfer.py`.
        """
        sayfa, layout = self._page()

        self._export_button = QPushButton()
        self._export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._export_button.clicked.connect(self._on_export)
        self._export_row = SettingRow(self._export_button)

        self._import_button = QPushButton()
        self._import_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._import_button.clicked.connect(self._on_import)
        self._import_row = SettingRow(self._import_button)

        self._backups_button = QPushButton()
        self._backups_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._backups_button.clicked.connect(self._on_open_backups)
        self._backups_row = SettingRow(self._backups_button)

        layout.addWidget(self._group([self._export_row, self._import_row]))
        layout.addWidget(self._group([self._backups_row]))
        layout.addStretch(1)
        return sayfa

    def _on_export(self) -> None:
        from datetime import date

        from PySide6.QtCore import QStandardPaths
        from PySide6.QtWidgets import QFileDialog

        from ..core import transfer
        from ..core.avatar import avatar_path
        from ..paths import database_path

        t = self._language.t
        klasor = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        oneri = str(Path(klasor) / t("settings.export_file", date=date.today().isoformat()))
        yol, _ = QFileDialog.getSaveFileName(self, t("settings.export"), oneri, t("settings.export_filter"))
        if not yol:
            return
        try:
            hedef = transfer.export_to(Path(yol), database_path(), avatar_path())
        except Exception:  # noqa: BLE001 — kullanıcıya söylenir, kayda yazılır
            from ..core import log

            log.get(__name__).exception("Dışa aktarma başarısız")
            self._export_row.description.setText(t("settings.export_failed"))
            return
        self._export_row.description.setText(t("settings.export_done", name=hedef.name))

    def _on_import(self) -> None:
        from PySide6.QtCore import QStandardPaths
        from PySide6.QtWidgets import QFileDialog

        from ..core import transfer
        from ..paths import user_data_dir

        t = self._language.t
        klasor = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        yol, _ = QFileDialog.getOpenFileName(self, t("settings.import"), klasor, t("settings.export_filter"))
        if not yol:
            return
        try:
            arsiv = transfer.read_archive(Path(yol))
        except transfer.TransferError as hata:
            self._import_row.description.setText(t(f"settings.import_error_{hata.code}"))
            return
        tarih = arsiv.created_at[:10]
        if arsiv.name:
            metin = t("settings.import_message_named", name=arsiv.name, date=tarih,
                      version=arsiv.app_version, quizzes=arsiv.quizzes_passed)
        else:
            metin = t("settings.import_message", date=tarih, version=arsiv.app_version,
                      quizzes=arsiv.quizzes_passed)
        kutu = ConfirmDialog(t("settings.import_title"), metin, t("settings.import_confirm"),
                             t("common.cancel"), self)
        if kutu.exec() != ConfirmDialog.DialogCode.Accepted:
            return
        try:
            transfer.stage(arsiv, user_data_dir())
        except OSError:
            from ..core import log

            log.get(__name__).exception("İçe aktarma hazırlanamadı")
            self._import_row.description.setText(t("settings.export_failed"))
            return
        self.restart_requested.emit()
        self.accept()

    def _on_open_backups(self) -> None:
        import os

        from ..paths import backups_dir

        klasor = backups_dir()
        klasor.mkdir(parents=True, exist_ok=True)
        try:
            os.startfile(str(klasor))  # noqa: S606 — kullanıcının kendi klasörü
        except (AttributeError, OSError):
            from PySide6.QtCore import QUrl
            from PySide6.QtGui import QDesktopServices

            QDesktopServices.openUrl(QUrl.fromLocalFile(str(klasor)))

    def _build_updates(self) -> QWidget:
        sayfa, layout = self._page()

        self._update_row = SettingRow()
        self._update_row.switch.toggled.connect(self._on_update_check)

        self._check_button = QPushButton()
        self._check_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._check_button.clicked.connect(self._on_update_button)
        self._check_row = SettingRow(self._check_button)
        # Denetimin sonucu ("Güncelsiniz", "0.8.4 çıktı") bu satırın
        # açıklamasında.
        self._update_status = self._check_row.description

        layout.addWidget(self._group([self._update_row, self._check_row]))
        layout.addStretch(1)
        return sayfa

    def _show_page(self, name: str) -> None:
        """Görünen sayfayı değiştirir. Pencerenin boyu değişmiyor."""
        if name not in PAGES:
            return
        self._current_page = name
        self._stack.slide_to(self._stack.widget(PAGES.index(name)))
        for ad, button in self._nav_buttons.items():
            button.setProperty("active", "true" if ad == name else "false")
            repolish(button)
        self._paint_nav_icons()
        self._render_page_header()
        QTimer.singleShot(0, self, lambda: self._nav_indicator.move_to(self._nav_buttons[name]))

    def _render_page_header(self) -> None:
        t = self._language.t
        self._page_title.setText(t(f"settings.nav_{self._current_page}"))
        self._page_description.setText(t(f"settings.page_{self._current_page}"))

    def _paint_nav_icons(self) -> None:
        p = PALETTES.get(self._theme.effective_mode, PALETTES["light"])
        for ad, button in self._nav_buttons.items():
            renk = p["text"] if ad == self._current_page else p["text_muted"]
            button.setIcon(make_icon(PAGE_ICONS[ad], renk, NAV_ICON_SIZE))

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        modal.center(self)
        # Pencere belirerek açılır (B9); gösterge seçili kategoriye oturur.
        motion.animate_property(self, "windowOpacity", 1.0, "short", "out", start=0.0)
        self._nav_indicator.reset()
        QTimer.singleShot(0, self, lambda: self._nav_indicator.move_to(self._nav_buttons[self._current_page]))

    def done(self, result: int) -> None:  # noqa: D102
        # Pencere kapanınca siliniyor. Arka planda süren bir iş (güncelleme
        # denetimi, veritabanı silme) varsa iş parçacığı çalışırken yok
        # edilip programı çökertmesin: sahibi ana pencere oluyor (kapanışta
        # onları bekliyor), iş bitince de kendini siliyor.
        sahip = self.parentWidget()
        for worker in (self._worker, self._sql_worker, self._docker_worker):
            if worker is not None and worker.isRunning():
                worker.setParent(sahip)
                worker.finished.connect(worker.deleteLater)
        super().done(result)
        # Burada sayı tazelenmiyor. Önceden kapanışta yeni bir SQL sayımı
        # başlatılıyordu; pencere hemen ardından silindiği için iş parçacığı
        # çalışırken yok ediliyor ve program "QThread: Destroyed while
        # thread is still running" ile çöküyordu (Alican bildirdi). Pencere
        # her açılışta yeniden kuruluyor ve sayım açılışta zaten yapılıyor.

    def _separator(self) -> QFrame:
        line = QFrame()
        # Şekil **verilmiyor**: `HLine` seçilince Qt çerçeveyi kendi
        # çiziyor ve QSS'teki arka plan rengi ekrana hiç çıkmıyordu.
        line.setFrameShape(QFrame.Shape.NoFrame)
        line.setFixedHeight(1)
        line.setProperty("role", "divider")
        return line

    # --- durum ------------------------------------------------------------

    def _load_state(self) -> None:
        """Kayıtlı değerleri anahtarlara yerleştirir.

        `set_checked` sinyal yaymadığı için bu, ayarları yeniden yazmıyor.
        """
        self._theme_picker.set_value(self._theme.effective_mode)
        self._language_picker.set_value(self._language.language)
        self._unlock_row.switch.set_checked(
            unlock_all(self._store), animate=False
        )
        self._untimed_row.switch.set_checked(
            untimed_quiz(self._store), animate=False
        )
        self._update_row.switch.set_checked(
            updates.enabled(self._store), animate=False
        )
        self._presence_row.switch.set_checked(
            discord_presence.enabled(self._store), animate=False
        )
        self._animations_row.switch.set_checked(
            animations.enabled(self._store), animate=False
        )
        self._reminder_row.switch.set_checked(
            reminders.enabled(self._store), animate=False
        )
        self._sound_row.switch.set_checked(
            celebration_sound.enabled(self._store), animate=False
        )
        self._docker_autostop_row.switch.set_checked(
            docker_admin.autostop_enabled(self._store), animate=False
        )
        self._reminder_time.blockSignals(True)
        self._reminder_time.setCurrentText(
            reminders.reminder_time(self._store).strftime("%H:%M")
        )
        self._reminder_time.blockSignals(False)
        self._sync_reminder_rows()

    def _paint_switches(self, mode: str) -> None:
        p = PALETTES.get(mode, PALETTES["light"])
        # Segment düğmelerinin **zeminini** QSS veriyor ama içlerindeki
        # güneş/ay birer `QIcon`; onlara QSS ulaşmıyor.
        self._theme_picker.set_icon_colors(p["text_muted"], p["text"])
        self._paint_nav_icons()
        self._reminder_time.set_arrow_color(p["text_muted"])
        for row in (self._unlock_row, self._untimed_row,
                    self._presence_row, self._update_row, self._reminder_row,
                    self._sound_row, self._animations_row, self._docker_autostop_row):
            row.switch.set_colors(
                # Kart zemininde (`surface`) kapalı anahtarın izi seçilsin;
                # `surface_alt` koyu temada kartla neredeyse aynıydı.
                track_off=p["border"],
                track_on=p["accent"],
                knob=p["surface"] if mode == "dark" else "#FFFFFF",
                border=p["border_strong"],
            )

    # --- olaylar ----------------------------------------------------------

    def _on_theme_changed(self, mode: str) -> None:
        # Pencerenin çerçevesi yok; boyanacak başlık çubuğu da yok.
        self._paint_switches(self._theme.effective_mode)

    def _on_theme(self, mode: str) -> None:
        self._theme.set_mode(mode)

    def _on_language(self, code: str) -> None:
        self._language.set_language(code)

    def _on_unlock(self, checked: bool) -> None:
        self._store.set_setting(UNLOCK_ALL_KEY, "1" if checked else "")
        self.lock_changed.emit()

    def _on_untimed(self, checked: bool) -> None:
        self._store.set_setting(UNTIMED_QUIZ_KEY, "1" if checked else "")
        self.timing_changed.emit()

    def _on_sound(self, checked: bool) -> None:
        # Kart gösterilirken okunuyor; açık ekrana sinyal gerekmiyor.
        celebration_sound.set_enabled(self._store, checked)

    def _on_presence(self, checked: bool) -> None:
        discord_presence.set_enabled(self._store, checked)
        self.presence_changed.emit()

    def _on_animations(self, checked: bool) -> None:
        animations.set_enabled(self._store, checked)
        self.animations_changed.emit(checked)

    def _sync_reminder_rows(self) -> None:
        acik = reminders.enabled(self._store)
        self._reminder_time.setEnabled(acik)
        self._reminder_test.setEnabled(acik)

    def _on_reminders(self, checked: bool) -> None:
        """Açınca görev kuruluyor, kapatınca görev ve kayıtlar siliniyor."""
        if checked:
            ok, error = reminder_service.enable(
                self._store, self._reminder_time.currentText()
            )
            if not ok:
                # Kurulamadıysa anahtar açık görünmesin.
                self._reminder_row.switch.set_checked(False, animate=False)
                self._reminder_test_row.description.setText(
                    self._language.t("reminder.enable_failed", error=error[:160])
                )
        else:
            reminder_service.disable(self._store)
        self._sync_reminder_rows()

    def _on_reminder_time(self, text: str) -> None:
        """Saat değişince görev yeni saatle yeniden kuruluyor."""
        if reminders.enabled(self._store):
            reminder_service.enable(self._store, text)
        else:
            self._store.set_setting(reminders.TIME_KEY, text)

    def _on_reminder_test(self) -> None:
        ok = reminder_service.send_test(self._store)
        self._reminder_test_row.description.setText(
            self._language.t(
                "settings.reminder_test_sent" if ok else "settings.reminder_test_failed"
            )
        )

    def _on_update_check(self, checked: bool) -> None:
        updates.set_enabled(self._store, checked)
        self._check_button.setEnabled(checked)
        if not checked:
            self._set_status("")

    # --- güncelleme -------------------------------------------------------

    def _on_update_button(self) -> None:
        """Düğme iki iş yapıyor: denetle, ya da bulunanı kur.

        Denetim "yeni sürüm var" dediğinde düğme **Güncelle**'ye dönüşüyor.
        Önceden yalnızca durum satırına yazıyordu: kullanıcı güncelleme
        olduğunu öğreniyor ama ayarlardan kuramıyordu (Alican bunu
        bildirdi).
        """
        if self._found is not None:
            self.accept()
            self.update_requested.emit(self._found)
            return
        self._check_now()

    def _check_now(self) -> None:
        """Elle denetim: "bugün zaten baktım" kuralını atlıyor."""
        if self._worker is not None and self._worker.isRunning():
            return
        if not updates.should_check(self._store, ignore_interval=True):
            return
        self._check_button.setEnabled(False)
        self._set_status(self._language.t("update.checking"))

        self._worker = UpdateWorker(parent=self)
        self._worker.finished_with.connect(self._on_checked)
        self._worker.start()

    def _on_checked(self, info) -> None:
        updates.record(self._store, info)
        self._check_button.setEnabled(updates.enabled(self._store))
        t = self._language.t
        if info.status == "newer":
            self._found = info
            self._check_button.setText(t("update.notice_update"))
            self._check_button.setProperty("variant", "primary")
            repolish(self._check_button)
            self._set_status(t("update.available", version=info.version))
        elif info.status == "current":
            self._set_status(t("update.current"))
        elif info.status == "offline":
            self._set_status(t("update.offline"))
        else:
            self._set_status(t("update.failed"))
        self.update_found.emit(info)

    def _set_status(self, text: str) -> None:
        """Denetim satırının açıklamasına sonucu yazar.

        Pencere sabit boyutlu; satır uzarsa sayfa kendi içinde kayıyor.
        """
        self._update_status.setText(text)

    # --- metinler ---------------------------------------------------------

    # --- SQL veritabanları ------------------------------------------------

    def _sql_refresh(self) -> None:
        """Veritabanı sayısını ve kapladığı yeri arka planda okur."""
        if _SUNUCU_YOK:
            self._sql_status.setText(
                self._language.t("settings.sql_unavailable")
            )
            self._sql_button.setEnabled(False)
            return
        if self._sql_worker is not None and self._sql_worker.isRunning():
            return
        self._sql_button.setEnabled(False)
        self._sql_status.setText(self._language.t("settings.sql_reading"))

        self._sql_worker = SqlAdminWorker("list_databases", parent=self)
        self._sql_worker.completed.connect(self._on_sql_listed)
        self._sql_worker.start()

    def _on_sql_listed(self, result: dict) -> None:
        t = self._language.t
        self._sql_databases = result.get("databases", [])

        if result.get("status") != "ok":
            # Sunucu kurulu değilse bu bölüm bir sorun değil, sadece
            # gösterecek bir şey yok.
            global _SUNUCU_YOK
            _SUNUCU_YOK = True
            self._sql_status.setText(t("settings.sql_unavailable"))
            self._sql_button.setEnabled(False)
            return

        adet = len(self._sql_databases)
        if not adet:
            self._sql_status.setText(t("settings.sql_none"))
            self._sql_button.setEnabled(False)
            return

        toplam = sum(float(v.get("mb", 0)) for v in self._sql_databases)
        self._sql_status.setText(
            t("settings.sql_usage", count=adet, size=_size_label(toplam))
        )
        self._sql_button.setEnabled(True)

    def _on_sql_clear(self) -> None:
        """Onay aldıktan sonra bütün alıştırma veritabanlarını siler."""
        if not self._sql_databases:
            return

        t = self._language.t
        toplam = sum(float(v.get("mb", 0)) for v in self._sql_databases)
        onay = ConfirmDialog(
            t("settings.sql_confirm_title"),
            t(
                "settings.sql_confirm_body",
                count=len(self._sql_databases),
                size=_size_label(toplam),
            ),
            t("settings.sql_confirm_yes"),
            t("common.cancel"),
            self,
        )
        if not onay.exec():
            return

        self._sql_button.setEnabled(False)
        self._sql_status.setText(t("settings.sql_clearing"))
        self._sql_worker = SqlAdminWorker(
            "drop_databases", [v["name"] for v in self._sql_databases], parent=self
        )
        self._sql_worker.completed.connect(self._on_sql_cleared)
        self._sql_worker.start()

    def _on_sql_cleared(self, result: dict) -> None:
        silinen = len(result.get("dropped", []))
        hatalar = result.get("errors", [])
        if hatalar:
            self._sql_status.setText(
                self._language.t(
                    "settings.sql_cleared_partly",
                    count=silinen,
                    failed=len(hatalar),
                )
            )
            self._sql_button.setEnabled(True)
            return
        self._sql_status.setText(
            self._language.t("settings.sql_cleared", count=silinen)
        )
        self._sql_databases = []
        self._sql_button.setEnabled(False)

    # --- Docker imajları --------------------------------------------------

    def _docker_buttons(self, enabled: bool) -> None:
        for button in (self._docker_button, self._docker_base_button, self._docker_cache_button):
            button.setEnabled(enabled)

    def _docker_refresh(self, action: str = "list") -> None:
        if self._docker_worker is not None and self._docker_worker.isRunning():
            return
        t = self._language.t
        self._docker_buttons(False)
        satir = {"remove": self._docker_row, "remove_base": self._docker_base_row,
                 "prune": self._docker_cache_row}.get(action)
        if satir is not None:
            satir.description.setText(t("settings.docker_clearing"))
        else:
            for row in (self._docker_row, self._docker_base_row, self._docker_cache_row):
                row.description.setText(t("settings.docker_reading"))
        self._docker_worker = DockerAdminWorker(action, parent=self)
        self._docker_worker.completed.connect(self._on_docker_listed)
        self._docker_worker.start()

    def _on_docker_listed(self, result: dict) -> None:
        self._docker_result = result
        self._render_docker()

    def _render_docker(self) -> None:
        """Durumu seçili dilde yazar (dil değişince Docker'a yeniden sorulmuyor)."""
        result = self._docker_result
        if result is None:
            return
        t = self._language.t
        durum = result.get("status") or {}
        state = durum.get("state", "stopped")
        if state != "ok":
            # Boyutlar yalnızca Docker çalışırken okunabiliyor.
            for row in (self._docker_row, self._docker_base_row, self._docker_cache_row):
                row.description.setText(t(f"settings.docker_{state}"))
            self._docker_buttons(False)
            return
        self._docker_images = result.get("images", [])
        self._docker_base = result.get("base", [])
        self._docker_cache_mb = float(result.get("cache_mb", 0.0))
        eylem = result.get("action", "list")

        if self._docker_images:
            toplam = sum(docker_admin.size_mb(item.get("size", "")) for item in self._docker_images)
            metin = t("settings.docker_usage", count=len(self._docker_images), size=_size_label(toplam))
        else:
            metin = t("settings.docker_none")
        if eylem == "remove":
            metin = t("settings.docker_cleared", count=result.get("removed", 0)) + " " + metin
        self._docker_row.description.setText(metin)
        self._docker_button.setEnabled(bool(self._docker_images))

        if self._docker_base:
            toplam = sum(docker_admin.size_mb(item.get("size", "")) for item in self._docker_base)
            adlar = ", ".join(item["name"] for item in self._docker_base)
            metin = t("settings.docker_base_usage", names=adlar, size=_size_label(toplam))
        else:
            metin = t("settings.docker_base_none")
        if eylem == "remove_base":
            metin = t("settings.docker_cleared", count=result.get("removed", 0)) + " " + metin
        self._docker_base_row.description.setText(metin)
        self._docker_base_button.setEnabled(bool(self._docker_base))

        if self._docker_cache_mb >= 1:
            metin = t("settings.docker_cache_usage", size=_size_label(self._docker_cache_mb))
        else:
            metin = t("settings.docker_cache_none")
        if eylem == "prune":
            metin = t("settings.docker_cache_cleared") + " " + metin
        self._docker_cache_row.description.setText(metin)
        self._docker_cache_button.setEnabled(self._docker_cache_mb >= 1)

    def _confirm(self, prefix: str, **values) -> bool:
        t = self._language.t
        onay = ConfirmDialog(
            t(f"settings.{prefix}_confirm_title"),
            t(f"settings.{prefix}_confirm_body", **values),
            t(f"settings.{prefix}_confirm_yes"),
            t("common.cancel"),
            self,
        )
        return bool(onay.exec())

    def _on_docker_clear(self) -> None:
        if not self._docker_images:
            return
        toplam = sum(docker_admin.size_mb(item.get("size", "")) for item in self._docker_images)
        if self._confirm("docker", count=len(self._docker_images), size=_size_label(toplam)):
            self._docker_refresh("remove")

    def _on_docker_base_clear(self) -> None:
        if not self._docker_base:
            return
        toplam = sum(docker_admin.size_mb(item.get("size", "")) for item in self._docker_base)
        if self._confirm("docker_base", size=_size_label(toplam)):
            self._docker_refresh("remove_base")

    def _on_docker_prune(self) -> None:
        if self._docker_cache_mb < 1:
            return
        if self._confirm("docker_cache", size=_size_label(self._docker_cache_mb)):
            self._docker_refresh("prune")

    def retranslate(self) -> None:
        t = self._language.t
        self.setWindowTitle(t("settings.title"))
        self._title.setText(t("settings.title"))
        self._close_button.setToolTip(t("common.close"))
        self._theme_picker.button("light").setText(" " + t("settings.theme_light_short"))
        self._theme_picker.button("dark").setText(" " + t("settings.theme_dark_short"))
        for ad, button in self._nav_buttons.items():
            button.setText(t(f"settings.nav_{ad}"))
        self._render_page_header()

        self._theme_row.title.setText(t("settings.theme"))
        self._theme_row.description.setText(t("settings.theme_help"))
        self._theme_picker.set_tooltips({
            "dark": t("settings.theme_dark"),
            "light": t("settings.theme_light"),
        })

        self._language_row.title.setText(t("settings.language"))
        self._language_row.description.setText(t("settings.language_help"))

        self._unlock_row.title.setText(t("settings.unlock_all"))
        self._tour_row.title.setText(t("settings.tour"))
        self._tour_row.description.setText(t("settings.tour_help"))
        self._tour_button.setText(t("settings.tour_start"))
        self._unlock_row.description.setText(t("settings.unlock_all_help"))

        self._untimed_row.title.setText(t("settings.untimed_quiz"))
        self._untimed_row.description.setText(t("settings.untimed_quiz_help"))
        self._presence_row.title.setText(t("settings.discord"))
        self._presence_row.description.setText(t("settings.discord_help"))
        self._animations_row.title.setText(t("settings.animations"))
        self._animations_row.description.setText(t("settings.animations_help"))
        self._sound_row.title.setText(t("settings.celebration_sound"))
        self._sound_row.description.setText(t("settings.celebration_sound_help"))
        self._reminder_row.title.setText(t("settings.reminders"))
        self._reminder_row.description.setText(t("settings.reminders_help"))
        self._reminder_time_row.title.setText(t("settings.reminder_time"))
        self._reminder_time_row.description.setText(t("settings.reminder_time_help"))
        self._reminder_test_row.title.setText(t("settings.reminder_test_title"))
        self._reminder_test_row.description.setText(t("settings.reminder_test_help"))
        self._reminder_test.setText(t("settings.reminder_test"))

        self._sql_heading.setText(t("settings.storage_sql").upper())
        self._sql_row.title.setText(t("settings.sql_databases"))
        self._sql_button.setText(t("settings.sql_clear"))
        # Durum satırı sayı taşıyor; dil değişince yeniden üretilmesi
        # gerekiyor, yoksa eski dilde kalıyor.
        self._sql_refresh()

        self._docker_heading.setText(t("settings.storage_docker").upper())
        self._docker_row.title.setText(t("settings.docker_images"))
        self._docker_button.setText(t("settings.docker_clear"))
        self._docker_base_row.title.setText(t("settings.docker_base"))
        self._docker_base_button.setText(t("settings.docker_base_clear"))
        self._docker_cache_row.title.setText(t("settings.docker_cache"))
        self._docker_cache_button.setText(t("settings.docker_cache_clear"))
        self._docker_autostop_row.title.setText(t("settings.docker_autostop"))
        self._docker_autostop_row.description.setText(t("settings.docker_autostop_help"))
        if self._docker_result is None:
            self._docker_refresh()
        else:
            self._render_docker()

        self._export_row.title.setText(t("settings.export"))
        self._export_row.description.setText(t("settings.export_help"))
        self._export_button.setText(t("settings.export_button"))
        self._import_row.title.setText(t("settings.import"))
        self._import_row.description.setText(t("settings.import_help"))
        self._import_button.setText(t("settings.import_button"))
        self._backups_row.title.setText(t("settings.backups"))
        self._backups_row.description.setText(t("settings.backups_help"))
        self._backups_button.setText(t("settings.backups_button"))

        self._update_row.title.setText(t("settings.update_check"))
        self._update_row.description.setText(t("settings.update_check_help"))
        self._check_row.title.setText(t("settings.update_manual"))
        if not self._update_status.text():
            self._update_status.setText(t("settings.update_manual_help"))
        self._check_button.setText(
            t("update.notice_update") if self._found is not None
            else t("update.check_now")
        )
        self._check_button.setEnabled(updates.enabled(self._store))
