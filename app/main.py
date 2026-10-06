"""Odyssey — uygulamanın giriş noktası.

Çalıştırmak için:
    .venv\\Scripts\\python app\\main.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Doğrudan `python app/main.py` ile çalıştırıldığında proje kökü içe aktarma
# yolunda olmuyor; bunu elle ekliyoruz.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.language import (  # noqa: E402
    AVAILABLE_LANGUAGES,
    LanguageManager,
    system_language,
)
from app.core.theme import ThemeManager  # noqa: E402
from app.core.runner import HARNESS_FLAG  # noqa: E402
from app.version import APP_VERSION  # noqa: E402

MIN_PYTHON = (3, 10)


def _run_harness_if_asked() -> bool:
    """Uygulama denetleyici olarak mı çağrıldı?

    Paketlenmiş `.exe` içinde ayrı bir `python.exe` yok. Alıştırma kodunu
    ayrı bir süreçte çalıştırmak için uygulama kendini `--run-harness`
    bayrağıyla çağırıyor; bu durumda arayüz hiç kurulmadan `sandbox/harness.py`
    çalıştırılıyor.

    Çalıştırıldıysa True döner ve program orada biter.
    """
    if len(sys.argv) < 3 or sys.argv[1] != HARNESS_FLAG:
        return False

    from app.paths import sandbox_dir

    harness = sandbox_dir() / "harness.py"
    source = harness.read_text(encoding="utf-8")

    # Denetleyici tek başına ayakta duran bir script; kendi `main()`'ini
    # çalıştırması için argümanları onun beklediği hâle getiriyoruz.
    sys.argv = [str(harness), sys.argv[2]]
    exec(compile(source, str(harness), "exec"), {"__name__": "__main__", "__file__": str(harness)})
    return True


def _icon_file():
    """Uygulama simgesinin yolu.

    `install_root()` üzerinden çözülüyor; paketlenmiş hâlde dosyalar
    `_internal` altına taşındığı için `__file__`'a göre hesaplamak orada
    yanlış yere bakıyordu. Bulunamazsa `.png` ile deneniyor.
    """
    from app.paths import install_root

    root = install_root() / "app" / "resources"
    for name in ("icon.ico", "icon.png"):
        candidate = root / name
        if candidate.exists():
            return candidate
    return None


def _claim_taskbar_identity() -> None:
    """Windows görev çubuğunda uygulamanın kendi simgesini göstermesini sağlar.

    Aksi hâlde Windows uygulamayı "Python" sayıyor ve simgesini pencereye
    verdiğimiz simgeyle değiştirmiyor. Kendimize ayrı bir kimlik tanıtınca
    görev çubuğu doğru simgeyi çiziyor.

    Ölçüldü: bu çağrı olmadan kaynaktan çalıştırıldığında görev çubuğunda
    Python'un simgesi çıkıyor, uygulamanınki değil.
    """
    if sys.platform != "win32":
        return

    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "AlicanKaya.Odyssey"
        )
    except Exception:
        # Simge biraz yanlış görünsün ama uygulama açılsın.
        pass


def check_python() -> None:
    if sys.version_info[:2] < MIN_PYTHON:
        raise SystemExit(
            f"Bu uygulama Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} veya üstünü "
            f"gerektiriyor. Şu an {sys.version.split()[0]} kullanılıyor."
        )


def _show_info(title, message, language, theme, window) -> None:
    """Tek düğmeli bilgi kutusu, arkası karartılmış."""
    from app.ui import titlebar
    from app.ui.confirm_dialog import ConfirmDialog
    from app.ui.modal import Backdrop

    perde = Backdrop(window)
    perde.show()
    kutu = ConfirmDialog(title, message, "", language.t("backup.ok"), window)
    titlebar.apply(kutu, theme.effective_mode)
    kutu.exec()
    perde.deleteLater()


def _show_restored(restored, language, theme, window) -> None:
    """İlerleme dosyası bozuk çıktı ve yedekten dönüldü: kişiye bir kez söyle."""
    from app.ui import titlebar
    from app.ui.confirm_dialog import ConfirmDialog
    from app.ui.modal import Backdrop

    t = language.t
    if restored.backup_day:
        baslik = t("backup.restored_title")
        metin = t("backup.restored_message", day=restored.backup_day, path=str(restored.broken_path))
    else:
        baslik = t("backup.lost_title")
        metin = t("backup.lost_message", path=str(restored.broken_path))
    perde = Backdrop(window)
    perde.show()
    kutu = ConfirmDialog(baslik, metin, "", t("backup.ok"), window)
    titlebar.apply(kutu, theme.effective_mode)
    kutu.exec()
    perde.deleteLater()


def main() -> int:
    # Denetleyici olarak çağrıldıysak arayüzü hiç kurmadan işi yapıp çıkıyoruz.
    if _run_harness_if_asked():
        return 0

    # Açılış animasyonu: programın kendisi `--intro` ile ikinci kez
    # başlatıyor (bkz. `app/core/intro_link.py`).
    if len(sys.argv) >= 3 and sys.argv[1] == "--intro":
        from app.ui.intro import run as run_intro

        return run_intro(sys.argv[2])

    # Görev Zamanlayıcı'nın hatırlatma çağrısı: arayüz kurulmadan, birkaç
    # saniyede bakıp gerekirse bildirim gösterip çıkıyor.
    if "--reminder-check" in sys.argv[1:]:
        from app.core import log, reminder_service

        log.setup("reminder")
        try:
            reminder_service.run_check()
        except Exception:  # noqa: BLE001 - arka planda sessizce bitmeli
            log.get("odyssey").exception("Hatırlatma denetimi başarısız")
        return 0

    # Bildirime tıklanınca Windows `odyssey://open` ile çağırıyor. Program
    # zaten açıksa ikinci bir pencere açılmıyor.
    if any(arg.startswith("odyssey:") for arg in sys.argv[1:]):
        from app.core import win_notify

        if win_notify.app_running():
            return 0
        sys.argv = [sys.argv[0]]

    check_python()

    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise SystemExit(
            "PySide6 yüklenemedi. Ortamı kurmak için:\n"
            "    py -3.14 tools/setup_env.py\n\n"
            "Not: Sanal ortamı Anaconda'nın Python'u ile kurma; Anaconda'nın\n"
            "taşıdığı eski MSVC kütüphaneleri Qt'nin açılmasını engelliyor.\n\n"
            f"Ayrıntı: {exc}"
        ) from exc

    from PySide6.QtGui import QIcon

    from app.core.intro_link import IntroLink, show_window
    from app.core.progress import ProgressStore
    from app.ui.splash import close_splash, show_splash

    # Ayarlar Qt'den önce okunuyor: açılış animasyonu ayrı bir süreç ve en
    # başta başlatılırsa bu sürecin Qt'yi ve pencereyi kurmasıyla aynı anda
    # açılıyor. Veritabanı sqlite, Qt gerektirmiyor.
    # Günlük kaydı ve veritabanı güvencesi: bozuk dosya açılmadan önce
    # yedekten dönülüyor, sağlamsa o günün yedeği alınıyor.
    from app.core import backup, log
    from app.paths import backups_dir, database_path

    log.setup("app")
    # Ayarlar › Veri › İçe aktar bir dosya bıraktıysa, veritabanı açılmadan
    # önce yerine konuyor (mevcut ilerleme yedekleniyor).
    from app.core import transfer
    from app.core.avatar import avatar_path

    imported = transfer.apply_pending(database_path(), avatar_path(), backups_dir())
    restored = backup.recover(database_path(), backups_dir())
    store = ProgressStore()
    backup.daily_backup(database_path(), backups_dir())
    from app.core import celebration_sound

    intro = IntroLink.launch(store.setting("theme", "dark"), store.setting("language", ""),
                             sound=celebration_sound.supported() and celebration_sound.enabled(store))

    # `main_window` burada içe aktarılmıyor: QtWebEngine'i o zincir yüklüyor
    # ve birkaç saniye sürüyor. Açılış ekranı tam o beklemeyi göstermek için
    # var, dolayısıyla ondan **sonra** aktarılıyor.

    application = QApplication(sys.argv)
    application.setApplicationName("Odyssey")
    application.setApplicationVersion(APP_VERSION)

    # "Program açık" kilidi: hatırlatma denetleyicisi buna bakıp açıkken
    # bildirim göndermiyor. Süreç kapanınca kilit kendiliğinden kalkıyor.
    from app.core import win_notify

    win_notify.claim_running()

    _claim_taskbar_identity()
    icon_path = _icon_file()
    icon = QIcon(str(icon_path)) if icon_path else QIcon()
    if not icon.isNull():
        application.setWindowIcon(icon)

    # Ayarlar kullanıcının kendi bilgisayarındaki veritabanından okunuyor.
    # Bu ucuz bir iş; açılış ekranından önce yapılıyor ki ekran doğru temada
    # açılsın. Ağır olan kısım ana pencerenin kurulması (Chromium).
    theme = ThemeManager(store.setting("theme", "dark"))
    theme.apply(application)

    # İlk açılışta dil, bilgisayarın diline göre seçiliyor ve kaydediliyor.
    # Kayıtlı bir seçim varsa ona dokunulmuyor: kullanıcı ayarlardan İngilizce
    # dediyse, Türkçe bir Windows'ta bile İngilizce açılmalı. Açılış
    # ekranından önce okunuyor ki ekrandaki yazılar doğru dilde çıksın.
    saved_language = store.setting("language", "")
    if saved_language not in AVAILABLE_LANGUAGES:
        saved_language = system_language()
        store.set_setting("language", saved_language)
    language = LanguageManager(saved_language)

    # Açılış ekranı, ağır kurulum başlamadan önce açılıyor: o kurulum bitene
    # kadar ekranda hiçbir belirti olmuyordu ve uygulama açılmamış gibi
    # duruyordu. Sürüm satırı `APP_VERSION`'dan geliyor.
    # Animasyon başlatılamadıysa eski açılış kartı gösteriliyor.
    splash_started = time.monotonic()
    splash = None
    if intro is None:
        splash = show_splash(
            icon_path,
            theme.effective_mode,
            language.t("app.subtitle"),
            f"v{APP_VERSION} · {language.t('splash.beta')}",
        )
        application.processEvents()

    def stage(key: str, value: float) -> None:
        if splash is not None:
            splash.set_stage(language.t(key), value)

    # Ağır kısım burada: bu satır QtWebEngine'i yüklüyor.
    stage("splash.stage_engine", 0.25)
    from app.ui.main_window import MainWindow

    stage("splash.stage_content", 0.55)
    window = MainWindow(language, theme, store)
    # Simge pencereye de ayrıca veriliyor. Windows görev çubuğu ve Alt+Tab
    # listesi uygulamanınkini değil, pencerenin kendi simgesini okuyor.
    if not icon.isNull():
        window.setWindowIcon(icon)
    # Tema başlangıçta da görünümlere bildirilsin.
    window._on_theme_changed(theme.effective_mode)

    # Pencere **görünmez** olarak açılıyor: opaklık sıfır.
    #
    # İki şeyi aynı anda istiyoruz. Birincisi, pencere açılış ekranı hâlâ
    # ekrandayken görünmemeli. İkincisi, belge alanlarının (Chromium) ilk
    # çizimi kullanıcı görmeden yapılmalı — yoksa her birine ilk girişte
    # ekran bir anlığına siyah kalıyor (ölçüldü: 48 ms, ortalama parlaklık
    # sıfır).
    #
    # Opaklığı sıfır bir pencere işletim sistemi tarafından yine de
    # bileşikleniyor, yani Chromium çiziyor ama kimse görmüyor. Açılış
    # ekranı kaybolurken opaklık bire çekiliyor.
    stage("splash.stage_pages", 0.8)
    window.setWindowOpacity(0.0)
    window.show()
    window.warm_up()

    first_name = store.profile().get("first_name", "").strip()
    greeting = (
        language.t("home.welcome_named", name=first_name)
        if first_name
        else language.t("home.welcome")
    )
    if intro is not None:
        # Animasyonun sonunu bekleyip pencereyi gösteriyor.
        intro.reveal(window)
    elif splash is not None:
        close_splash(splash, window, splash_started, greeting)
    else:
        show_window(window)

    # Beta uyarısı pencere göründükten sonra çıkıyor; boş ekranın önünde
    # açılan bir kutu, uygulamanın açılmadığı izlenimi veriyor.
    if restored is not None:
        _show_restored(restored, language, theme, window)
    elif imported:
        _show_info(language.t("backup.imported_title"), language.t("backup.imported_message"),
                   language, theme, window)

    from app.ui.beta_notice import SETTING_KEY, BetaNoticeDialog, mark_seen, should_show

    if should_show(store):
        from app.ui import titlebar

        if store.setting(SETTING_KEY, "") == "":
            # İlk kurulum: beta uyarısı.
            notice = BetaNoticeDialog(language, window)
            titlebar.apply(notice, theme.effective_mode)
            notice.exec()
        else:
            # Güncellemeden sonraki ilk açılış: "Neler yeni?" (Alican istedi).
            from app.ui.modal import Backdrop
            from app.ui.whats_new import WhatsNewDialog

            perde = Backdrop(window)
            perde.show()
            yenilik = WhatsNewDialog(language, window)
            titlebar.apply(yenilik, theme.effective_mode)
            yenilik.exec()
            perde.deleteLater()
            if yenilik.wants_notes:
                window._navigate("releases")
        mark_seen(store)

    # Seri hatırlatmaları kendiliğinden açılmıyor: ilk açılışta bir kez,
    # nasıl çalıştığı anlatılarak soruluyor. Açıksa görev arka planda
    # tazeleniyor (programın yolu güncellemeyle değişmiş olabilir).
    from app.core import reminder_service
    from app.ui.reminder_prompt import ReminderPromptDialog, should_ask

    if should_ask(store):
        from app.ui import titlebar

        prompt = ReminderPromptDialog(language, store, theme.effective_mode, window)
        titlebar.apply(prompt, theme.effective_mode)
        prompt.exec()
    else:
        reminder_service.ensure_async(store)

    # Tanıtım turu: ilk açılışta, bu güncellemeden sonra da herkese bir kez
    # soruluyor. Evet denirse tur başlıyor (her an geçilebiliyor).
    from app.ui import tour as tour_ui

    if tour_ui.should_ask(store):
        from app.ui import titlebar
        from app.ui.modal import Backdrop

        perde = Backdrop(window)
        perde.show()
        soru = tour_ui.TourPromptDialog(language, tour_ui.is_new_user(store), window)
        titlebar.apply(soru, theme.effective_mode)
        kabul = soru.exec()
        perde.deleteLater()
        if kabul:
            window.start_tour()
        else:
            tour_ui.mark(store, "declined")

    # Sürüm denetimi en sona bırakıldı: açılışın hiçbir adımı ağı
    # beklemiyor. Denetim ayrı bir iş parçacığında yapılıyor ve
    # başarısız olduğunda hiçbir şey göstermiyor.
    # Bir önceki güncellemeden kalan kurulum dosyası burada siliniyor:
    # kurulum programı çalışırken kendi dosyasını silemiyordu.
    from app.core.updater import cleanup as _cleanup_updates

    _cleanup_updates()

    window.start_update_check()

    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
