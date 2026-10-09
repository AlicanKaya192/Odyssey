"""Güncellemeden sonraki ilk açılışta "Neler yeni?" penceresi.

Alican istedi: güncellemeden sonra beta uyarısı yerine üstte "ODYSSEY X.Y.Z
GÜNCELLEMESİ" yazan bir banner, altında en önemli beş yenilik ve "tüm
sürüm notları" bağlantısı (programın Sürüm Notları ekranına götürüyor).
İlk kez kuran kişi hoş geldiniz penceresini görüyor (`main.py`, `welcome.py`).

Yenilikler sürüm notundan (`CHANGELOG.<dil>.md`) okunuyor: bu sürümün
kalın başlıklı maddeleri, yazıldıkları sırayla (sürüm notunda en önemli
olan en üstte yazılıyor; önce içerik, sonra program).
"""

from __future__ import annotations

import re

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QPainter, QPainterPath
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from ..core.language import LanguageManager
from ..paths import install_root
from ..resources.theme.tokens import SPACING
from ..version import APP_VERSION
from . import modal

LIMIT = 5
WIDTH = 620
BANNER_RATIO = 480 / 1600
_BOLD = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$", re.S)


def _plain(text: str) -> str:
    return re.sub(r"[`*]", "", text).strip()


def total_changes(language: str) -> int:
    """Bu sürümün sürüm notundaki bütün maddeler (kalın başlıklı ya da değil)."""
    from .release_view import parse_changelog

    ad = "CHANGELOG.md" if language == "tr" else f"CHANGELOG.{language}.md"
    yol = install_root() / ad
    if not yol.exists():
        yol = install_root() / "CHANGELOG.md"
    for surum in parse_changelog(yol):
        if surum.version == APP_VERSION:
            return sum(len(maddeler) for _grup, maddeler in surum.groups)
    return 0


def highlights(language: str, limit: int = LIMIT) -> list[tuple[str, str]]:
    """Bu sürümün en fazla `limit` kalın başlıklı maddesi: (başlık, ilk cümle)."""
    from .release_view import parse_changelog

    ad = "CHANGELOG.md" if language == "tr" else f"CHANGELOG.{language}.md"
    yol = install_root() / ad
    if not yol.exists():
        yol = install_root() / "CHANGELOG.md"
    for surum in parse_changelog(yol):
        if surum.version != APP_VERSION:
            continue
        sonuc: list[tuple[str, str]] = []
        for _grup, maddeler in surum.groups:
            for madde in maddeler:
                m = _BOLD.match(madde.strip())
                if not m:
                    continue
                baslik = _plain(m.group(1)).rstrip(".")
                govde = _plain(m.group(2))
                cumle = re.split(r"(?<=[.!?])\s", govde, maxsplit=1)[0] if govde else ""
                if len(cumle) > 130:
                    cumle = cumle[:127].rsplit(" ", 1)[0].rstrip(",;:") + "…"
                sonuc.append((baslik, cumle))
                if len(sonuc) >= limit:
                    return sonuc
        return sonuc
    return []


