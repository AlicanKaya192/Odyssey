"""Profil ekranı.

Bütün bilgiler kullanıcının kendi bilgisayarında, `%APPDATA%\\Odyssey\\progress.db`
içinde duruyor — sunucu yok, hesap yok, hiçbir veri dışarı çıkmıyor.

**Neden yeniden yazıldı?** Önceki hâli bir profil değil, bir **formdu**: ad
ve soyad giriş kutularının içinde duruyordu, yani kişi kendi adını hiçbir
zaman "görmüyordu"; en önemli sayı olan genel ilerleme diğer dördüyle aynı
boyuttaydı; ve geniş ekranda içerik dar bir sütuna sıkışıp altta koca bir
boşluk bırakıyordu.

Şimdiki düzen:

- **Solda kimlik kartı** — fotoğraf, ad, başlangıç tarihi ve ilerleme
  çubuğu. Yalnızca gösteriyor; düzenleme ayrı bir pencerede
  (`profile_edit_dialog.py`), çünkü form alanları bu dar sütuna
  sığmıyordu ve yazılar kırpılıyordu.
- **Sağ üstte sayı şeridi**, altında **rozet duvarı**.
- **Altta tam genişlikte etkinlik ızgarası** ve sağında yıl seçici.
"""

from __future__ import annotations

from datetime import date
from html import escape

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..core.avatar import load_avatar
from ..core import badges as badge_core
from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..paths import content_dir
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING, mix
from ..widgets.activity_graph import ActivityGraph
from ..widgets.avatar import AvatarView
from ..widgets.badge_wall import BadgeWall
from ..widgets.segmented import SegmentedControl
from ..widgets.common import Card, section_label

# Rozet ipucunun genişliği. Zengin metinde Qt kendiliğinden sarmıyor.
TOOLTIP_WIDTH = 280

# Rozet duvarının sayfa okları ve "1 / 2" yazısı.
# Düğmenin ölçüsü stil dosyasındaki `variant="page-nav"` kuralında.
PAGE_ICON = 16
PAGE_LABEL_PX = 13

# Üst karttaki fotoğrafın çapı.
AVATAR_SIZE = 108

# Sol sütunun genişliği. Artık yalnızca gösteriyor — düzenleme ayrı bir
# pencerede olduğu için buraya form sığdırmak gerekmiyor.
IDENTITY_WIDTH = 344

# Profil sayfasının genişliği. `CONTENT_WIDTH` (820) okuma metni için
# ayarlanmış bir ölçü; burası bir gösterge paneli ve o genişlikte
# istatistik etiketleri kırpılıyordu ("Üst üste çalışılan gün" tek
# satırda 234 piksel istiyor).
PROFILE_WIDTH = 1240


