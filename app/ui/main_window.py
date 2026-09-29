"""Ana pencere.

Yapı: solda dar ikon şeridi, sağında o an açık olan ekran. Ekranlar arasında
geçiş `QStackedWidget` ile yapılıyor.

Ekranlar:
  journey   — modül kartları ve öğrenme yolu
  topic     — bir bölümün içeriği
  roadmap   — hangi patikanın hangi sırayla çalışılacağı (Rotalar)
  notes     — kullanıcının kendi notları (Notlarım)
  profile   — kullanıcı bilgileri ve istatistikler
  releases  — sürüm notları
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QPoint, QThread, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core import animations
from ..core.catalog import Catalog
from ..widgets import motion
from ..widgets.fade_stack import BACK, FORWARD, FadeStack
from ..core.discord_presence import (
    BUTTON_LABEL,
    PROJECT_URL,
    RELEASES_URL,
    DiscordPresence,
)
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..core.unlock import is_unlocked
from ..core.theme import ThemeManager
from ..paths import content_dir
from ..version import APP_VERSION
from .header import ScreenHeader
from ..widgets.common import HairlineFrame, SegmentedControl
from .about_view import SECTIONS as ABOUT_SECTIONS, AboutView
from .confirm_dialog import ConfirmDialog
from . import titlebar
from ..resources.theme.tokens import RAIL_COLORS, RAIL_WIDTH
from .footer import Footer
from .journey_view import JourneyView
from .notebook_view import NotebookView
from .search_palette import SearchPalette
from ..core.search import SearchItem, build_index, plain
from .profile_view import ProfileView
from .rail import Rail, RailToggle
from .release_view import ReleaseView
from .roadmap_view import RoadmapView
from .settings_dialog import SettingsDialog
from .update_check import StarWorker, UpdateWorker
from .update_notice import UpdateNoticeDialog
from ..core import updates
from .topic_view import TopicView
from ..widgets.toast import ToastData, ToastManager
from ..widgets.confetti import Confetti
from ..resources.logos import logo_key
from ..resources.medals import TIER_ACCENTS, tier_of
from ..resources.theme.tokens import PALETTES, SPACING
from ..widgets.shortcut_panel import ShortcutPanel
from PySide6.QtWidgets import QApplication
from ..core import badges as badge_core
from ..core import github_stars
from ..core.celebration_sound import CelebrationSound


class Screen(QWidget):
    """Başlık şeridi ve içerikten oluşan basit bir ekran kabı."""

    def __init__(self, header: ScreenHeader, body: QWidget, subbar: QWidget | None = None) -> None:
        super().__init__()
        self.header = header
        self.body = body

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header)
        if subbar is not None:
            layout.addWidget(subbar)
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
        # Animasyonlar ayarı ekranlar kurulmadan önce: ilk girişler de ona uyuyor.
        motion.set_enabled(animations.enabled(store))

        # Discord'da "Odyssey kullanıyor" yazısı. Discord kapalıysa ya da
        # kurulu değilse hiçbir şey olmuyor; ayrı bir iş parçacığında
        # dönüyor ve arayüzü hiçbir koşulda bekletmiyor.
        self._presence = DiscordPresence(self._store)
        self._presence_where = ("", "")

        self.resize(1400, 900)
        self.setMinimumSize(1080, 700)

        # Güncelleme için kapanırken çıkış onayı sorulmuyor (`close_for_update`).
        self._closing_for_update = False

        # Klavye kısayollarının listesi; alt şeritteki klavye düğmesi ve F1.
        self._shortcut_panel = ShortcutPanel(language, self)

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

        # Şeridi açıp kapatan tutamak (Ctrl+M). Düzene girmiyor, şeridin
        # kenarının üstünde duruyor; konumu `_place_rail_toggle` veriyor.
        self._central = central
        self._rail_toggle = RailToggle(central)
        self._rail_toggle.clicked.connect(self._toggle_rail)
        self._rail_animation = None
        if store.setting("rail_collapsed", "") == "1":
            self._rail.setFixedWidth(0)
            self._rail.hide()
            self._rail_toggle.set_collapsed(True)

        # İçerik ile telif şeridi alt alta; şerit soldaki ikon şeridinin
        # sağında kalıyor, böylece ikon şeridi tepeden tabana kesintisiz.
        content = QWidget()
        column = QVBoxLayout(content)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)

        self._stack = FadeStack()
        column.addWidget(self._stack, 1)

        self._footer = Footer(language)
        column.addWidget(self._footer)

        row.addWidget(content, 1)
        root.addWidget(body)

        self._build_screens()

        # Bölüm bitince ve rozet kazanılınca sağ altta beliren kartlar. Alt
        # şeridin hemen üstüne diziliyorlar. Pencere ilk kez görünene kadar
        # gelen kartlar bekletiliyor (`_flush_toasts`): açılışta pencere
        # görünmezken ısınma turu dönüyor, kart orada harcanırdı.
        self._toasts = ToastManager(central, self._toast_anchor, lambda: language.t("toast.close"))
        self._toasts.on_activated = self._on_toast
        self._toast_ready = False
        self._pending_toasts: list[ToastData] = []
        # Kartla birlikte kısa bir ses. Aynı anda gelen kartlar (bölüm ve
        # onunla kazanılan rozetler) tek ses çalıyor: türler bu olay turu
        # boyunca toplanıyor, bir sonrakinde çalınıyor (`_play_sound`).
        self._sound = CelebrationSound(store)
        self._sound_kinds: set[str] = set()
        # Açılıştaki biten bölümler; yalnızca bundan sonra bitenler kutlanıyor.
        self._done_sections = badge_core.completed_sections(self._catalog, self._store)

        # Sol alttaki GitHub yıldızı: önce son bilinen sayı, sonra arka planda
        # güncel olanı (`start_update_check` sırasında).
        self._star_worker: StarWorker | None = None
        self._star_checked_at = 0.0
        # Kapanış başladı: yıldız artık sorulmuyor (`closeEvent`).
        self._shutting_down = False
        self._star_timer = QTimer(self)
        self._star_timer.setInterval(github_stars.REFRESH_SEC * 1000)
        self._star_timer.timeout.connect(self._check_stars)

        # Genel arama kutusu: pencerenin üstünde, kapalı başlıyor. Katalogun
        # dizini dil başına bir kez kuruluyor (dosya okuma), notlar ve
        # ekranlar her açılışta tazeleniyor.
        self._search_index: tuple[str, list] = ("", [])
        self._search = SearchPalette(language, self)
        self._search.set_provider(self._search_items, self._search_locked)
        # Bölüm sonuçlarında patika logosu için katalog.
        self._search._delegate.catalog = self._catalog  # noqa: SLF001
        self._search.activated.connect(self._on_search)

        self._install_shortcuts()

        self._footer.shortcuts_clicked.connect(self._toggle_shortcuts)
        self._footer.set_stars(github_stars.cached(self._store))

        language.language_changed.connect(self._on_language_changed)
        theme.theme_changed.connect(self._on_theme_changed)

        # Temayı pencere kendisi uyguluyor; çağıranın hatırlamasına gerek yok.
        self._on_theme_changed(theme.effective_mode)

        self._navigate("journey")
        self._refresh_release_dot()
        self._refresh_progress()
        self.retranslate()

        # Güncelleme denetimi açılışta bir kez, arka planda. Pencere
        # kurulurken başlatılmıyor: ağ yavaşsa açılışı bekletmesin diye
        # `start_update_check` ilk kare çizildikten sonra çağrılıyor.
        self._update_worker: UpdateWorker | None = None
        self._update_startup = False
        # Bulunan son güncelleme; şeritteki duyuruya tıklanınca gereken
        # bilgi burada duruyor.
        self._update_info = None

        self._footer.update_clicked.connect(self._on_footer_update)

        # Uygulama günlerce açık kalabiliyor; o oturumda da üç saatte bir
        # bakılıyor. Zamanlayıcı yalnızca denetimi tetikliyor, kararı yine
        # `updates.should_check` veriyor.
        self._update_timer = QTimer(self)
        self._update_timer.setInterval(updates.CHECK_INTERVAL_SEC * 1000)
        self._update_timer.timeout.connect(self._periodic_update_check)

        # Discord'daki yazı **en sonda** başlatılıyor: metin önce
        # hazırlanıyor, sonra bağlantı kuruluyor. Ters sırada ilk çerçeve
        # boş gidiyor ve kullanıcı bir an "Odyssey" dışında bir şey
        # görmüyordu.
        self._set_presence_location()
        self._presence.start()

    # --- ekranlar ---------------------------------------------------------

    def _build_screens(self) -> None:
        # Öğrenme yolu
        self._journey = JourneyView(self._catalog, self._language, self._store)
        self._journey.section_opened.connect(self._open_section)
        self._journey.view_changed.connect(self._update_headers)
        self._journey_header = ScreenHeader(self._language)
        self._journey_header.back_clicked.connect(self._journey_back)
        # Öğrenme Yolu içinde ekran değişince başlık yeniden belirir (prototip `hIn`).
        self._journey.view_changed.connect(self._journey_header.play_enter)
        # Sekmeli patikanın modül seçicisi (MAT 1 / MAT 2); başka yerde gizli.
        # Bölüm sekmeleri gibi başlığın altında, ortalanmış şeritte (Alican:
        # sağ üstte durmasın).
        self._journey_tabs = SegmentedControl()
        self._journey_tabs.changed.connect(self._on_journey_tab)
        self._journey_subbar = HairlineFrame()
        self._journey_subbar.setProperty("role", "subbar")
        alt = QHBoxLayout(self._journey_subbar)
        alt.setContentsMargins(SPACING["lg"], SPACING["sm"] + 2, SPACING["lg"], SPACING["sm"] + 2)
        alt.addStretch(1)
        alt.addWidget(self._journey_tabs)
        alt.addStretch(1)
        self._journey_subbar.hide()
        self._journey_screen = Screen(self._journey_header, self._journey, self._journey_subbar)

        # Bölüm içeriği (kendi başlığını taşıyor)
        self._topic = TopicView(self._catalog, self._language, self._store)
        self._topic.back_requested.connect(self._topic_back)
        self._topic.progress_changed.connect(self._journey.refresh)
        self._topic.progress_changed.connect(self._refresh_progress)
        self._topic.open_notebook.connect(self._open_note)
        # İlk yazılı not bir rozet koşulu; ilerleme hesabı rozetleri de
        # kaydedip bildirime düşürüyor.
        self._topic.notes_changed.connect(self._refresh_progress)

        # Profil
        self._profile = ProfileView(self._catalog, self._language, self._store)
        self._profile.saved.connect(self._journey.refresh)
        self._profile.saved.connect(self._rail.refresh_avatar)
        self._profile_header = ScreenHeader(self._language)
        self._profile_screen = Screen(self._profile_header, self._profile)

        # Rotalar: hangi patikanın hangi sırayla çalışılacağı. Rota
        # başlıktaki seçiciyle değişiyor, Hakkında'daki sekmeler gibi.
        self._roadmap = RoadmapView(self._catalog, self._language, self._store)
        self._roadmap.track_opened.connect(self._open_track)
        self._roadmap_header = ScreenHeader(self._language)
        self._roadmap_segments = SegmentedControl()
        self._roadmap_segments.set_items(self._roadmap.route_labels())
        self._roadmap_segments.set_current(self._roadmap.route_index, notify=False)
        self._roadmap_segments.changed.connect(self._roadmap.show_index)
        self._roadmap_header.add_widget(self._roadmap_segments)
        self._roadmap_screen = Screen(self._roadmap_header, self._roadmap)

        # Notlarım
        self._notebook = NotebookView(self._catalog, self._language, self._store)
        self._notebook.open_section.connect(self._open_section)
        self._notebook.changed.connect(self._refresh_progress)
        self._notebook_header = ScreenHeader(self._language)
        self._notebook_screen = Screen(self._notebook_header, self._notebook)

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
            self._roadmap_screen,
            self._notebook_screen,
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

        # Notlarım'ın okuma alanı açılışta boş ekranın arkasında duruyor;
        # ilk not seçilince siyah kare görünmesin.
        self._stack.setCurrentWidget(self._notebook_screen)
        self._notebook.warm_up()

        # Genel aramanın dizini de burada, pencere görünmezken kuruluyor.
        self._catalog_index()

        if onceki is not None:
            self._stack.setCurrentWidget(onceki)
        QApplication.processEvents()

    def start_update_check(self) -> None:
        """Açılışta yeni sürüm var mı diye bakar.

        **Her açılışta bir kez**, aradaki süreye bakmadan: programı açıp
        kapatan biri her seferinde güncel bilgiyi görüyor. Süre kuralı
        yalnızca açık kalan oturumun kendi kendine yaptığı denetim için.

        Ayar kapalıysa hiç iş parçacığı kurulmuyor: karar veritabanına
        bakıyor, veritabanına da yalnızca bu iş parçacığından dokunuluyor.
        """
        self._update_timer.start()
        self._run_update_check(startup=True)
        self._star_timer.start()
        self._check_stars()

    def _periodic_update_check(self) -> None:
        """Açık kalan oturumda üç saatte bir."""
        self._run_update_check(startup=False)

    def _run_update_check(self, startup: bool) -> None:
        if self._update_worker is not None and self._update_worker.isRunning():
            return
        if not updates.should_check(self._store, ignore_interval=startup):
            return
        self._update_startup = startup
        self._update_worker = UpdateWorker(parent=self)
        self._update_worker.finished_with.connect(self._on_update_checked)
        self._update_worker.start()

    def _on_update_checked(self, info) -> None:
        """Denetim bitti. Yalnızca **yeni sürüm varsa** bir şey görünüyor.

        Başarısız denetim sessiz: internetin olmaması bu uygulamada bir
        hata değil, olağan durum.
        """
        updates.record(self._store, info)
        if not info.has_update:
            return

        self._update_info = info
        self._footer.set_update(info.version, info.url)

        # Duyuru penceresi sürüm başına bir kez ve yalnızca açılışta:
        # ders okurken ya da sınav çözerken önüne kutu çıkmıyor.
        if not self._update_startup:
            return
        if updates.already_notified(self._store, info.version):
            return
        updates.mark_notified(self._store, info.version)
        self._show_update_notice(info)

    def _on_footer_update(self) -> None:
        """Şeritteki duyuruya tıklandı.

        Kutu **her zaman** açılıyor: "sürüm başına bir kez" kuralı yalnızca
        kendiliğinden çıkan duyuru için. Kullanıcı tıkladıysa görmek
        istiyordur.
        """
        if self._update_info is not None:
            self._show_update_notice(self._update_info)

    def _show_update_notice(self, info) -> None:
        from . import titlebar

        notice = UpdateNoticeDialog(self._language, info, self)
        titlebar.apply(notice, self._theme.effective_mode)
        notice.exec()

    def _refresh_progress(self) -> None:
        """İlerleme değişince yeni biten bölümleri ve rozetleri kutlar.

        Önce şeridin ortasındaki genel ilerleme halkasını da güncelliyordu;
        halka kalktı (aynı yüzde öğrenme yolu ekranında var). Sonra yeni
        rozetler alt şeritteki zile bildirim olarak düşüyordu; zil kalktı,
        şimdi sağ altta o an bir kart çıkıyor.
        """
        simdi = badge_core.completed_sections(self._catalog, self._store)
        yeni_bolumler = simdi - self._done_sections
        self._done_sections = simdi
        for chapter_id, section_id in sorted(yeni_bolumler):
            veri = self._section_toast(chapter_id, section_id)
            if veri is not None:
                self._toast(veri)

        yeniler = badge_core.award_new(
            self._catalog, self._store, content_dir() / "badges.json"
        )
        for tanim in yeniler:
            self._toast(self._badge_toast(tanim))

        # Patikanın tamamı bitti (efsanevi rozet): bir kez konfeti (D2).
        if any(tier_of(t) == "legendary" for t in yeniler):
            self._confetti([t for t in yeniler if tier_of(t) == "legendary"][0])

    def _confetti(self, tanim: dict) -> None:
        p = PALETTES.get(self._theme.effective_mode, PALETTES["dark"])
        renkler = [p["accent"], p["accent_second"], "#FBBF24", "#4ADE80", "#F472B6", "#38BDF8"]
        track_id = {"python-complete": "python", "ml-complete": "machine-learning",
                    "sql-complete": "sql"}.get(tanim.get("id", ""))
        track = self._catalog.track(track_id) if track_id else None
        if track is not None:
            renkler += [track.color, track.color]
        katman = Confetti(self._central, renkler)
        QTimer.singleShot(250, katman.burst)

    # --- kutlama kartları -------------------------------------------------

    def _toast_anchor(self) -> tuple[int, int]:
        """Kartların dizildiği köşe: alt şeridin sağ üst ucunun biraz içi."""
        nokta = self._footer.mapTo(self._central, QPoint(self._footer.width(), 0))
        return nokta.x() - 12, nokta.y() - 8

    def _toast(self, veri: ToastData) -> None:
        if not self._toast_ready:
            self._pending_toasts.append(veri)
            return
        self._toasts.show(veri)
        self._queue_sound(veri.kind)

    def _flush_toasts(self) -> None:
        self._toast_ready = True
        bekleyen, self._pending_toasts = self._pending_toasts, []
        for veri in bekleyen:
            self._toasts.show(veri)
            self._queue_sound(veri.kind)

    def _queue_sound(self, kind: str) -> None:
        if not self._sound_kinds:
            QTimer.singleShot(0, self._play_sound)
        self._sound_kinds.add(kind)

    def _play_sound(self) -> None:
        turler, self._sound_kinds = self._sound_kinds, set()
        self._sound.play("badge" if "badge" in turler else "section")

    def _badge_toast(self, tanim: dict) -> ToastData:
        p = PALETTES.get(self._theme.effective_mode, PALETTES["dark"])
        return ToastData(
            kind="badge",
            eyebrow=self._language.t_upper("toast.badge_eyebrow"),
            title=self._language.pick(tanim.get("title"), tanim.get("id", "")),
            subtitle=self._language.pick(tanim.get("description"), ""),
            icon=tanim.get("icon", "award"),
            color=TIER_ACCENTS.get(tier_of(tanim), (p["accent"],))[0],
            color2=TIER_ACCENTS.get(tier_of(tanim), (p["accent"], p["accent_second"]))[1],
            payload=("badge", tanim.get("id", "")),
            medal=(*(tanim.get("medal") or ["circle", "bronze"])[:2], tanim.get("icon", "star")),
        )

    def _section_toast(self, chapter_id: str, section_id: str) -> ToastData | None:
        chapter = self._catalog.chapter(chapter_id)
        section = self._catalog.section(chapter_id, section_id)
        if chapter is None or section is None:
            return None
        kisa = self._language.pick(chapter.raw.get("short"), "")
        modul = self._language.pick(chapter.title, "")
        return ToastData(
            kind="section",
            eyebrow=self._language.t_upper("toast.section_eyebrow"),
            title=self._language.pick(section.title, section_id),
            subtitle=f"{kisa} · {modul}" if kisa else modul,
            icon=chapter.icon,
            color=chapter.color,
            color2=QColor(chapter.color).lighter(140).name(),
            payload=("section", chapter_id, section_id),
            logo=logo_key(chapter.icon, chapter.id),
        )

    def _on_toast(self, veri: ToastData) -> None:
        """Karta tıklandı: rozette profil açılıyor, bölümde yalnızca kapanıyor."""
        if veri.payload and veri.payload[0] == "badge":
            self._navigate("profile")

    # --- GitHub yıldızı ---------------------------------------------------

    def _check_stars(self) -> None:
        """Yıldız sayısını arka planda sorar.

        Güncelleme denetimi ayarlardan kapatıldıysa hiç sorulmuyor: o ayar
        "program ağa çıkmasın" demek. Son bilinen sayı görünmeye devam ediyor.
        """
        import time

        if self._shutting_down or not updates.enabled(self._store):
            return
        if self._star_worker is not None and self._star_worker.isRunning():
            return
        if time.monotonic() - self._star_checked_at < github_stars.MIN_INTERVAL_SEC and self._star_checked_at:
            return
        self._star_checked_at = time.monotonic()
        self._star_worker = StarWorker(parent=self)
        self._star_worker.finished_with.connect(self._on_stars)
        self._star_worker.start()

    def _on_stars(self, count: int) -> None:
        if count < 0 or self._shutting_down:
            return
        github_stars.remember(self._store, count)
        self._footer.set_stars(count)

    def changeEvent(self, event) -> None:  # noqa: N802
        # Tarayıcıda yıldız verip geri dönen kişi sayıyı hemen güncel görsün.
        if event.type() == QEvent.Type.ActivationChange and self.isActiveWindow() and self._star_timer.isActive():
            self._check_stars()
        super().changeEvent(event)

    def _refresh_release_dot(self) -> None:
        """Şeritteki sürüm notu noktası.

        Nokta süs değil: `CHANGELOG.md`'deki en yeni sürüm, kullanıcının en
        son baktığı sürümden farklıysa çıkıyor.
        """
        latest = self._releases.latest_version()
        seen = self._store.setting("seen_version", "")
        self._rail.set_notification("releases", bool(latest) and latest != seen)

    def _install_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+,"), self, self._open_settings)
        QShortcut(QKeySequence("Ctrl+K"), self, self._search.toggle)
        QShortcut(QKeySequence("Ctrl+M"), self, self._toggle_rail)
        QShortcut(QKeySequence(Qt.Key.Key_F1), self, self._toggle_shortcuts)
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, self._escape)

    def _toggle_shortcuts(self) -> None:
        """Kısayol listesini açar ya da kapatır (klavye düğmesi, F1)."""
        if self._shortcut_panel.isVisible():
            self._shortcut_panel.close()
            return
        self._shortcut_panel.show_above(self._footer.shortcut_button)

    # --- genel arama ------------------------------------------------------

    def _catalog_index(self) -> list[SearchItem]:
        """Katalogun arama dizini; seçili dilde, dil başına bir kez kuruluyor.

        Kurmak ~0,4 sn (bin dosya okunuyor). Açılışta pencere görünmeden
        (`warm_up`) kuruluyor; yoksa ilk `Ctrl+K`'da kutu o kadar
        gecikiyordu. Dil değişince bir sonraki açılışta yeniden.
        """
        dil = self._language.language
        if self._search_index[0] != dil:
            self._search_index = (dil, build_index(self._catalog, dil, self._language.pick))
        return self._search_index[1]

    def _search_items(self) -> list[SearchItem]:
        """Aranabilecek her şey: ekranlar, kullanıcının notları, katalog."""
        t = self._language.t
        katalog = self._catalog_index()

        ekranlar: list[SearchItem] = []
        son = self._store.last_visited()
        if son is not None:
            bolum = self._catalog.section(*son)
            ekranlar.append(
                SearchItem(
                    "screen",
                    t("nav.continue"),
                    self._language.pick(bolum.title) if bolum else "",
                    {"type": "screen", "key": "continue", "icon": "play"},
                )
            )
        for key, simge, anahtar in (
            ("journey", "compass", "nav.path"),
            ("roadmap", "route", "nav.roadmap"),
            ("notes", "notebook", "nav.notes"),
            ("profile", "user", "nav.profile"),
            ("releases", "scroll-text", "nav.releases"),
            ("about", "info", "nav.about"),
            ("settings", "sliders", "settings.title"),
        ):
            ekranlar.append(
                SearchItem("screen", t(anahtar), t("search.go"), {"type": "screen", "key": key, "icon": simge})
            )

        klasorler = {f["id"]: f["name"] for f in self._store.notebook_folders()}
        notlar = []
        for entry in self._store.notebook_entries_with_body():
            chapter = self._catalog.chapter(entry["chapter_id"])
            yer = klasorler.get(entry["folder_id"]) or (
                self._language.pick(chapter.title) if chapter else t("notebook.other")
            )
            notlar.append(
                SearchItem(
                    "note",
                    entry["title"],
                    f"{t('nav.notes')}  ›  {yer}",
                    {"type": "note", "id": entry["id"]},
                    body=plain(entry["body"]),
                )
            )
        # Patikalar (prototip: arama boşken en üstte, "Patika" etiketiyle).
        patikalar = [
            SearchItem("track", self._language.pick(track.title), self._language.pick(track.description),
                       {"type": "track", "track": track.id, "logo": logo_key(track.icon, track.id),
                        "color": track.color})
            for track in self._catalog.tracks if not track.locked
        ]
        return patikalar + ekranlar + notlar + katalog

    def _search_locked(self, target: dict) -> bool:
        """Sonuç kilitli bir bölüme mi götürüyor?"""
        if "chapter" not in target:
            return False
        return not is_unlocked(self._catalog, self._store, target["chapter"], target["section"])

    def _on_search(self, target: dict) -> None:
        """Arama kutusunda seçilen sonuca gider."""
        kind = target.get("type")
        if kind == "screen":
            key = target["key"]
            if key == "continue":
                son = self._store.last_visited()
                if son is not None:
                    self._open_section(*son)
            else:
                self._navigate(key)
            return
        if kind == "note":
            self._open_note(target["id"])
            return
        if kind == "track":
            self._open_track(target["track"])
            return

        self._open_section(target["chapter"], target["section"])
        if self._stack.currentWidget() is not self._topic:
            return
        if kind == "lesson":
            self._topic.focus("lesson", anchor=target.get("anchor", ""))
        elif kind == "course_note":
            self._topic.focus("notes", target.get("document", 0))
        elif kind == "exercise":
            self._topic.focus("exercise", target.get("exercise", 0))

    # --- gezinme ----------------------------------------------------------

    def _navigate(self, key: str) -> None:
        if key == "settings":
            self._open_settings()
            return
        if key == "search":
            self._search.toggle()
            return

        if key == "journey":
            self._journey.show_modules()
            self._stack.slide_to(self._journey_screen)
        elif key == "roadmap":
            # İlerleme bölümlerde değişiyor; rota her gelişte yeniden çiziliyor.
            self._roadmap.refresh(keep_scroll=True, animate=True)
            self._slide_screen(self._roadmap_screen)
        elif key == "notes":
            self._notebook.refresh()
            self._slide_screen(self._notebook_screen)
        elif key == "profile":
            self._profile.refresh()
            self._stack.slide_to(self._profile_screen)
        elif key == "about":
            self._about.refresh()
            self._slide_screen(self._about_screen)
        elif key == "releases":
            self._releases.refresh()
            self._slide_screen(self._releases_screen)
            # Bakıldı: bildirim noktası sönsün ve bir daha çıkmasın.
            self._store.set_setting("seen_version", self._releases.latest_version())
            self._rail.set_notification("releases", False)

        self._rail.set_current(key)
        # Bu geçişlerin hepsi bölümden çıkmak demek; Discord'da bölüm adı
        # kalırsa kullanıcı çoktan başka ekrandayken orada donmuş görünüyor.
        self._set_presence_location()
        self._update_headers()

    def _slide_screen(self, screen) -> None:
        """Belge içeren ekrana geçiş: belge çizilmeye hazır olunca başlıyor."""
        from ..widgets.document_view import when_documents_ready
        self._stack.slide_to(screen, wait=lambda basla: when_documents_ready(screen, basla, 400))

    def _open_section(self, chapter_id: str, section_id: str) -> None:
        # Kilitli bölüm açılmıyor. Yol ekranındaki halka zaten tıklanmıyor;
        # bu kontrol, bölümü başka bir yerden açan bir çağrı eklenirse
        # kilidin arkadan dolanılmamasını sağlıyor.
        if not is_unlocked(self._catalog, self._store, chapter_id, section_id):
            return

        self._topic.show_section(chapter_id, section_id)
        self._set_presence_location(chapter_id, section_id)
        # Geçiş ders sayfası yüklenince oynuyor: bölüm içeriğiyle birlikte
        # kayarak giriyor (prototip `pgFwd`); o ana kadar eski ekranın
        # görüntüsü üstte duruyor.
        self._stack.slide_to(self._topic, FORWARD,
                             wait=lambda basla: self._topic.when_ready(basla, 400))
        self._rail.set_current("journey")

    def _open_track(self, track_id: str) -> None:
        """Rotadaki "Patikaya git": Öğrenme Yolu'nda o patikayı açar."""
        self._navigate("journey")
        self._journey.open_track(track_id)

    def _open_note(self, entry_id: int) -> None:
        """Bölümdeki not panelinden "Notlarım'da aç"."""
        self._navigate("notes")
        self._notebook.open_note(entry_id)

    def _on_presence_changed(self) -> None:
        self._presence.refresh_setting()
        self._refresh_presence()

    def _set_presence_location(
        self, chapter_id: str = "", section_id: str = ""
    ) -> None:
        """Kullanıcının nerede olduğunu kaydeder ve Discord'a yansıtır.

        Argümansız çağrılmak "artık bir bölümde değil" demek. Bu ayrım
        önemli: eskiden konum yalnızca **doluysa** yazılıyordu, dolayısıyla
        bölümden çıkınca eski bölüm saklı kalıyor ve Discord'daki yazı
        orada donuyordu.
        """
        self._presence_where = (chapter_id, section_id)
        self._refresh_presence()

    def _refresh_presence(self) -> None:
        """Saklanan konumu, kullanıcının dilinde metne çevirip gönderir.

        Konumu değiştirmiyor; yalnızca yeniden üretiyor. Dil değişiminde
        `retranslate` buraya geliyor, yoksa Discord'da eski dil kalıyor.
        """
        chapter_id, section_id = self._presence_where

        t = self._language.t
        details = "Odyssey"
        state = t("presence.browsing")

        chapter = self._catalog.chapter(chapter_id) if chapter_id else None
        if chapter is not None:
            details = self._language.pick(chapter.title) or "Odyssey"
            section = (
                self._catalog.section(chapter_id, section_id)
                if section_id
                else None
            )
            if section is not None:
                state = self._language.pick(section.title) or state

        self._presence.set_activity(
            details,
            state,
            large_text=f"Odyssey {APP_VERSION}",
            buttons=[
                # "GitHub" marka adı, çevrilmiyor; "İndir" bir eylem,
                # kullanıcının dilinde yazılıyor.
                {"label": BUTTON_LABEL, "url": PROJECT_URL},
                {"label": t("presence.download"), "url": RELEASES_URL},
            ],
        )

    def _topic_back(self) -> None:
        """Bölümden yola dön; ilerleme değişmiş olabilir, yenile."""
        self._journey.refresh()
        self._stack.slide_to(self._journey_screen, BACK)
        self._update_headers()
        self._set_presence_location()

    def _on_journey_tab(self, index: int) -> None:
        chapters = self._journey.chapter_tabs
        if 0 <= index < len(chapters):
            self._journey.open_module(chapters[index].id)

    def _journey_back(self) -> None:
        """Bir seviye yukarı: yoldan modüllere, modüllerden patikalara."""
        self._journey.back()
        self._update_headers()
        self._set_presence_location()

    def _escape(self) -> None:
        """Kaçış tuşu bir seviye geri gider.

        Arama kutusu açıksa yalnızca onu kapatıyor. Bu kısayol pencere
        genelinde ve kutunun kendi Esc'inden önce yakalıyor; burada
        bakılmasaydı Esc kutuyu kapatmak yerine bölümden çıkarıyordu.
        """
        if self._search.isVisible():
            self._search.close_palette()
            return
        for panel in (self._shortcut_panel,):
            if panel.isVisible():
                panel.close()
                return
        current = self._stack.currentWidget()
        if current is self._topic:
            self._topic_back()
        elif current is self._journey_screen and not self._journey.showing_tracks:
            self._journey_back()

    def _update_headers(self) -> None:
        # Üç katman var: patikalar -> modüller -> yol. Geri düğmesi en üst
        # katman dışında hep görünüyor ve bir seviye yukarı çıkarıyor.
        en_ustte = self._journey.showing_tracks
        # Modül listesi atlanmışsa geri düğmesi doğrudan patikalara dönüyor;
        # "Modüllere dön" yazması, görülmemiş bir ekrana gidecekmiş gibi
        # duruyordu.
        self._journey_header.set_back(
            not en_ustte,
            self._language.t(
                "path.back_tracks" if self._journey.back_goes_to_tracks else "path.back"
            ),
        )

        tabs = self._journey.chapter_tabs
        self._journey_subbar.setVisible(bool(tabs))
        if tabs:
            acik = self._catalog.chapter(self._journey.path.chapter_id)
            self._journey_tabs.set_accent(acik.color if acik else None)
            self._journey_tabs.set_labels([self._language.pick(c.short) for c in tabs])
            ids = [c.id for c in tabs]
            current = self._journey.path.chapter_id
            if current in ids:
                self._journey_tabs.set_current(ids.index(current), notify=False)

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
        self._notebook_header.set_titles(
            self._language.t("nav.notes"), self._language.t("app.title")
        )
        self._roadmap_header.set_titles(
            self._language.t("nav.roadmap"), self._language.t("app.title")
        )
        self._roadmap_segments.set_labels(self._roadmap.route_labels())
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
        # Discord ayarı da anında uygulanıyor: kapatıldığında yazı hemen
        # siliniyor, açıldığında hemen görünüyor. Ayarın etkisini görmek
        # için uygulamayı kapatıp açmak gerekmiyor.
        dialog.presence_changed.connect(self._on_presence_changed)
        # Animasyonlar ayarı da anında: döngüsel hareketler hemen duruyor.
        dialog.animations_changed.connect(motion.set_enabled)
        # Elle denetim yapıldıysa sonucu şeride de yansıt.
        dialog.update_found.connect(self._on_update_checked)
        # Ayarlardan "Güncelle" denince kutu açılıyor: kullanıcı orada
        # güncelleme olduğunu öğrenip hiçbir şey yapamıyordu.
        dialog.update_requested.connect(self._show_update_notice)
        dialog.exec()

        # Seçimler kalıcı olsun diye veritabanına yazılıyor.
        self._store.set_setting("language", self._language.language)
        self._store.set_setting("theme", self._theme.mode)

        # Pencere kapandı: dil bağı koparılıyor ve pencere siliniyor. Yoksa
        # her açılışta bir pencere daha birikiyor ve hepsi her dil
        # değişiminde boş yere yeniden çevriliyordu (ölçüldü: iki açılışta
        # iki pencere yaşıyordu). Süren işçileri pencere kendisi devrediyor.
        try:
            self._language.language_changed.disconnect(dialog.retranslate)
        except (RuntimeError, TypeError):
            pass
        dialog.deleteLater()

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
            ("roadmap", self._roadmap_header),
            ("notes", self._notebook_header),
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
        self._rail_toggle.set_mode(mode)
        self._stack.set_background(PALETTES[mode]["bg"])
        self._journey.set_mode(mode)
        self._journey_header.set_mode(mode)
        self._topic.set_mode(mode)
        self._roadmap.set_mode(mode)
        self._roadmap_header.set_mode(mode)
        self._notebook.set_mode(mode)
        self._notebook_header.set_mode(mode)
        self._profile.set_mode(mode)
        self._profile_header.set_mode(mode)
        self._about.set_mode(mode)
        self._about_header.set_mode(mode)
        self._releases.set_mode(mode)
        self._releases_header.set_mode(mode)
        self._footer.set_mode(mode)
        self._toasts.set_mode(mode)
        self._shortcut_panel.set_mode(mode)
        self._search.set_mode(mode)
        self._apply_header_accents(mode)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("app.title"))
        self._rail.retranslate()
        self._rail_toggle.setToolTip(f"{self._language.t('nav.toggle_menu')}  (Ctrl+M)")
        self._refresh_progress()
        self._footer.retranslate()
        self._journey.retranslate()
        self._topic.retranslate()
        self._roadmap.retranslate()
        self._notebook.retranslate()
        self._profile.retranslate()
        self._about.retranslate()
        self._releases.retranslate()
        self._search.retranslate()
        self._shortcut_panel.retranslate()
        self._update_headers()
        # Discord'daki yazı da kullanıcının dilinde; `retranslate` onu
        # yeniden üretmezse orada eski dil kalıyor.
        self._refresh_presence()

    # --- sol şerit: aç / kapat -------------------------------------------

    def _toggle_rail(self) -> None:
        """Sol şeridi kısa bir kaymayla gizler ya da gösterir; durum saklanıyor."""
        from PySide6.QtCore import QEasingCurve, QVariantAnimation

        kapanacak = self._rail.isVisible() and self._rail.width() > 0
        self._store.set_setting("rail_collapsed", "1" if kapanacak else "")
        self._rail_toggle.set_collapsed(kapanacak)
        if not kapanacak:
            self._rail.show()

        if self._rail_animation is not None:
            self._rail_animation.stop()
        anim = QVariantAnimation(self)
        anim.setDuration(180)
        anim.setStartValue(self._rail.width() if self._rail.isVisible() else 0)
        anim.setEndValue(0 if kapanacak else RAIL_WIDTH)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        def adim(value) -> None:
            self._rail.setFixedWidth(int(value))
            self._place_rail_toggle()

        def bitti() -> None:
            if kapanacak:
                # Gizli şeridin düğmeleri Tab ile odak almasın.
                self._rail.hide()
            self._place_rail_toggle()

        anim.valueChanged.connect(adim)
        anim.finished.connect(bitti)
        anim.start()
        self._rail_animation = anim

    def _place_rail_toggle(self) -> None:
        """Tutamağı şeridin sağ kenarının ortasına (kapalıyken pencere
        kenarına) yerleştirir."""
        toggle = self._rail_toggle
        # Menü panelinin sağ kenarına oturuyor (panel şeridin içinde, kenardan içeride).
        genislik = self._rail.dock_right() if self._rail.isVisible() and self._rail.width() > 0 else 0
        x = max(0, genislik - toggle.width() // 2)
        # Dikeyde arama simgesinin tam ortasına hizalı: şeridin ortasına
        # göre konunca simgeden birkaç piksel kayık ve orantısız duruyordu.
        # Şerit gizliyken son bilinen hiza kullanılıyor.
        if self._rail.isVisible() and self._rail.height() > 0:
            dugme = self._rail.anchor_button()
            merkez = dugme.mapTo(self._central, dugme.rect().center()).y()
            self._rail_toggle_center = merkez
        merkez = getattr(self, "_rail_toggle_center", None)
        if merkez is None:
            ust = self._rail.mapTo(self._central, self._rail.rect().topLeft()).y()
            merkez = ust + (self._rail.height() or self._central.height()) // 2
        toggle.move(x, round(merkez - toggle.height() / 2))
        toggle.raise_()

    def showEvent(self, event) -> None:  # noqa: N802
        super().showEvent(event)
        self._place_rail_toggle()
        if not self._toast_ready:
            # Açılış animasyonu bitsin, sonra bekleyen kartlar gelsin.
            QTimer.singleShot(1200, self._flush_toasts)
        if not getattr(self, "_warmed", False):
            self._warmed = True
            QTimer.singleShot(1500, self._warm_documents)

    def _warm_documents(self) -> None:
        """Henüz hiç sayfa yüklememiş belge alanlarına boş sayfa yükler.

        Bir belge alanının **ilk** yüklemesi 620 ms sürüyordu (tarayıcı
        tarafı ilk kez kuruluyor), sonrakiler ~90 ms (ölçüldü). Bölüme ilk
        girişte ders sayfası geç geliyor, ekran boş kayıyordu. Açılıştan
        sonra boşta, birer birer ısıtılıyor.
        """
        from ..widgets.document_view import DocumentView

        belgeler = [d for d in self.findChildren(DocumentView) if not getattr(d, "_body", "")]

        def sirayla(kalan=belgeler) -> None:
            if not kalan:
                return
            belge = kalan.pop(0)
            if not getattr(belge, "_body", ""):
                belge.setHtml("<!doctype html><html><body></body></html>")
            QTimer.singleShot(120, self, lambda: sirayla(kalan))

        sirayla()

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._place_rail_toggle()
        # Üstte duran katmanlar pencerenin tamamını kaplıyor; pencereyle
        # birlikte büyüyorlar.
        if self._search.isVisible():
            self._search.setGeometry(self.rect())
        self._shortcut_panel.reposition()
        self._toasts.reposition()

    def close_for_update(self) -> None:
        """Güncelleme yardımcısına yer açmak için onay sormadan kapanır.

        `QApplication.quit()` Qt 6'da önce pencereleri kapatmaya çalışıyor,
        bu da çıkış onayını açıyordu. Kutu "güncelleniyor" penceresinin
        arkasında kalıyor ve fark edilmiyordu; yardımcı ise uygulamanın
        kapanmasını en fazla 60 saniye bekleyip vazgeçiyor. Kullanıcı
        "Güncelle"ye basarak kapanmayı zaten kabul etti, ikinci kez
        sorulmuyor.
        """
        self._closing_for_update = True
        QApplication.quit()

    def closeEvent(self, event) -> None:  # noqa: N802
        """Kapatmadan önce onay sorar, sonra veritabanını kapatır.

        Uygulama uzun süre açık kalıyor; kapatma düğmesine yanlışlıkla
        basmak, okunan yerin kaybolması demek. Kutu, verinin kaydedildiğini
        de söylüyor — asıl merak edilen o.
        """
        if not self._closing_for_update:
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

        # Yıldız denetimi burada kesiliyor. Çıkış onayı kapanınca pencere
        # yeniden etkin oluyor ve `changeEvent` yıldızı soruyordu; kapanışın
        # sonunda veritabanı kapatıldıktan sonra da bir etkinleşme geliyor ve
        # ayar okuması "Cannot operate on a closed database" veriyordu
        # (Alican, 25 Eylül). Yolda olan bir cevap da artık yazılmıyor.
        self._shutting_down = True
        self._star_timer.stop()

        # Notta yazılıp henüz kaydedilmemiş son harfler (Notlarım ve
        # bölümdeki not paneli).
        self._notebook.flush()
        self._topic.flush_note()

        # Discord'daki yazı silinsin; yoksa kapatılan uygulama hâlâ
        # kullanılıyor gibi görünüyor.
        self._presence.stop()
        self._wait_for_workers()
        self._store.close()
        super().closeEvent(event)

    def _wait_for_workers(self) -> None:
        """Kapanmadan önce arka plan işlerinin bitmesini kısa süre bekler.

        Güncelleme denetimi (en fazla `updates.TIMEOUT_SEC`) ya da çalışan
        bir alıştırma bitmeden pencere yok edilince Qt "QThread: Destroyed
        while thread is still running" uyarısı veriyor ve süreç çökebiliyor
        (Alican bildirdi). Pencere önce gizleniyor: kişi beklemeyi görmüyor.
        """
        running = [t for t in self.findChildren(QThread) if t.isRunning()]
        if not running:
            return
        self.hide()
        QApplication.processEvents()
        limit_ms = (updates.TIMEOUT_SEC + 1) * 1000
        for thread in running:
            thread.requestInterruption()
            thread.wait(limit_ms)
