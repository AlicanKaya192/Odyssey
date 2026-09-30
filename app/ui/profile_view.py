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

from PySide6.QtCore import QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter
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
from ..core import levels as level_core
from ..core.catalog import Catalog
from ..core.language import LanguageManager
from ..core.progress import ProgressStore
from ..paths import content_dir
from ..resources.icons import icon
from ..resources.theme.tokens import PALETTES, SPACING, mix
from ..widgets.activity_graph import ActivityGraph
from ..widgets.avatar import AvatarView
from ..widgets.badge_wall import BadgeWall
from ..widgets import motion
from ..widgets.segmented import SegmentedControl
from ..widgets.effects import apply_shadow, refresh_shadow
from ..widgets.common import Card

# Rozet ipucunun genişliği. Zengin metinde Qt kendiliğinden sarmıyor.
TOOLTIP_WIDTH = 280

# Rozet duvarının sayfa okları ve "1 / 2" yazısı.
# Düğmenin ölçüsü stil dosyasındaki `variant="page-nav"` kuralında.
PAGE_ICON = 16
PAGE_LABEL_PX = 13

# Üst karttaki fotoğrafın çapı.
AVATAR_SIZE = 140  # 124 px daire + 8 px halka payı

# Sol sütunun genişliği. Artık yalnızca gösteriyor — düzenleme ayrı bir
# pencerede olduğu için buraya form sığdırmak gerekmiyor.
IDENTITY_WIDTH = 380

# Profil sayfasının genişliği. `CONTENT_WIDTH` (820) okuma metni için
# ayarlanmış bir ölçü; burası bir gösterge paneli ve o genişlikte
# istatistik etiketleri kırpılıyordu ("Üst üste çalışılan gün" tek
# satırda 234 piksel istiyor).
PROFILE_WIDTH = 1116


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


# Profilde en son görülen kazanılmış rozetler (virgüllü); fark "yeni" sayılır.
SEEN_BADGES_KEY = "profile_seen_badges"