class ProgressBar(QFrame):
    """İnce ilerleme çubuğu."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setProperty("role", "progress-track")
        self.setFixedHeight(8)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._fill = QFrame()
        self._fill.setProperty("role", "progress-fill")
        layout.addWidget(self._fill)
        self._spacer = QWidget()
        layout.addWidget(self._spacer)

        self.set_ratio(0.0)

    def set_ratio(self, ratio: float) -> None:
        """0 ile 1 arasında doluluk."""
        ratio = max(0.0, min(1.0, ratio))
        # Esneme paylarıyla veriliyor: sabit piksel yazılsaydı pencere
        # genişleyince çubuk yerinde kalırdı.
        self.layout().setStretch(0, max(1, int(ratio * 1000)))
        self.layout().setStretch(1, max(1, int((1 - ratio) * 1000)))
        self._fill.setVisible(ratio > 0)


class ProfileView(QWidget):
    """Kullanıcının profili, ilerleme özeti ve etkinlik geçmişi."""

    saved = Signal()

    def __init__(
        self,
        catalog: Catalog,
        language: LanguageManager,
        store: ProgressStore,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._catalog = catalog
        self._language = language
        self._store = store
        self._mode = "light"
        self._badge_list: list = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(
            SPACING["xl"], SPACING["lg"], SPACING["xl"], SPACING["xxl"]
        )
        row.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(PROFILE_WIDTH)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._column = QVBoxLayout(column)
        self._column.setContentsMargins(0, 0, 0, 0)
        self._column.setSpacing(SPACING["lg"])

        # Üst alan iki sütun: solda kimlik, sağda rozetler.
        #
        # Arada bir de sayı kartı vardı — çözülen alıştırma, tamamlanan
        # bölüm, seri, ilerleme. Dördü de öğrenme yolu ekranının
        # karşılama şeridinde zaten duruyor; profilde ikinci kez
        # göstermek yer kaplamaktan başka bir şey yapmıyordu. Rozet
        # duvarı onun yerine geçti ve sığmayanlar için sayfa geçişi
        # kazandı.
        ust = QHBoxLayout()
        ust.setSpacing(SPACING["lg"])

        kimlik = self._build_identity()
        kimlik.setFixedWidth(IDENTITY_WIDTH)
        ust.addWidget(kimlik, 0)
        ust.addWidget(self._build_badges(), 1)

        self._column.addLayout(ust)
        self._column.addWidget(self._build_activity())
        self._column.addStretch(1)

        row.addWidget(column, 10)
        row.addStretch(1)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.refresh()

    # --- kimlik kartı -----------------------------------------------------

    def _build_identity(self) -> QWidget:
        holder = QWidget()
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["sm"])

        # Yanındaki rozet kartının üstünde bir başlık var; kimlik kartında
        # olmayınca iki kart farklı yükseklikten başlıyordu.
        self._identity_title = section_label("")
        layout.addWidget(self._identity_title)

        card = Card(mode=self._mode, padding=SPACING["lg"])
        self._identity_card = card

        sag = card.body
        sag.setSpacing(SPACING["xs"])

        # Kart, sağdaki sütun kadar uzuyor (rozet duvarı onu aşağı çekiyor).
        # Artan boşluk tek parça hâlinde "Düzenle" düğmesinin üstünde
        # kalıyordu; içerik iki uçtan eşit payla ortalanınca kart dolu
        # görünüyor ve düğme metnin hemen altında duruyor.
        sag.addStretch(1)

        self._avatar = AvatarView(AVATAR_SIZE)
        self._avatar.clicked.connect(self._open_editor)
        sag.addWidget(self._avatar, 0, Qt.AlignmentFlag.AlignHCenter)
        sag.addSpacing(SPACING["xs"])

        self._name_label = QLabel()
        self._name_label.setProperty("role", "subtitle")
        self._name_label.setStyleSheet("font-size: 18px; font-weight: 750;")
        self._name_label.setWordWrap(True)
        self._name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        sag.addWidget(self._name_label)

        self._started = QLabel()
        self._started.setProperty("role", "muted")
        # Tarih uzun bir dizgi ve dil değişince uzunluğu da değişiyor;
        # sarma açık olmasa kart genişlediği ölçüde kırpılıyordu.
        self._started.setWordWrap(True)
        self._started.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        sag.addWidget(self._started)

        sag.addSpacing(SPACING["sm"])

        # Genel ilerleme: profilin en önemli sayısı.
        self._progress_caption = QLabel()
        self._progress_caption.setProperty("role", "muted")
        self._progress_caption.setWordWrap(True)
        sag.addWidget(self._progress_caption)
        sag.addSpacing(2)

        self._progress = ProgressBar()
        sag.addWidget(self._progress)

        sag.addSpacing(SPACING["md"])

        self._edit_button = QPushButton()
        self._edit_button.setProperty("variant", "ghost")
        self._edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._edit_button.clicked.connect(self._open_editor)
        sag.addWidget(self._edit_button)

        sag.addStretch(1)
        layout.addWidget(card, 1)
        return holder

    # --- rozetler ---------------------------------------------------------

    def _build_badges(self) -> QWidget:
        holder = QWidget()
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["sm"])

        self._badges_title = section_label("")
        layout.addWidget(self._badges_title)

        card = Card(mode=self._mode, padding=SPACING["lg"])
        self._badges_card = card

        self._badges_count = QLabel()
        self._badges_count.setProperty("role", "muted")
        # Aralıklar elle veriliyor: kartın kendi `spacing` değeri esneme
        # paylarının da arasına giriyor ve üst boşluk alttan 8 piksel
        # fazla çıkıyordu.
        card.body.setSpacing(0)

        card.body.addWidget(self._badges_count)
        # Rozetler sayaç satırı ile kartın altı arasında dikey ortalanıyor;
        # tek bir esneme payı sonda kalınca hepsi yukarı yapışıyordu.
        card.body.addStretch(1)

        # Oklar kartın iki ucunda, rozetler ortada.
        #
        # İkisi de sağ üstteyken duvar sola yaslı kalıyor ve sağda tek
        # parça bir boşluk oluyordu. Uçlara alınınca o boşluk okların
        # yerine dönüşüyor ve rozetler ortalanıyor.
        orta = QHBoxLayout()
        orta.setSpacing(SPACING["sm"])

        self._badge_prev = self._page_button("arrow-left", -1)
        self._badge_next = self._page_button("arrow-right", 1)
        self._badge_wall = BadgeWall()
        self._badge_wall.paging_changed.connect(self._refresh_paging)

        orta.addWidget(self._badge_prev, 0, Qt.AlignmentFlag.AlignVCenter)
        orta.addWidget(self._badge_wall, 1)
        orta.addWidget(self._badge_next, 0, Qt.AlignmentFlag.AlignVCenter)
        card.body.addLayout(orta)

        # "1 / 2" rozetlerin altında, ortada. Oklar aynı genişlikte olduğu
        # için kartın ortası duvarın da ortası oluyor.
        self._badge_page_label = QLabel()
        # Soluk ve ince hâlinde okunmuyordu; kalın ve normal metin rengi.
        self._badge_page_label.setStyleSheet(
            f"font-size: {PAGE_LABEL_PX}px; font-weight: 700;"
        )
        self._badge_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card.body.addSpacing(SPACING["md"])
        card.body.addWidget(self._badge_page_label)
        card.body.addStretch(1)

        layout.addWidget(card, 1)
        return holder

    def _page_button(self, icon_name: str, step: int) -> QPushButton:
        """Rozet duvarının sayfa oku."""
        button = QPushButton()
        button.setProperty("variant", "page-nav")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(
            lambda _=False, s=step: self._badge_wall.set_page(
                self._badge_wall.page + s
            )
        )
        button.setProperty("icon_name", icon_name)
        return button

    def _refresh_paging(self) -> None:
        """Okları ve "1 / 2" yazısını duvarın durumuna göre günceller."""
        duvar = self._badge_wall
        tek_sayfa = duvar.page_count <= 1
        for parca in (self._badge_prev, self._badge_page_label, self._badge_next):
            parca.setVisible(not tek_sayfa)
        if tek_sayfa:
            return
        self._badge_page_label.setText(f"{duvar.page + 1} / {duvar.page_count}")
        self._badge_prev.setEnabled(duvar.page > 0)
        self._badge_next.setEnabled(duvar.page < duvar.page_count - 1)
        self._paint_page_buttons()

    def _paint_page_buttons(self) -> None:
        """Ok simgelerini tema rengiyle çizer.

        Simge bir `QIcon`; QSS ona ulaşamıyor, tema değişince elle
        yenileniyor (anahtar ve ızgarayla aynı sebep).
        """
        p = PALETTES.get(self._mode, PALETTES["light"])
        for button in (self._badge_prev, self._badge_next):
            renk = p["text"] if button.isEnabled() else p["text_muted"]
            button.setIcon(icon(button.property("icon_name"), renk, PAGE_ICON))
            button.setIconSize(QSize(PAGE_ICON, PAGE_ICON))

    def _wrap(self, text: str, pixel_size: int) -> str:
        """Metni ipucu genişliğine göre satırlara böler ve kaçışlar.

        Kelime kelime ölçülüyor; karakter sayısına göre bölmek iki dilde
        de yanlış yerde kesiyor.
        """
        font = QFont(self.font())
        font.setPixelSize(pixel_size)
        olcu = QFontMetrics(font)

        satirlar: list[str] = []
        gecerli = ""
        for kelime in text.split():
            aday = f"{gecerli} {kelime}".strip()
            if gecerli and olcu.horizontalAdvance(aday) > TOOLTIP_WIDTH:
                satirlar.append(gecerli)
                gecerli = kelime
            else:
                gecerli = aday
        if gecerli:
            satirlar.append(gecerli)
        return "<br>".join(escape(satir) for satir in satirlar)

    def _badge_tooltip(self, badge) -> str:
        """Rozetin üstüne gelince görünen kart.

        Zengin metin: düz metinde üç satırın üçü de aynı boyutta ve aynı
        renkte çıkıyordu, rozetin adı ile koşulu birbirinden ayrılmıyordu.
        Qt ipucu içinde HTML'in bir alt kümesini çiziyor; başlık, durum ve
        koşul burada boyut ve renkle ayrılıyor.

        Satırlar elle bölünüyor. Zengin metinde Qt kendiliğinden sarmıyor
        ve `<table width>` yalnızca **alt** sınır oluyor: 280 piksel
        istendiğinde en uzun açıklama 494 piksel çiziliyordu, ölçüldü.
        Tablo yine de duruyor, çünkü kısa ipuçlarına ortak bir en az
        genişlik veriyor.

        Emoji kullanılmıyor; `✓` ve `○` her yazı tipinde aynı çiziliyor ve
        metin rengini alıyor.
        """
        p = PALETTES.get(self._mode, PALETTES["light"])
        title = self._wrap(self._language.pick(badge.title), 15)
        desc = self._wrap(self._language.pick(badge.description), 13)

        if badge.earned:
            tarih = badge.earned_at[:10] if badge.earned_at else ""
            durum = self._wrap(
                self._language.t("profile.badge_earned", date=tarih), 12
            )
            durum_rengi, isaret = p["success"], "✓"
        else:
            durum = self._wrap(self._language.t("profile.badge_locked"), 12)
            durum_rengi, isaret = p["text_muted"], "○"

        return (
            f'<table width="{TOOLTIP_WIDTH}" cellspacing="0" cellpadding="0"><tr><td>'
            f'<div style="font-size:15px; font-weight:700; color:{p["text"]};">'
            f"{title}</div>"
            f'<div style="font-size:12px; color:{durum_rengi};">'
            f"{isaret}&nbsp;&nbsp;{durum}</div>"
            f'<div style="margin-top:8px; font-size:13px; color:{p["text_muted"]};">'
            f"{desc}</div>"
            "</td></tr></table>"
        )

    # --- etkinlik ---------------------------------------------------------

    def _build_activity(self) -> QWidget:
        holder = QWidget()
        layout = QVBoxLayout(holder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING["sm"])

        self._activity_title = section_label("")
        layout.addWidget(self._activity_title)

        card = Card(mode=self._mode, padding=SPACING["lg"])
        self._activity_card = card

        self._activity_summary = QLabel()
        self._activity_summary.setProperty("role", "muted")
        card.body.addWidget(self._activity_summary)
        card.body.addSpacing(SPACING["sm"])

        # Izgara solda, yıllar sağında dikey. Yıl seçici üstte yatay
        # duruyordu; ızgaranın dışında, yanında olması hem GitHub'daki
        # yerleşim hem de ızgaranın genişliğini bölmüyor.
        orta = QHBoxLayout()
        orta.setSpacing(SPACING["lg"])

        self._graph = ActivityGraph()
        self._graph.set_tooltip_maker(self._activity_tooltip)
        orta.addWidget(self._graph, 1, Qt.AlignmentFlag.AlignTop)

        self._year_picker = None
        self._year_holder = QWidget()
        # Kartın içinde: kendi zeminini boyamamalı, yoksa kartta delik
        # açıyor (genel `QWidget` kuralı sayfa zeminini veriyor).
        self._year_holder.setProperty("role", "bare")
        tutucu = QVBoxLayout(self._year_holder)
        tutucu.setContentsMargins(0, 0, 0, 0)
        tutucu.setSpacing(0)
        self._year_layout = tutucu
        orta.addWidget(self._year_holder, 0, Qt.AlignmentFlag.AlignTop)
        card.body.addLayout(orta)

        # Renk ölçeği açıklaması.
        legend = QHBoxLayout()
        legend.setSpacing(SPACING["xs"])
        legend.addStretch(1)
        self._legend_less = QLabel()
        self._legend_less.setProperty("role", "muted")
        legend.addWidget(self._legend_less)
        self._legend_cells = []
        for _ in range(4):
            hucre = QFrame()
            hucre.setFixedSize(14, 14)
            self._legend_cells.append(hucre)
            legend.addWidget(hucre)
        self._legend_more = QLabel()
        self._legend_more.setProperty("role", "muted")
        legend.addWidget(self._legend_more)
        card.body.addSpacing(SPACING["xs"])
        card.body.addLayout(legend)

        layout.addWidget(card)
        return holder

    def _rebuild_years(self) -> None:
        """Yıl düğmelerini kurar.

        Yıllar veriye göre değişebildiği için (yeni yıla geçmek, eski
        kayıtların gelmesi) seçici her yenilemede baştan kuruluyor.
        """
        yillar = self._store.activity_years()
        current_year = date.today().year
        if current_year not in yillar:
            yillar.append(current_year)
        yillar = sorted(list(set(yillar)), reverse=True)

        if self._year_picker is not None:
            if [int(v) for v, _ in self._year_options] == yillar:
                self._year_picker.set_value(str(self._graph.year))
                return
            self._year_layout.removeWidget(self._year_picker)
            self._year_picker.deleteLater()

        self._year_options = [(str(y), str(y)) for y in yillar]
        self._year_picker = SegmentedControl(self._year_options, vertical=True)
        self._year_picker.set_value(str(self._graph.year))
        self._year_picker.selected.connect(self._on_year)
        self._year_layout.addWidget(self._year_picker)
        # Tek yıl varken de gösteriliyor: seçici hiç görünmeyince "yıl
        # seçme diye bir şey var mı" sorusunun cevabı yok, çalışıp
        # çalışmadığı anlaşılmıyor.

    def _on_year(self, value: str) -> None:
        yil = int(value)
        self._graph.set_year(yil)
        self._graph.set_counts(self._store.activity_for_year(yil))
        self._refresh_activity_summary()

    def _refresh_activity_summary(self) -> None:
        yil = self._graph.year
        toplam = sum(self._store.activity_for_year(yil).values())
        self._activity_summary.setText(
            self._language.t("profile.activity_summary", count=toplam, year=yil)
        )

    def _activity_tooltip(self, day: date, count: int) -> str:
        tarih = day.strftime("%d.%m.%Y")
        if count == 0:
            return self._language.t("profile.activity_none", date=tarih)
        return self._language.t("profile.activity_count", count=count, date=tarih)

    # --- veri -------------------------------------------------------------

    def refresh(self) -> None:
        profile = self._store.profile()
        self._refresh_avatar()
        self._refresh_name()

        started = profile.get("started_at", "")
        self._started.setText(
            self._language.t("profile.member_since", date=started[:10]) if started else ""
        )

        total = 0
        completed = 0
        for chapter in self._catalog.chapters:
            for section in chapter.sections:
                total += 1
                state = self._store.section_state(
                    chapter.id, section.id, len(section.exercises)
                )
                if state.status(section.requires_quiz, section.requires_exercises) == "completed":
                    completed += 1

        self._completed = completed
        self._total = total
        self._progress.set_ratio(completed / total if total else 0.0)

        self._rebuild_years()
        self._graph.set_counts(self._store.activity_for_year(self._graph.year))

        # Rozetler her yenilemede yeniden değerlendiriliyor; yeni kazanılan
        # varsa tarihi bu çağrıda kaydediliyor.
        self._badge_list = badge_core.collect(
            self._catalog, self._store, content_dir() / "badges.json"
        )

        self.retranslate()

    # --- düzenleme --------------------------------------------------------

    def _open_editor(self) -> None:
        """Düzenleme penceresini açar; arkayı karartır."""
        from .modal import Backdrop
        from .profile_edit_dialog import ProfileEditDialog

        kok = self.window()
        perde = Backdrop(kok)
        perde.show()

        dialog = ProfileEditDialog(self._language, self._store, self._mode, kok)
        kabul = dialog.exec()
        perde.deleteLater()

        if kabul:
            self._store.set_profile(dialog.first_name, dialog.last_name)
            self.refresh()
            self.saved.emit()
        elif dialog.photo_changed:
            # Vazgeçilse bile fotoğraf dosyaya yazılmış oluyor; ekranın
            # onu göstermesi gerekiyor.
            self.refresh()
            self.saved.emit()

    def _refresh_name(self) -> None:
        profile = self._store.profile()
        ad = " ".join(
            part for part in
            (profile.get("first_name", ""), profile.get("last_name", ""))
            if part
        ).strip()
        self._name_label.setText(ad or self._language.t("profile.no_name"))

    def _refresh_avatar(self) -> None:
        """Karttaki fotoğrafı ve baş harfleri günceller.

        Fotoğrafın seçilmesi artık düzenleme penceresinde; burada yalnızca
        gösteriliyor.
        """
        profile = self._store.profile()
        harfler = "".join(
            parca[:1]
            for parca in (profile.get("first_name", ""), profile.get("last_name", ""))
            if parca
        )
        self._avatar.set_initials(harfler)
        self._avatar.set_photo(load_avatar())
        palette = PALETTES.get(self._mode, PALETTES["light"])
        self._avatar.set_colors(palette["accent"], "#FFFFFF")

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._identity_card.set_mode(mode)
        self._badges_card.set_mode(mode)
        self._activity_card.set_mode(mode)
        self._refresh_avatar()
        self._paint_graph()
        # Rozet ipuçları zengin metin ve sayfa okları birer `QIcon`;
        # ikisinin de renkleri paletten geliyor ve QSS onlara ulaşmıyor,
        # tema değişince yeniden üretilmeleri gerekiyor.
        self.retranslate()

    def _paint_graph(self) -> None:
        """Izgaranın renklerini temadan alır.

        QSS bir widget'ın `paintEvent` çizimine ulaşamıyor; renkler elle
        veriliyor ve tema değişince yenileniyor.
        """
        p = PALETTES.get(self._mode, PALETTES["light"])
        # Üç koyuluk, boş kare renginden vurgu rengine doğru harmanlanıyor.
        # Önce paletten üç ayrı ton alınıyordu; ölçüldü, son iki ton
        # arasındaki fark açık temada ΔE 14 çıkıyordu (25'in altı "zor ayırt
        # edilir") ve üç basamak iki gibi görünüyordu. Harmanla adımlar
        # 23-38 arasında, düzenli.
        olcek = [mix(p["surface_alt"], p["accent"], oran) for oran in (0.35, 0.65, 1.0)]
        self._graph.set_colors(p["surface_alt"], olcek, p["text_muted"])

        for index, hucre in enumerate(self._legend_cells):
            renk = p["surface_alt"] if index == 0 else olcek[index - 1]
            hucre.setStyleSheet(f"background-color: {renk}; border-radius: 3px;")

    def retranslate(self) -> None:
        t = self._language.t
        self._edit_button.setText(t("profile.edit"))
        self._refresh_avatar()
        self._refresh_name()

        yuzde = round(self._completed * 100 / self._total) if self._total else 0
        self._progress_caption.setText(
            t("profile.progress_caption", percent=yuzde,
              done=self._completed, total=self._total)
        )

        self._identity_title.setText(self._language.t_upper("profile.title"))
        self._badges_title.setText(self._language.t_upper("profile.badges"))
        kazanilan = sum(1 for b in self._badge_list if b.earned)
        self._badges_count.setText(
            t("profile.badge_progress", earned=kazanilan, total=len(self._badge_list))
        )
        p = PALETTES.get(self._mode, PALETTES["light"])
        self._badge_wall.set_badges(
            self._badge_list,
            lambda b: self._language.pick(b.title),
            self._badge_tooltip,
            (p["text_inverse"], p["text_muted"]),
        )
        self._refresh_paging()

        self._activity_title.setText(self._language.t_upper("profile.activity"))
        self._refresh_activity_summary()
        self._legend_less.setText(t("profile.activity_less"))
        self._legend_more.setText(t("profile.activity_more"))

        self._graph.set_labels(
            [t(f"month.{i}") for i in range(1, 13)],
            [t(f"weekday.{i}") for i in range(7)],
        )
        self._paint_graph()
