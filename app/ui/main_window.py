"""Ana pencere.

Yapı: solda dar ikon şeridi, sağında o an açık olan ekran. Ekranlar arasında
geçiş `QStackedWidget` ile yapılıyor.

Ekranlar:
  journey   — modül kartları ve öğrenme yolu
  topic     — bir bölümün içeriği
  profile   — kullanıcı bilgileri ve istatistikler
  releases  — sürüm notları
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.unlock import is_unlocked
from ..core.theme import ThemeManager
from ..paths import content_dir
from .header import ScreenHeader
from ..widgets.common import SegmentedControl
from .about_view import SECTIONS as ABOUT_SECTIONS, AboutView
from .confirm_dialog import ConfirmDialog
from . import titlebar
from ..resources.theme.tokens import RAIL_COLORS
from .footer import Footer
from .journey_view import JourneyView
from .profile_view import ProfileView
from .rail import Rail
from .release_view import ReleaseView
from .settings_dialog import SettingsDialog
from .topic_view import TopicView


class Screen(QWidget):
    """Başlık şeridi ve içerikten oluşan basit bir ekran kabı."""

    def __init__(self, header: ScreenHeader, body: QWidget) -> None:
        super().__init__()
        self.header = header
        self.body = body

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header)
        layout.addWidget(body, 1)


class MainWindow(QMainWindow):
    """Uygulamanın ana penceresi."""

    def __init__(
        self,
        language: LanguageManager,
        theme: ThemeManager,
        store: ProgressStore,
    ) -> None:
        super().__init__()
        self._language = language
        self._theme = theme
        self._store = store
        self._catalog = Catalog.load(content_dir())

        self.resize(1400, 900)
        self.setMinimumSize(1080, 700)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        body = QWidget()
        from PySide6.QtWidgets import QHBoxLayout

        row = QHBoxLayout(body)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self._rail = Rail(language)
        self._rail.navigate.connect(self._navigate)
        row.addWidget(self._rail)

        # İçerik ile telif şeridi alt alta; şerit soldaki ikon şeridinin
        # sağında kalıyor, böylece ikon şeridi tepeden tabana kesintisiz.
        content = QWidget()
        column = QVBoxLayout(content)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)

        self._stack = QStackedWidget()
        column.addWidget(self._stack, 1)

        self._footer = Footer(language)
        column.addWidget(self._footer)

        row.addWidget(content, 1)
        root.addWidget(body)

        self._build_screens()
        self._install_shortcuts()

        language.language_changed.connect(self._on_language_changed)
        theme.theme_changed.connect(self._on_theme_changed)

        # Temayı pencere kendisi uyguluyor; çağıranın hatırlamasına gerek yok.
        self._on_theme_changed(theme.effective_mode)

        self._navigate("journey")
        self._refresh_notifications()
        self._refresh_progress()
        self.retranslate()

    # --- ekranlar ---------------------------------------------------------

    def _build_screens(self) -> None:
        # Öğrenme yolu
        self._journey = JourneyView(self._catalog, self._language, self._store)
        self._journey.section_opened.connect(self._open_section)
        self._journey.view_changed.connect(self._update_headers)
        self._journey_header = ScreenHeader(self._language)
        self._journey_header.back_clicked.connect(self._journey_back)
        self._journey_screen = Screen(self._journey_header, self._journey)

        # Bölüm içeriği (kendi başlığını taşıyor)
        self._topic = TopicView(self._catalog, self._language, self._store)
        self._topic.back_requested.connect(self._topic_back)
        self._topic.progress_changed.connect(self._journey.refresh)
        self._topic.progress_changed.connect(self._refresh_progress)

        # Profil
        self._profile = ProfileView(self._catalog, self._language, self._store)
        self._profile.saved.connect(self._journey.refresh)
        self._profile.saved.connect(self._rail.refresh_avatar)
        self._profile_header = ScreenHeader(self._language)
        self._profile_screen = Screen(self._profile_header, self._profile)

        # Hakkında: Bilgi, SSS, Bağlantılarım, Ekstra İçerikler ve Lisans
        # tek ekranda, başlıktaki sekmelerle.
        self._about = AboutView(self._language)
        self._about_header = ScreenHeader(self._language)
        self._about_segments = SegmentedControl()
        self._about_segments.changed.connect(self._about.show_index)
        self._about.section_changed.connect(lambda _: self._update_headers())
        self._about_header.add_widget(self._about_segments)
        self._about_screen = Screen(self._about_header, self._about)

        # Sürüm notları
        self._releases = ReleaseView(self._language)
        self._releases_header = ScreenHeader(self._language)
        self._releases_screen = Screen(self._releases_header, self._releases)

        for widget in (
            self._journey_screen,
            self._topic,
            self._profile_screen,
            self._about_screen,
            self._releases_screen,
        ):
            self._stack.addWidget(widget)

    def warm_up(self) -> None:
        """Bütün ekranları bir kez çizdirir.

        Belge alanları Chromium ile çiziliyor ve her biri **ilk kez
        gösterildiğinde** yüzeyi hazırlanana kadar siyah kalıyor. Ölçüldü:
        ana ekrandan Hakkında'ya geçişte 48 ms boyunca ekran tamamen
        siyahtı (ortalama parlaklık 0), sonra sayfa geliyordu.

        Sayfanın zemin rengini vermek çözmüyor; o siyahlık Chromium'un ilk
        karesinden **önceki** yüzeyin kendisi. Tek çare o ilk kareyi
        kullanıcı görmeden çizdirmek.

        Bu tur, pencere opaklığı sıfırken (yani görünmezken) çalışıyor;
        `app/main.py` içindeki açılış akışına bak.
        """
        from PySide6.QtWidgets import QApplication

        onceki = self._stack.currentWidget()

        for index in range(self._stack.count()):
            self._stack.setCurrentIndex(index)
            QApplication.processEvents()

        # Konu ekranı kendi içinde birden fazla belge alanı taşıyor.
        self._stack.setCurrentWidget(self._topic)
        self._topic.warm_up()

        if onceki is not None:
            self._stack.setCurrentWidget(onceki)
        QApplication.processEvents()

    def _refresh_progress(self) -> None:
        """Şeridin tepesindeki halkayı günceller.

        Tamamlanmış bölüm sayısının toplam bölüme oranı. Profil ekranındaki
        "Genel ilerleme" ile aynı hesap; ikisi ayrışmasın diye aynı ölçüt
        kullanılıyor: bölüm, sınavı ve alıştırmaları bitince tamamlanmış
        sayılıyor.
        """
        toplam = 0
        biten = 0
        for chapter in self._catalog.chapters:
            for section in chapter.sections:
                toplam += 1
                state = self._store.section_state(
                    chapter.id, section.id, len(section.exercises)
                )
                durum = state.status(section.requires_quiz, section.requires_exercises)
                if durum == "completed":
                    biten += 1

        self._rail.set_progress(round(biten * 100 / toplam) if toplam else 0)

    def _refresh_notifications(self) -> None:
        """Okunmamış sürüm notu varsa şeritte nokta gösterir.

        Nokta süs değil: `CHANGELOG.md`'deki en yeni sürüm, kullanıcının en
        son baktığı sürümden farklıysa çıkıyor.
        """
        latest = self._releases.latest_version()
        seen = self._store.setting("seen_version", "")
        self._rail.set_notification("releases", bool(latest) and latest != seen)

    def _install_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+,"), self, self._open_settings)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self._escape)

    # --- gezinme ----------------------------------------------------------

    def _navigate(self, key: str) -> None:
        if key == "settings":
            self._open_settings()
            return

        if key == "journey":
            self._journey.show_modules()
            self._stack.setCurrentWidget(self._journey_screen)
        elif key == "profile":
            self._profile.refresh()
            self._stack.setCurrentWidget(self._profile_screen)
        elif key == "about":
            self._about.refresh()
            self._stack.setCurrentWidget(self._about_screen)
        elif key == "releases":
            self._releases.refresh()
            self._stack.setCurrentWidget(self._releases_screen)
            # Bakıldı: bildirim noktası sönsün ve bir daha çıkmasın.
            self._store.set_setting("seen_version", self._releases.latest_version())
            self._rail.set_notification("releases", False)

        self._rail.set_current(key)
        self._update_headers()

    def _open_section(self, chapter_id: str, section_id: str) -> None:
        # Kilitli bölüm açılmıyor. Yol ekranındaki halka zaten tıklanmıyor;
        # bu kontrol, bölümü başka bir yerden açan bir çağrı eklenirse
        # kilidin arkadan dolanılmamasını sağlıyor.
        if not is_unlocked(self._catalog, self._store, chapter_id, section_id):
            return

        self._topic.show_section(chapter_id, section_id)
        self._stack.setCurrentWidget(self._topic)
        self._rail.set_current("journey")

    def _topic_back(self) -> None:
        """Bölümden yola dön; ilerleme değişmiş olabilir, yenile."""
        self._journey.refresh()
        self._stack.setCurrentWidget(self._journey_screen)
        self._update_headers()

    def _journey_back(self) -> None:
        """Bir seviye yukarı: yoldan modüllere, modüllerden patikalara."""
        self._journey.back()
        self._update_headers()

    def _escape(self) -> None:
        """Kaçış tuşu bir seviye geri gider."""
        current = self._stack.currentWidget()
        if current is self._topic:
            self._topic_back()
        elif current is self._journey_screen and not self._journey.showing_tracks:
            self._journey_back()

    def _update_headers(self) -> None:
        # Üç katman var: patikalar -> modüller -> yol. Geri düğmesi en üst
        # katman dışında hep görünüyor ve bir seviye yukarı çıkarıyor.
        en_ustte = self._journey.showing_tracks
        self._journey_header.set_back(
            not en_ustte, self._language.t("path.back")
        )

        if self._journey.showing_path:
            # Yoldayken başlık modülün adını göstersin; "Öğrenme Yolu" yazmak
            # kullanıcıya hangi modülde olduğunu söylemiyor.
            chapter = self._catalog.chapter(self._journey.path.chapter_id)
            self._journey_header.set_titles(
                self._language.pick(chapter.title) if chapter else "",
                self._language.t("nav.path"),
            )
        elif not en_ustte:
            # Modül listesindeyken patikanın adı yazıyor.
            self._journey_header.set_titles(
                self._language.pick(self._journey.track_title),
                self._language.t("nav.path"),
            )
        else:
            self._journey_header.set_titles(
                self._language.t("nav.path"), self._language.t("app.title")
            )
        self._profile_header.set_titles(
            self._language.t("profile.title"), self._language.t("app.title")
        )
        # Başlıkta ekranın adı sabit; hangi sekmede olduğumuzu sağdaki
        # seçici zaten gösteriyor.
        self._about_header.set_titles(
            self._language.t("nav.about"), self._language.t("app.title")
        )
        # `set_labels` seçimi bozmadan yalnızca metinleri değiştiriyor;
        # `notify=False` ise seçiciyi güncellemenin tekrar bu metodu
        # çağırmasını engelliyor.
        self._about_segments.set_labels(
            [self._language.t(f"nav.{name}") for name in ABOUT_SECTIONS]
        )
        self._about_segments.set_current(self._about.section_index, notify=False)
        self._apply_header_accents(self._theme.effective_mode)
        self._releases_header.set_titles(
            self._language.t("release.title"), self._language.t("app.title")
        )

    # --- ayarlar ----------------------------------------------------------

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self._language, self._theme, self._store, self)
        self._language.language_changed.connect(dialog.retranslate)
        # Kilit ayarı değişir değişmez ekranlar yenileniyor: yol ekranındaki
        # halkalar ve açık bölümün alt gezinme düğmeleri o an güncelleniyor.
        dialog.lock_changed.connect(self._on_lock_changed)
        # Süre ayarı da aynı şekilde: açık bir sınav varsa sayaç o an
        # duruyor ya da geri geliyor.
        dialog.timing_changed.connect(self._on_timing_changed)
        dialog.exec()

        # Seçimler kalıcı olsun diye veritabanına yazılıyor.
        self._store.set_setting("language", self._language.language)
        self._store.set_setting("theme", self._theme.mode)

    def _on_lock_changed(self) -> None:
        """Kilit ayarı değişti; kilide bakan her ekran yenileniyor."""
        self._journey.refresh()
        self._topic.refresh_navigation()

    def _on_timing_changed(self) -> None:
        """Sınav süresi ayarı değişti; açık sınav o an güncelleniyor."""
        self._topic.refresh_quiz_timing()

    # --- olaylar ----------------------------------------------------------

    def _on_language_changed(self, _code: str) -> None:
        self.retranslate()

    def _apply_header_accents(self, mode: str) -> None:
        """Her başlığa şeritteki simgesiyle aynı rengi verir.

        Ekranlar arasında gezerken aynı rengin devam etmesi, nerede
        olunduğunu yazıdan önce renkten okutuyor.
        """
        colors = RAIL_COLORS.get(mode, RAIL_COLORS["light"])
        for key, header in (
            ("journey", self._journey_header),
            ("profile", self._profile_header),
            ("releases", self._releases_header),
        ):
            header.set_accent(colors[key])

        self._about_header.set_accent(colors["about"])
        self._topic.header.set_accent(colors["journey"])

    def _on_theme_changed(self, mode: str) -> None:
        # Windows başlık çubuğu Qt'nin dışında kalıyor; koyu temada pencere
        # koyu, çubuk açık kalıp ekran ikiye bölünmüş gibi duruyordu.
        titlebar.apply(self, mode)

        self._rail.set_mode(mode)
        self._journey.set_mode(mode)
        self._journey_header.set_mode(mode)
        self._topic.set_mode(mode)
        self._profile.set_mode(mode)
        self._profile_header.set_mode(mode)
        self._about.set_mode(mode)
        self._about_header.set_mode(mode)
        self._releases.set_mode(mode)
        self._releases_header.set_mode(mode)
        self._apply_header_accents(mode)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("app.title"))
        self._rail.retranslate()
        self._refresh_progress()
        self._footer.retranslate()
        self._journey.retranslate()
        self._topic.retranslate()
        self._profile.retranslate()
        self._about.retranslate()
        self._releases.retranslate()
        self._update_headers()

    def closeEvent(self, event) -> None:  # noqa: N802
        """Kapatmadan önce onay sorar, sonra veritabanını kapatır.

        Uygulama uzun süre açık kalıyor; kapatma düğmesine yanlışlıkla
        basmak, okunan yerin kaybolması demek. Kutu, verinin kaydedildiğini
        de söylüyor — asıl merak edilen o.
        """
        dialog = ConfirmDialog(
            self._language.t("quit.title"),
            self._language.t("quit.message"),
            self._language.t("quit.confirm"),
            self._language.t("quit.cancel"),
            self,
        )
        # Ayrı pencerelerin başlık çubuğu da temaya uysun.
        titlebar.apply(dialog, self._theme.effective_mode)

        if dialog.exec() != ConfirmDialog.DialogCode.Accepted:
            event.ignore()
            return

        self._store.close()
        super().closeEvent(event)