def paint_update_banner(p: QPainter, w: float, h: float, version_text: str) -> None:
    """Pencerenin üst bandı: sentor, menderes bordürleri, "Odyssey" ve sürüm.

    README banner'ı 1600 × 480 için ölçülmüştü; küçültülünce bordürler
    taşıyor, zemin çizgisiyle çakışıyor ve yazı yerinden kayıyordu (Alican).
    Burada her ölçü bandın yüksekliğinden; bordürler tam birim ve ortalı.
    """
    import random

    from PySide6.QtCore import QPointF
    from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPen, QRadialGradient

    from ..resources import appicon as A
    from ..resources.theme.tokens import FONTS

    I = A._colors()  # noqa: SLF001
    zemin = QRadialGradient(QPointF(w * .30, h * .30), w * .8)
    zemin.setColorAt(0.0, I.GROUND_IN)
    zemin.setColorAt(0.5, I.GROUND_MID)
    zemin.setColorAt(1.0, I.GROUND_OUT)
    p.fillRect(QRectF(0, 0, w, h), zemin)

    def menderes(ust: float, yukseklik: float, birim: float, kalem: float) -> None:
        kenar = h * .09
        adet = int((w - 2 * kenar) // birim)
        sol = (w - adet * birim + birim * .25) / 2
        A._meander(p, sol, ust, adet * birim, birim, yukseklik, A._alpha(I.INK, .85), kalem)  # noqa: SLF001

    birim, cizgi = h * .075, max(1.4, h * .011)
    ust_bordur = h * .07
    menderes(ust_bordur, h * .055, birim, cizgi)

    # Yıldızlar yalnızca gökte, bordürle zemin arasında.
    yer = h * .80
    rnd = random.Random(7)
    p.setPen(Qt.PenStyle.NoPen)
    for _ in range(26):
        x, y = rnd.uniform(0, w), rnd.uniform(h * .17, h * .55)
        r = rnd.uniform(.7, 1.6)
        p.setBrush(A._alpha(I.SPARK, rnd.uniform(.25, .6)))  # noqa: SLF001
        p.drawEllipse(QPointF(x, y), r, r)

    for oran, yuk, renk in ((.40, h * .10, A._alpha(I.HILL, .45)), (.55, h * .06, A._alpha(I.HILL, .7))):  # noqa: SLF001
        tepe = QPainterPath(QPointF(0, yer))
        adim, xx = w * oran, -w * oran * .3
        while xx < w + adim:
            tepe.cubicTo(xx + adim * .2, yer - yuk, xx + adim * .4, yer - yuk * 1.15, xx + adim * .55, yer - yuk * .3)
            tepe.cubicTo(xx + adim * .7, yer, xx + adim * .85, yer - yuk * .6, xx + adim, yer)
            xx += adim
        tepe.lineTo(w, yer + 2)
        tepe.lineTo(0, yer + 2)
        tepe.closeSubpath()
        p.fillPath(tepe, renk)
    p.fillRect(QRectF(0, yer, w, h - yer), A._alpha(I.GROUND_OUT, .55))  # noqa: SLF001
    p.setPen(QPen(I.INK, max(1.5, h * .014)))
    p.drawLine(QPointF(0, yer), QPointF(w, yer))
    # Alt bordür zemin şeridinin tam ortasında.
    alt_y = h * .055
    menderes(yer + (h - yer - alt_y) / 2, alt_y, birim, cizgi)

    # Sentor: sol tarafta, ay diskinin önünde, toynaklar zemin çizgisinde.
    olcek = h * .56 / (A.FIG_BOTTOM - A.FIG_TOP)
    fx = w * .06 - A.FIG_LEFT * olcek
    ay = QPointF(fx + 400 * olcek, yer - 250 * olcek)
    r = 150 * olcek
    hale = QRadialGradient(ay, r * 2)
    hale.setColorAt(0, A._alpha(I.SPARK, .3))  # noqa: SLF001
    hale.setColorAt(1, A._alpha(I.SPARK, 0))  # noqa: SLF001
    p.fillRect(QRectF(0, 0, w, h), hale)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(A._alpha(I.RING_LIGHT, .5))  # noqa: SLF001
    p.drawEllipse(ay, r, r)
    A._figure(p, fx, yer + 3 * olcek, olcek, True)  # noqa: SLF001
    sentor_sag = fx + A.FIG_RIGHT * olcek

    # Yazı bloğu: sentorun sağındaki alanın ortasında; bordürle zemin
    # çizgisi arasında dikey olarak ortalı. Başlık, altında kısa bir
    # menderes, altında sürüm.
    alan_sol, alan_sag = sentor_sag + h * .10, w - h * .12
    alan_ust, alan_alt = ust_bordur + h * .055 + h * .05, yer - h * .05
    orta = (alan_sol + alan_sag) / 2

    aile = FONTS["display"].split(",")[0].strip().strip('"')
    baslik = QFont(aile)
    baslik.setPixelSize(int(h * .26))
    baslik.setWeight(QFont.Weight.DemiBold)
    baslik.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, h * .01)
    surum = QFont(FONTS["ui"].split(",")[0].strip().strip('"'))
    surum.setPixelSize(int(h * .095))
    surum.setWeight(QFont.Weight.Bold)
    surum.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, h * .008)
    mb, ms = QFontMetricsF(baslik), QFontMetricsF(surum)
    bosluk, mend_y = h * .045, h * .045
    blok = mb.ascent() + mb.descent() * .6 + bosluk + mend_y + bosluk + ms.ascent()
    taban = alan_ust + (alan_alt - alan_ust - blok) / 2 + mb.ascent()

    p.setFont(baslik)
    p.setPen(I.INK)
    gb = mb.horizontalAdvance("Odyssey")
    p.drawText(QPointF(orta - gb / 2, taban), "Odyssey")
    mend_ust = taban + mb.descent() * .6 + bosluk
    m_birim = h * .062
    m_adet = max(1, int(gb // m_birim))
    A._meander(p, orta - m_adet * m_birim / 2 + m_birim * .125, mend_ust, m_adet * m_birim,  # noqa: SLF001
               m_birim, mend_y, I.INK, max(1.4, h * .012))
    p.setFont(surum)
    p.setPen(QColor(I.INK))
    gs = ms.horizontalAdvance(version_text)
    p.drawText(QPointF(orta - gs / 2, mend_ust + mend_y + bosluk + ms.ascent()), version_text)


class _Banner(QWidget):
    """Pencerenin üst bandı (`paint_update_banner`)."""

    def __init__(self, tagline: str) -> None:
        super().__init__()
        self._tagline = tagline
        self.setFixedHeight(int(WIDTH * BANNER_RATIO))

    def paintEvent(self, event) -> None:  # noqa: N802
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        # Pencerenin üst köşeleri yuvarlak (modal, 22 px); band taşmasın.
        yol = QPainterPath()
        r, w, h = 21.0, float(self.width()), float(self.height())
        yol.moveTo(0, h)
        yol.lineTo(0, r)
        yol.quadTo(0, 0, r, 0)
        yol.lineTo(w - r, 0)
        yol.quadTo(w, 0, w, r)
        yol.lineTo(w, h)
        yol.closeSubpath()
        p.setClipPath(yol)
        paint_update_banner(p, w, h, self._tagline)
        p.end()


class WhatsNewDialog(QDialog):
    """Banner, en önemli yenilikler, "tüm sürüm notları" ve "devam et"."""

    def __init__(self, language: LanguageManager, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language = language
        self.wants_notes = False
        t = language.t
        modal.prepare(self)
        self.setFixedWidth(WIDTH)

        duzen = QVBoxLayout(self)
        duzen.setContentsMargins(1, 1, 1, SPACING["lg"])
        duzen.setSpacing(0)
        duzen.addWidget(_Banner(t("whatsnew.banner", version=APP_VERSION)))

        govde = QVBoxLayout()
        govde.setContentsMargins(SPACING["lg"] + 4, SPACING["lg"], SPACING["lg"] + 4, 0)
        govde.setSpacing(SPACING["sm"])
        baslik = QLabel(t("whatsnew.heading"))
        baslik.setProperty("role", "dialog-title")
        govde.addWidget(baslik)

        from ..widgets.effects import theme_palette

        renk = theme_palette()
        maddeler = highlights(language.language)
        for ad, cumle in maddeler:
            satir = QLabel(
                f"<span style='color:{renk['text']}; font-weight:700'>•&nbsp;&nbsp;{ad}</span>"
                + (f"<br><span style='color:{renk['text_muted']}'>{cumle}</span>" if cumle else ""))
            satir.setTextFormat(Qt.TextFormat.RichText)
            satir.setWordWrap(True)
            satir.setProperty("role", "whatsnew-item")
            govde.addWidget(satir)
        if not maddeler:
            bos = QLabel(t("whatsnew.empty"))
            bos.setProperty("role", "muted")
            govde.addWidget(bos)
        # Beş madde "bu kadar mı?" dedirtmesin: kaç yenilik daha olduğu yazıyor.
        kalan = max(0, total_changes(language.language) - len(maddeler))
        if kalan:
            daha = QLabel(t("whatsnew.more", count=kalan))
            daha.setProperty("role", "whatsnew-more")
            daha.setStyleSheet(f"color: {renk['accent']}; font-weight: 600; padding-top: 4px;")
            govde.addWidget(daha)

        govde.addSpacing(SPACING["md"])
        dugmeler = QHBoxLayout()
        self._notes_button = QPushButton(t("whatsnew.see_all") if kalan else t("whatsnew.all_notes"))
        self._notes_button.setProperty("variant", "ghost")
        self._notes_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._notes_button.clicked.connect(self._open_notes)
        dugmeler.addWidget(self._notes_button)
        dugmeler.addStretch(1)
        devam = QPushButton(t("whatsnew.continue"))
        devam.setProperty("variant", "primary")
        devam.setCursor(Qt.CursorShape.PointingHandCursor)
        devam.clicked.connect(self.accept)
        devam.setDefault(True)
        dugmeler.addWidget(devam)
        govde.addLayout(dugmeler)
        duzen.addLayout(govde)

    def _open_notes(self) -> None:
        self.wants_notes = True
        self.accept()

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(WIDTH, super().sizeHint().height())