class PagerDots(QWidget):
    """Sayfa noktaları: açık sayfa uzun ve vurgu renginde (C9)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._count = 1
        self._pos = 0.0
        self.setFixedHeight(8)

    def set_pages(self, count: int, current: int) -> None:
        ilk = self._count != count
        self._count = count
        self.setFixedWidth(max(1, count) * 12 + 14)
        if ilk:
            self._pos = float(current)
            self.update()
            return
        motion.animate(self, "pos", self._pos, float(current), self._set_pos, "spring", "spring")

    def _set_pos(self, v: float) -> None:
        self._pos = v
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        from ..widgets.effects import theme_palette

        p = theme_palette()
        g = QPainter(self)
        g.setRenderHint(QPainter.RenderHint.Antialiasing)
        x = 0.0
        for i in range(self._count):
            yakinlik = max(0.0, 1 - abs(self._pos - i))
            w = 6 + 14 * yakinlik
            renk = QColor(mix(p["border_strong"], p["accent"], yakinlik))
            g.setPen(Qt.PenStyle.NoPen)
            g.setBrush(renk)
            g.drawRoundedRect(QRectF(x, 1, w, 6), 3, 3)
            x += w + 6


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
        self._levels = level_core.Update(level_core.level_state(0))
        self._tag_list = level_core.load_tags(content_dir() / "tags.json")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(32, 32, 32, 32)
        row.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(PROFILE_WIDTH)
        column.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self._column = QVBoxLayout(column)
        self._column.setContentsMargins(0, 0, 0, 0)
        self._column.setSpacing(26)

        # Üst alan iki sütun: solda kimlik, sağda rozetler.
        #
        # Arada bir de sayı kartı vardı — çözülen alıştırma, tamamlanan
        # bölüm, seri, ilerleme. Dördü de öğrenme yolu ekranının
        # karşılama şeridinde zaten duruyor; profilde ikinci kez
        # göstermek yer kaplamaktan başka bir şey yapmıyordu. Rozet
        # duvarı onun yerine geçti ve sığmayanlar için sayfa geçişi
        # kazandı.
        ust = QHBoxLayout()
        ust.setSpacing(26)

        kimlik = self._build_identity()
        kimlik.setFixedWidth(IDENTITY_WIDTH)
        ust.addWidget(kimlik, 0)
        ust.addWidget(self._build_badges(), 1)

        self._column.addLayout(ust)
        self._column.addWidget(self._build_activity())
        self._column.addStretch(1)

        row.addWidget(column, 100)
        row.addStretch(1)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.refresh()

    # --- kimlik kartı -----------------------------------------------------

    def _build_identity(self) -> QWidget:
        """Kimlik kartı (prototip `.pcard`): avatar, ad, unvan, başlangıç,
        seviye ve XP çubuğu, "Profili düzenle"."""
        card = Card(mode=self._mode, padding=28)
        self._identity_card = card
        sag = card.body
        sag.setSpacing(6)
        # İçerik kartın yüksekliğinde dikey ortalı (kart rozet kartı kadar uzuyor).
        sag.addStretch(1)

        self._avatar = AvatarView(AVATAR_SIZE)
        self._avatar.clicked.connect(self._open_editor)
        sag.addWidget(self._avatar, 0, Qt.AlignmentFlag.AlignHCenter)
        sag.addSpacing(4)

        self._name_label = QLabel()
        self._name_label.setProperty("role", "pcard-name")
        self._name_label.setWordWrap(True)
        self._name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        sag.addWidget(self._name_label)

        # Unvan: tıklanınca unvan penceresi açılıyor. Seçili unvan yoksa
        # kesik çerçeveli "Unvan seç".
        self._tag_button = QPushButton()
        self._tag_button.setProperty("variant", "tag-chip")
        self._tag_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._tag_button.clicked.connect(self._open_tags)
        sag.addSpacing(2)
        sag.addWidget(self._tag_button, 0, Qt.AlignmentFlag.AlignHCenter)
        sag.addSpacing(2)

        self._started = QLabel()
        self._started.setProperty("role", "pcard-since")
        self._started.setWordWrap(True)
        self._started.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        sag.addWidget(self._started)

        sag.addSpacing(10)
        satir = QHBoxLayout()
        # Seviye ve o seviyenin içindeki XP. Burada önce genel ilerleme
        # yüzdesi vardı; aynı yüzde Öğrenme Yolu'nda duruyor.
        self._progress_caption = QLabel()
        self._progress_caption.setProperty("role", "pcard-level")
        self._progress_percent = QLabel()
        self._progress_percent.setProperty("role", "pcard-percent")
        satir.addWidget(self._progress_caption)
        satir.addStretch(1)
        satir.addWidget(self._progress_percent)
        sag.addLayout(satir)
        self._progress = ProgressBar()
        sag.addWidget(self._progress)


        sag.addSpacing(12)
        self._edit_button = QPushButton()
        self._edit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._edit_button.clicked.connect(self._open_editor)
        sag.addWidget(self._edit_button)
        sag.addStretch(1)
        return card

    # --- rozetler ---------------------------------------------------------

    def _build_badges(self) -> QWidget:
        card = QFrame()
        card.setProperty("surface", "card")
        apply_shadow(card, self._mode)
        self._badges_card = card
        govde = QVBoxLayout(card)
        govde.setContentsMargins(24, 22, 24, 22)
        govde.setSpacing(0)
        card.body = govde

        # Başlık satırı (prototip `.bwall .hd`): ad, sağda oklar.
        ust = QHBoxLayout()
        ust.setSpacing(12)
        self._badges_title = QLabel()
        self._badges_title.setProperty("role", "card-head")
        ust.addWidget(self._badges_title)
        ust.addStretch(1)
        self._badge_prev = self._page_button("chevron-left", -1)
        self._badge_next = self._page_button("chevron-right", 1)
        ust.addWidget(self._badge_prev)
        ust.addWidget(self._badge_next)
        govde.addLayout(ust)
        govde.addSpacing(14)

        self._badge_wall = BadgeWall()
        self._badge_wall.paging_changed.connect(self._refresh_paging)
        govde.addWidget(self._badge_wall)

        # Sayfa noktaları rozetlerin altında, ortada; açık sayfanın noktası
        # uzun ve vurgu renginde, sayfa değişince yayla uzayıp kısalıyor.
        self._badge_page_label = PagerDots()
        govde.addSpacing(12)
        govde.addWidget(self._badge_page_label, 0, Qt.AlignmentFlag.AlignHCenter)

        # Rozet / gün seri / bölüm: rozetlerin altında ince çizgiyle ayrılmış
        # ayrı bir bölüm (Alican: kimlik kartında boşluk bırakıyordu, rozet
        # kartında da altta boşluk kalıyordu).
        govde.addSpacing(18)
        cizgi = QFrame()
        cizgi.setProperty("role", "divider")
        cizgi.setFixedHeight(1)
        govde.addWidget(cizgi)
        govde.addSpacing(18)
        sag = govde
        # Üç küçük sayı (prototip `.minis`).
        minis = QHBoxLayout()
        minis.setSpacing(8)
        self._minis: dict[str, tuple[QLabel, QLabel]] = {}
        for anahtar in ("badges", "streak", "sections"):
            kutu = QFrame()
            kutu.setProperty("role", "mini")
            ic = QVBoxLayout(kutu)
            ic.setContentsMargins(6, 10, 6, 10)
            ic.setSpacing(0)
            deger = QLabel()
            deger.setProperty("role", "mini-value")
            deger.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            ad = QLabel()
            ad.setProperty("role", "mini-label")
            ad.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            ic.addWidget(deger)
            ic.addWidget(ad)
            minis.addWidget(kutu, 1)
            self._minis[anahtar] = (deger, ad)
        sag.addLayout(minis)
        govde.addStretch(1)
        return card

    def _page_button(self, icon_name: str, step: int) -> QPushButton:
        """Rozet duvarının sayfa oku."""
        button = QPushButton()
        button.setProperty("variant", "round-nav")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(
            lambda _=False, s=step: self._badge_wall.set_page(
                (self._badge_wall.page + s) % self._badge_wall.page_count, animate=True
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
        self._badge_page_label.set_pages(duvar.page_count, duvar.page)
        self._paint_page_buttons()

    def _paint_page_buttons(self) -> None:
        """Ok simgelerini tema rengiyle çizer.

        Simge bir `QIcon`; QSS ona ulaşamıyor, tema değişince elle
        yenileniyor (anahtar ve ızgarayla aynı sebep).
        """
        p = PALETTES.get(self._mode, PALETTES["light"])
        for button in (self._badge_prev, self._badge_next):
            renk = p["text"]
            button.setIcon(icon(button.property("icon_name"), renk, PAGE_ICON))
            button.setIconSize(QSize(17, 17))
        self._edit_button.setIcon(icon("pencil", p["text"], 16))

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
        card = Card(mode=self._mode, padding=24)
        self._activity_card = card

        bas = QHBoxLayout()
        bas.setSpacing(10)
        self._activity_title = QLabel()
        self._activity_title.setProperty("role", "card-head")
        bas.addWidget(self._activity_title)
        self._activity_summary = QLabel()
        self._activity_summary.setProperty("role", "pcard-since")
        bas.addWidget(self._activity_summary)
        bas.addStretch(1)
        card.body.addLayout(bas)
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
        return card

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
        gun = sum(1 for v in self._store.activity_for_year(yil).values() if v)
        self._activity_summary.setText(
            self._language.t("profile.activity_days", count=gun, year=yil)
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

        self._started_raw = profile.get("started_at", "")
        self._render_started()

        total = 0
        completed = 0
        for chapter in self._catalog.chapters:
            for section in chapter.sections:
                total += 1
                state = self._store.section_state(
                    chapter.id, section.id, section.exercises
                )
                if state.status(section.requires_quiz, section.requires_exercises) == "completed":
                    completed += 1

        self._completed = completed
        self._total = total

        self._rebuild_years()
        self._graph.set_counts(self._store.activity_for_year(self._graph.year))

        # Rozetler her yenilemede yeniden değerlendiriliyor; yeni kazanılan
        # varsa tarihi bu çağrıda kaydediliyor.
        self._badge_list = badge_core.collect(
            self._catalog, self._store, content_dir() / "badges.json"
        )

        # Profil ekranına her dönüşte rozet duvarı 1. sayfadan başlasın; son
        # ziyaretten beri kazanılan rozet varsa onun sayfasından.
        kazanilan = {b.id for b in self._badge_list if b.earned}
        kayit = self._store.setting(SEEN_BADGES_KEY, None)
        gorulen = set(filter(None, kayit.split(","))) if kayit is not None else kazanilan
        self._fresh_badges = kazanilan - gorulen
        self._store.set_setting(SEEN_BADGES_KEY, ",".join(sorted(kazanilan)))
        self._badge_wall.set_page(0)

        # Rozetler kaydedildikten sonra: XP onlardan toplanıyor. Burada
        # kaydedilmiyor (`record=False`); seviye atlama kartını ana pencere
        # çıkarıyor, burada tüketilirse kart hiç çıkmazdı.
        self._levels = level_core.refresh(
            self._catalog, self._store, content_dir(), record=False
        )
        self._progress.set_ratio(self._levels.state.ratio)

        self.retranslate()
        if self._fresh_badges:
            ilk = sorted(self._fresh_badges, key=lambda i: self._badge_wall.page_of(i))[0]
            self._badge_wall.set_page(self._badge_wall.page_of(ilk))
            QTimer.singleShot(250, lambda: self._badge_wall.celebrate(
                self._fresh_badges, self._language.t_upper("profile.badge_new")))

    def _render_started(self) -> None:
        """"Başlangıç: 2 Eylül 2026" — ay adı dilde yazılı (prototip)."""
        ham = getattr(self, "_started_raw", "")
        try:
            gun = date.fromisoformat(ham[:10])
        except ValueError:
            self._started.setText("")
            return
        t = self._language.t
        if self._language.language == "tr":
            metin = f"{gun.day} {t(f'month_long.{gun.month}')} {gun.year}"
        else:
            metin = f"{t(f'month_long.{gun.month}')} {gun.day}, {gun.year}"
        self._started.setText(t("profile.member_since", date=metin))

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

    def _render_level(self) -> None:
        """Seviye satırı, XP çubuğunun ipucu ve unvan düğmesi."""
        t = self._language.t
        durum = self._levels.state
        self._progress_caption.setText(t("level.label", level=durum.level))
        if durum.need:
            self._progress_percent.setText(t("level.xp", into=durum.into, need=durum.need))
            ipucu = t("level.tooltip", xp=durum.xp, left=durum.need - durum.into)
        else:
            self._progress_percent.setText(t("level.max"))
            ipucu = t("level.tooltip_max", xp=durum.xp)
        for parca in (self._progress, self._progress_caption, self._progress_percent):
            parca.setToolTip(ipucu)

        secili = level_core.selected_tag(self._store, self._levels.tags)
        tanim = next((u for u in self._tag_list if u.get("id") == secili), None)
        self._tag_button.setText(
            self._language.pick(tanim.get("title"), secili) if tanim else t("tags.choose")
        )
        self._tag_button.setToolTip(t("tags.button_tip"))
        bos = "false" if tanim else "true"
        if self._tag_button.property("empty") != bos:
            self._tag_button.setProperty("empty", bos)
            self._tag_button.style().unpolish(self._tag_button)
            self._tag_button.style().polish(self._tag_button)

    def _open_tags(self) -> None:
        """Unvan penceresini açar; seçilen unvan hemen kullanılıyor."""
        from .modal import Backdrop
        from .tag_dialog import TagDialog

        kok = self.window()
        perde = Backdrop(kok)
        perde.show()
        onceki = level_core.selected_tag(self._store, self._levels.tags)
        dialog = TagDialog(
            self._language, self._tag_list, self._levels.tags, onceki, self._mode, kok
        )
        kabul = dialog.exec()
        perde.deleteLater()
        if kabul and dialog.selected != onceki:
            level_core.select_tag(self._store, dialog.selected)
            self._render_level()

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
        self._avatar.set_ring(palette["surface"], palette["accent"], palette["accent_second"])

    # --- tema ve dil ------------------------------------------------------

    def set_mode(self, mode: str) -> None:
        self._mode = mode
        self._identity_card.set_mode(mode)
        refresh_shadow(self._badges_card, mode)
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
        self._edit_button.setText("  " + t("profile.edit_title"))
        self._render_started()
        self._refresh_avatar()
        self._refresh_name()

        self._render_level()

        self._badges_title.setText(t("profile.badges"))
        kazanilan = sum(1 for b in self._badge_list if b.earned)
        for anahtar, deger, ad in (
            ("badges", f"{kazanilan}/{len(self._badge_list)}", t("profile.mini_badges")),
            ("streak", str(self._store.streak()), t("profile.mini_streak")),
            ("sections", str(self._completed), t("profile.mini_sections")),
        ):
            self._minis[anahtar][0].setText(deger)
            self._minis[anahtar][1].setText(ad)
        p = PALETTES.get(self._mode, PALETTES["light"])
        self._badge_wall.set_badges(
            self._badge_list,
            lambda b: self._language.pick(b.title),
            self._badge_tooltip,
            (p["text_inverse"], p["text_muted"]),
        )
        self._refresh_paging()

        self._activity_title.setText(t("profile.activity"))
        self._refresh_activity_summary()
        self._legend_less.setText(t("profile.activity_less"))
        self._legend_more.setText(t("profile.activity_more"))

        self._graph.set_labels(
            [t(f"month.{i}") for i in range(1, 13)],
            [t(f"weekday.{i}") for i in range(7)],
        )
        self._paint_graph()
