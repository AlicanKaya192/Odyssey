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

from PySide6.QtCore import QThread, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..core.catalog import Catalog
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
from ..widgets.common import SegmentedControl
from .about_view import SECTIONS as ABOUT_SECTIONS, AboutView
from .confirm_dialog import ConfirmDialog
from . import titlebar
from ..resources.theme.tokens import RAIL_COLORS
from .footer import Footer
from .journey_view import JourneyView
from .notebook_view import NotebookView
from .search_palette import SearchPalette
from ..core.search import SearchItem, build_index, plain
from .profile_view import ProfileView
from .rail import Rail
from .release_view import ReleaseView
from .roadmap_view import RoadmapView
from .settings_dialog import SettingsDialog
from .update_check import UpdateWorker
from .update_notice import UpdateNoticeDialog
from ..core import updates
from .topic_view import TopicView
from ..widgets.notification_panel import NotificationPanel
from ..widgets.shortcut_panel import ShortcutPanel
from PySide6.QtWidgets import QApplication
from ..core import badges as badge_core


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

        # Discord'da "Odyssey kullanıyor" yazısı. Discord kapalıysa ya da
        # kurulu değilse hiçbir şey olmuyor; ayrı bir iş parçacığında
        # dönüyor ve arayüzü hiçbir koşulda bekletmiyor.
        self._presence = DiscordPresence(self._store)
        self._presence_where = ("", "")

        self.resize(1400, 900)
        self.setMinimumSize(1080, 700)

        # Güncelleme için kapanırken çıkış onayı sorulmuyor (`close_for_update`).
        self._closing_for_update = False

        # Bildirim paneli: alt şeritteki zile basınca yukarı doğru açılıyor.
        self._notif_panel = NotificationPanel(self)
        self._notif_panel.cleared.connect(self._on_notifications_cleared)
        self._notif_panel.notification_read.connect(self._on_notification_read)

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

        # Genel arama kutusu: pencerenin üstünde, kapalı başlıyor. Katalogun
        # dizini dil başına bir kez kuruluyor (dosya okuma), notlar ve
        # ekranlar her açılışta tazeleniyor.
        self._search_index: tuple[str, list] = ("", [])
        self._search = SearchPalette(language, self)
        self._search.set_provider(self._search_items, self._search_locked)
        self._search.activated.connect(self._on_search)

        self._install_shortcuts()

        self._footer.bell_button.clicked.connect(self._toggle_notification_panel)
        self._footer.shortcuts_clicked.connect(self._toggle_shortcuts)

        language.language_changed.connect(self._on_language_changed)
        theme.theme_changed.connect(self._on_theme_changed)

        # Temayı pencere kendisi uyguluyor; çağıranın hatırlamasına gerek yok.
        self._on_theme_changed(theme.effective_mode)

        self._navigate("journey")
        self._refresh_notifications()
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
        # Sekmeli patikanın modül seçicisi (MAT 1 / MAT 2); başka yerde gizli.
        self._journey_tabs = SegmentedControl()
        self._journey_tabs.changed.connect(self._on_journey_tab)
        self._journey_tabs.hide()
        self._journey_header.add_widget(self._journey_tabs)
        self._journey_screen = Screen(self._journey_header, self._journey)

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
        """İlerleme değişince yeni kazanılan rozetleri kaydeder.

        Önce şeridin ortasındaki genel ilerleme halkasını da güncelliyordu;
        halka kalktı (aynı yüzde öğrenme yolu ekranında var).
        """
        # Yeni kazanılan rozetler burada kaydedilip bildirime düşüyor.
        # Önce yalnızca profil ekranı kaydediyordu; bildirim ancak profile
        # bakınca geliyordu. Metin değil kimlik saklanıyor: bildirim
        # gösterildiği anda seçili dilde yazılıyor.
        yeniler = badge_core.award_new(
            self._catalog, self._store, content_dir() / "badges.json"
        )
        for tanim in yeniler:
            self._store.add_notification(
                kind="badge",
                title_key=tanim.get("id", ""),
                icon=tanim.get("icon", ""),
            )
        if yeniler:
            self._refresh_notifications()

    def _refresh_notifications(self) -> None:
        """Zilin üstündeki sayı ve şeritteki sürüm notu noktası.

        Nokta süs değil: `CHANGELOG.md`'deki en yeni sürüm, kullanıcının en
        son baktığı sürümden farklıysa çıkıyor.
        """
        self._footer.set_unread_count(self._store.unread_notification_count())

        latest = self._releases.latest_version()
        seen = self._store.setting("seen_version", "")
        self._rail.set_notification("releases", bool(latest) and latest != seen)

    def _toggle_notification_panel(self) -> None:
        if self._notif_panel.isVisible():
            self._notif_panel.close()
        else:
            self._show_notification_panel()

    def _show_notification_panel(self) -> None:
        tanimlar = {
            t.get("id", ""): t
            for t in badge_core.load_definitions(content_dir() / "badges.json")
        }
        notifs = []
        for n in self._store.all_notifications():
            n = dict(n)
            tanim = tanimlar.get(n["title_key"]) if n["kind"] == "badge" else None
            if tanim is not None:
                ad = self._language.pick(tanim.get("title"), n["title_key"])
                n["text"] = self._language.t("notification.badge", name=ad)
            else:
                # Tanımı olmayan (silinmiş ya da eski) bir kayıt: olduğu gibi.
                n["text"] = n["title_key"]
            notifs.append(n)
        self._notif_panel.populate(
            notifs,
            self._language.t("notification.title"),
            self._language.t("notification.clear"),
            self._language.t("notification.empty"),
            self._language.t("notification.mark_read"),
        )
        self._notif_panel.show_above(self._footer.bell_button)

    def _on_notification_read(self, notif_id: int) -> None:
        self._store.mark_notification_read(notif_id)
        self._refresh_notifications()
        if self._notif_panel.isVisible():
            self._show_notification_panel()

    def _on_notifications_cleared(self) -> None:
        self._store.clear_notifications()
        self._refresh_notifications()

    def _install_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+,"), self, self._open_settings)
        QShortcut(QKeySequence("Ctrl+K"), self, self._search.toggle)
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
            ("journey", "home", "nav.path"),
            ("roadmap", "route", "nav.roadmap"),
            ("notes", "notebook", "nav.notes"),
            ("profile", "user", "nav.profile"),
            ("releases", "megaphone", "nav.releases"),
            ("about", "info", "nav.about"),
            ("settings", "settings", "settings.title"),
        ):
            ekranlar.append(
                SearchItem("screen", t(anahtar), "", {"type": "screen", "key": key, "icon": simge})
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
        return ekranlar + notlar + katalog

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
            self._stack.setCurrentWidget(self._journey_screen)
        elif key == "roadmap":
            # İlerleme bölümlerde değişiyor; rota her gelişte yeniden çiziliyor.
            self._roadmap.refresh(keep_scroll=True)
            self._stack.setCurrentWidget(self._roadmap_screen)
        elif key == "notes":
            self._notebook.refresh()
            self._stack.setCurrentWidget(self._notebook_screen)
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
        # Bu geçişlerin hepsi bölümden çıkmak demek; Discord'da bölüm adı
        # kalırsa kullanıcı çoktan başka ekrandayken orada donmuş görünüyor.
        self._set_presence_location()
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
        self._set_presence_location(chapter_id, section_id)

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
        self._stack.setCurrentWidget(self._journey_screen)
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
        for panel in (self._shortcut_panel, self._notif_panel):
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
        self._journey_tabs.setVisible(bool(tabs))
        if tabs:
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
        self._notif_panel.set_mode(mode)
        self._shortcut_panel.set_mode(mode)
        self._search.set_mode(mode)
        self._apply_header_accents(mode)

    def retranslate(self) -> None:
        self.setWindowTitle(self._language.t("app.title"))
        self._rail.retranslate()
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

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        # Üstte duran katmanlar pencerenin tamamını kaplıyor; pencereyle
        # birlikte büyüyorlar.
        if self._search.isVisible():
            self._search.setGeometry(self.rect())
        self._shortcut_panel.reposition()
        self._notif_panel.reposition()

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
