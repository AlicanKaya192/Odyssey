"""Profil kartını resim olarak kaydetmek (paylaşım kartı).

Alican istedi: kişi seviyesini, unvanını, rozetlerini ve son bir yıldaki
çalışmasını (GitHub'daki katkı tablosu gibi) LinkedIn gibi bir yerde
paylaşabilsin. Sol altta Odyssey'in, sağ altta kişinin kendi GitHub adresi
(profil düzenleme penceresinde giriliyor). Kart 1200 × 780 piksel; temadan
bağımsız, açılışın morunda. Her şey bilgisayarda çiziliyor, hiçbir yere
gönderilmiyor.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QImage, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QApplication

WIDTH = 1200
HEIGHT = 780
BG_TOP = QColor("#2A2160")
BG_BOTTOM = QColor("#121026")
ACCENT = QColor("#8B84FF")
TEXT = QColor("#F4F3FF")
MUTED = QColor("#B9B4E6")
CARD = QColor(255, 255, 255, 18)
MAX_MEDALS = 10
WEEKS = 53
PROJECT_URL = "github.com/AlicanKaya192/Odyssey"
GITHUB_KEY = "github_username"

# GitHub kullanıcı adı: harf, rakam ve tek tire; tireyle başlayıp bitemez;
# en fazla 39 karakter.
_GITHUB = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}$")


def normalize_github(text: str) -> str | None:
    """Girilen metinden GitHub kullanıcı adını çıkarır; geçersizse None, boşsa "".

    `https://github.com/ad`, `github.com/ad/`, `@ad` ve düz `ad` kabul.
    """
    metin = (text or "").strip()
    if not metin:
        return ""
    metin = re.sub(r"^(https?://)?(www\.)?github\.com/", "", metin, flags=re.I)
    metin = metin.strip("/").lstrip("@").split("/")[0].split("?")[0]
    return metin if _GITHUB.match(metin) else None


@dataclass
class CardData:
    name: str
    tag: str
    level: int
    xp: int
    into: int
    need: int
    sections_done: int
    sections_total: int
    exercises_solved: int
    streak: int
    badges_earned: int
    badges_total: int
    medals: list[QPixmap] = field(default_factory=list)
    avatar: Path | None = None
    activity: dict[str, int] = field(default_factory=dict)
    github: str = ""
    labels: dict = field(default_factory=dict)
    today: date | None = None


def _font(px: int, bold: bool = False) -> QFont:
    f = QFont(QApplication.font().family())
    f.setPixelSize(px)
    f.setBold(bold)
    return f


def _shade(count: int) -> QColor:
    """Etkinlik karesinin rengi: boş, sonra dört kademe mor."""
    if count <= 0:
        return QColor(255, 255, 255, 20)
    if count == 1:
        return QColor(139, 132, 255, 90)
    if count <= 3:
        return QColor(139, 132, 255, 150)
    if count <= 6:
        return QColor(139, 132, 255, 215)
    return QColor("#C9C2FF")


def render(data: CardData) -> QImage:
    img = QImage(WIDTH, HEIGHT, QImage.Format.Format_ARGB32_Premultiplied)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    zemin = QLinearGradient(0, 0, WIDTH * 0.4, HEIGHT)
    zemin.setColorAt(0, BG_TOP)
    zemin.setColorAt(1, BG_BOTTOM)
    p.fillRect(img.rect(), zemin)
    L = data.labels

    # Sağ üst: logo ve ad.
    from ..resources import appicon

    p.save()
    p.translate(WIDTH - 60 - 56, 44)
    appicon.paint_icon(p, 60)
    p.restore()
    p.setPen(TEXT)
    p.setFont(_font(26, True))
    p.drawText(QRectF(WIDTH - 420, 44, 420 - 60 - 56 - 16, 60),
               Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, "Odyssey")

    # Sol: fotoğraf ya da baş harfler.
    cx, cy, r = 146, 156, 80
    p.setPen(QPen(ACCENT, 6))
    p.setBrush(QColor("#3B3180"))
    p.drawEllipse(QPointF(cx, cy), r + 4, r + 4)
    yol = QPainterPath()
    yol.addEllipse(QPointF(cx, cy), r, r)
    foto = QPixmap(str(data.avatar)) if data.avatar and data.avatar.is_file() else QPixmap()
    if not foto.isNull():
        p.save()
        p.setClipPath(yol)
        olcek = foto.scaled(2 * r, 2 * r, Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                            Qt.TransformationMode.SmoothTransformation)
        p.drawPixmap(int(cx - olcek.width() / 2), int(cy - olcek.height() / 2), olcek)
        p.restore()
    else:
        harfler = "".join(w[0] for w in data.name.split()[:2]).upper() or "?"
        p.setPen(TEXT)
        p.setFont(_font(60, True))
        p.drawText(QRectF(cx - r, cy - r, 2 * r, 2 * r), Qt.AlignmentFlag.AlignCenter, harfler)

    # Ad, unvan, seviye.
    x0 = 280
    p.setPen(TEXT)
    p.setFont(_font(52, True))
    p.drawText(QRectF(x0, 72, WIDTH - x0 - 140, 68), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
               data.name or L.get("anonymous", ""))
    if data.tag:
        p.setFont(_font(21, True))
        genislik = p.fontMetrics().horizontalAdvance(data.tag) + 36
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(139, 132, 255, 60))
        p.drawRoundedRect(QRectF(x0, 146, genislik, 38), 19, 19)
        p.setPen(QColor("#D9D6FF"))
        p.drawText(QRectF(x0, 146, genislik, 38), Qt.AlignmentFlag.AlignCenter, data.tag)
    y = 200
    p.setPen(TEXT)
    p.setFont(_font(27, True))
    p.drawText(QRectF(x0, y, 400, 34), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
               L.get("level", "").format(level=data.level))
    p.setPen(MUTED)
    p.setFont(_font(20))
    p.drawText(QRectF(x0, y, WIDTH - x0 - 60, 34), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
               L.get("xp", "").format(xp=data.xp))
    cubuk = QRectF(x0, y + 42, WIDTH - x0 - 60, 14)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(255, 255, 255, 30))
    p.drawRoundedRect(cubuk, 7, 7)
    oran = 1.0 if not data.need else max(0.0, min(1.0, data.into / data.need))
    if oran > 0:
        dolu = QLinearGradient(cubuk.left(), 0, cubuk.right(), 0)
        dolu.setColorAt(0, QColor("#6D63F5"))
        dolu.setColorAt(1, QColor("#B6A8FF"))
        p.setBrush(dolu)
        p.drawRoundedRect(QRectF(cubuk.left(), cubuk.top(), max(14, cubuk.width() * oran), cubuk.height()), 7, 7)

    # Sayılar: dört kutu.
    kutular = [
        (f"{data.sections_done}/{data.sections_total}", L.get("sections", "")),
        (str(data.exercises_solved), L.get("exercises", "")),
        (str(data.streak), L.get("streak", "")),
        (f"{data.badges_earned}/{data.badges_total}", L.get("badges", "")),
    ]
    kx, ky, kh, ara = 60, 290, 108, 20
    kg = (WIDTH - 120 - 3 * ara) / 4
    for i, (deger, ad) in enumerate(kutular):
        r_ = QRectF(kx + i * (kg + ara), ky, kg, kh)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(CARD)
        p.drawRoundedRect(r_, 18, 18)
        p.setPen(TEXT)
        p.setFont(_font(38, True))
        p.drawText(QRectF(r_.left(), r_.top() + 12, r_.width(), 50), Qt.AlignmentFlag.AlignCenter, deger)
        p.setPen(MUTED)
        p.setFont(_font(18))
        p.drawText(QRectF(r_.left(), r_.top() + 64, r_.width(), 32), Qt.AlignmentFlag.AlignCenter, ad)

    # Rozetler: son kazanılanlardan en fazla on tanesi.
    mx, my, ms = 60, 428, 64
    for i, medal in enumerate(data.medals[:MAX_MEDALS]):
        p.drawPixmap(QRectF(mx + i * (ms + 12), my, ms, ms), medal, QRectF(medal.rect()))

    # Son bir yılın etkinliği (GitHub'daki katkı tablosu gibi): 53 hafta,
    # her sütun Pazartesi'den Pazar'a; son sütun bu hafta.
    bugun = data.today or date.today()
    ilk = bugun - timedelta(days=bugun.weekday()) - timedelta(weeks=WEEKS - 1)
    gx, gy, kare, aralik = 60, 540, 15, 3
    adim = kare + aralik
    calisilan = sum(1 for g, n in data.activity.items() if n > 0 and ilk.isoformat() <= g <= bugun.isoformat())
    p.setPen(MUTED)
    p.setFont(_font(18, True))
    p.drawText(QRectF(gx, gy - 34, 600, 26), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
               L.get("activity", ""))
    p.setFont(_font(18))
    p.drawText(QRectF(gx, gy - 34, WEEKS * adim - aralik, 26),
               Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
               L.get("active_days", "").format(days=calisilan))
    p.setPen(Qt.PenStyle.NoPen)
    for hafta in range(WEEKS):
        for gun in range(7):
            o_gun = ilk + timedelta(weeks=hafta, days=gun)
            if o_gun > bugun:
                continue
            p.setBrush(_shade(data.activity.get(o_gun.isoformat(), 0)))
            p.drawRoundedRect(QRectF(gx + hafta * adim, gy + gun * adim, kare, kare), 4, 4)
    # Kademe açıklaması (az → çok), tablonun sağında.
    lx = gx + WEEKS * adim + 22
    p.setPen(MUTED)
    p.setFont(_font(16))
    p.drawText(QRectF(lx, gy, 120, 22), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, L.get("less", ""))
    for i, n in enumerate((0, 1, 2, 4, 7)):
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(_shade(n))
        p.drawRoundedRect(QRectF(lx, gy + 28 + i * adim, kare, kare), 4, 4)
    p.setPen(MUTED)
    p.drawText(QRectF(lx, gy + 28 + 5 * adim, 120, 22), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
               L.get("more", ""))

    # Alt köşeler: solda Odyssey, sağda kişinin GitHub'ı.
    alt = HEIGHT - 56
    p.setPen(QColor(255, 255, 255, 40))
    p.drawLine(QPointF(60, alt - 16), QPointF(WIDTH - 60, alt - 16))
    p.setFont(_font(19, True))
    p.setPen(MUTED)
    p.drawText(QRectF(60, alt, 560, 34), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, PROJECT_URL)
    if data.github:
        p.setPen(TEXT)
        p.drawText(QRectF(WIDTH - 620, alt, 560, 34), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                   f"github.com/{data.github}")
    p.end()
    return img
