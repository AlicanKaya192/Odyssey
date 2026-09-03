"""Uygulama simgesini üretir.

`app/resources/appicon.py` içindeki SVG'yi alıp Windows'un beklediği `.ico`
dosyasını ve önizleme için bir PNG yazar. Tasarım değişince bu script tekrar
çalıştırılır.

Ayrıca **Discord** için iki dosya üretiyor. Discord'un Rich Presence
varlıkları en az 512x512 olmak zorunda; uygulamanın 256x256 simgesi
yüklenmeye çalışıldığında portal kabul etmiyor. Bu dosyalar uygulamanın
içinde kullanılmıyor, yalnızca Developer Portal'a elle yükleniyor:

- `discord-odyssey-1024.png` — Rich Presence varlığı (kare)
- `discord-cover-1024x576.png` — sohbet daveti kapak görseli (16:9)

`.ico` dosyası elle yazılıyor çünkü Qt bu biçimi kaydetmeyi desteklemiyor.
Biçim basit: bir başlık, her boyut için bir dizin girdisi ve arkasından PNG
verileri. Windows Vista'dan beri ICO içinde PNG saklanabiliyor.

Kullanım:
    .venv\\Scripts\\python tools/build_icon.py
"""

from __future__ import annotations

import os
import struct
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QSize, Qt  # noqa: E402
from PySide6.QtCore import QRectF  # noqa: E402
from PySide6.QtGui import (  # noqa: E402
    QBrush,
    QColor,
    QImage,
    QLinearGradient,
    QPainter,
)
from PySide6.QtSvg import QSvgRenderer  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from app.resources.appicon import icon_svg  # noqa: E402

# Windows'un kullandığı boyutlar. 256 görev çubuğunun büyük görünümü için.
SIZES = (16, 24, 32, 48, 64, 128, 256)

OUTPUT_DIR = PROJECT_ROOT / "app" / "resources"

# Discord'a yüklenecek dosyalar depoya girmiyor: uygulama onları
# kullanmıyor ve paketin içinde yer kaplamalarının bir anlamı yok.
DISCORD_DIR = PROJECT_ROOT / "Plan" / "discord"

# Discord Rich Presence varlığı: en az 512, önerilen 1024.
DISCORD_ASSET = 1024
# Sohbet daveti kapak görseli: 16:9.
DISCORD_COVER = (1024, 576)

# Simgenin 512'lik tuvalindeki görünen çizimin merkezi. Çizim tuvalde
# ortalı değil; kapakta ortalamak için bu nokta kullanılıyor.
CANVAS = 512
MARK_CENTER = (278, 259)


def render(svg: str, size: int) -> QImage:
    """SVG'yi istenen boyutta bir görüntüye çizer."""
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))

    image = QImage(QSize(size, size), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()

    return image


def to_png_bytes(image: QImage) -> bytes:
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return bytes(buffer.data())


def write_ico(path: Path, images: dict[int, bytes]) -> None:
    """PNG verilerini bir `.ico` kabına yazar."""
    count = len(images)

    # Başlık: ayrılmış(0), tür(1 = ikon), görüntü sayısı
    header = struct.pack("<HHH", 0, 1, count)

    # Dizin girdileri 16'şar bayt; veriler onların hemen ardından başlıyor.
    offset = len(header) + count * 16
    directory = b""
    payload = b""

    for size in sorted(images):
        data = images[size]
        # 256 piksel dizinde 0 olarak yazılır (tek bayta sığmadığı için).
        stored = 0 if size >= 256 else size
        directory += struct.pack(
            "<BBBBHHII",
            stored,      # genişlik
            stored,      # yükseklik
            0,           # palet rengi yok
            0,           # ayrılmış
            1,           # renk düzlemi
            32,          # piksel başına bit
            len(data),   # veri uzunluğu
            offset,      # verinin dosyadaki yeri
        )
        payload += data
        offset += len(data)

    path.write_bytes(header + directory + payload)


def render_cover(svg: str, width: int, height: int) -> QImage:
    """16:9 kapak: simgenin zemin rengi arkada, işaret ortada.

    Kare simgeyi doğrudan gerdirmek oranı bozuyor. Onun yerine zemin
    gradyanı bütün tuvali kaplıyor ve simge, köşe yuvarlaması olmadan
    ortaya çiziliyor.
    """
    image = QImage(QSize(width, height), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    # Zemin: simgenin kendi gradyanı, köşesiz ve tuvali kaplayan hâli.
    background = QLinearGradient(0, 0, width, height)
    background.setColorAt(0.0, QColor("#4F46E5"))
    background.setColorAt(1.0, QColor("#7C3AED"))
    painter.fillRect(0, 0, width, height, QBrush(background))

    # İşaret: kare simgenin zeminsiz hâli.
    #
    # Çizim kendi 512'lik tuvalinde **ortalı değil** — yol sol alttan sağ
    # üste gidiyor ve görünen kütlenin merkezi (278, 259) civarında.
    # Kareyi tuvalin ortasına koymak işareti hafif kaydırıyor; onun yerine
    # çizimin kendi merkezi kapağın merkezine oturtuluyor.
    mark = QSvgRenderer(QByteArray(mark_svg().encode("utf-8")))
    side = int(height * 0.90)
    scale = side / CANVAS
    left = (width - side) / 2 - (MARK_CENTER[0] - CANVAS / 2) * scale
    top = (height - side) / 2 - (MARK_CENTER[1] - CANVAS / 2) * scale
    mark.render(painter, QRectF(left, top, side, side))
    painter.end()

    return image


def mark_svg() -> str:
    """Simgenin zeminsiz hâli: yalnızca yol, düğümler ve yıldız."""
    full = icon_svg()
    # Zemin dikdörtgeni çıkarılıyor; geri kalan çizim aynı tuvalde duruyor.
    start = full.index("<rect")
    end = full.index(">", start) + 1
    return full[:start] + full[end:]


def main() -> int:
    application = QApplication(sys.argv)  # noqa: F841 (Qt için gerekli)

    svg = icon_svg()
    images = {size: to_png_bytes(render(svg, size)) for size in SIZES}

    ico_path = OUTPUT_DIR / "icon.ico"
    write_ico(ico_path, images)

    png_path = OUTPUT_DIR / "icon.png"
    png_path.write_bytes(images[256])

    svg_path = OUTPUT_DIR / "icon.svg"
    svg_path.write_text(svg, encoding="utf-8")

    print(f"Yazıldı: {ico_path.name}  ({ico_path.stat().st_size:,} bayt, "
          f"{len(SIZES)} boyut: {', '.join(str(s) for s in SIZES)})")
    print(f"Yazıldı: {png_path.name}  ({png_path.stat().st_size:,} bayt)")
    print(f"Yazıldı: {svg_path.name}")

    # --- Discord Developer Portal'a elle yüklenecek dosyalar ------------
    DISCORD_DIR.mkdir(parents=True, exist_ok=True)

    asset_path = DISCORD_DIR / "discord-odyssey-1024.png"
    asset_path.write_bytes(to_png_bytes(render(svg, DISCORD_ASSET)))

    cover_path = DISCORD_DIR / "discord-cover-1024x576.png"
    cover_path.write_bytes(to_png_bytes(render_cover(svg, *DISCORD_COVER)))

    print(f"Yazıldı: {asset_path}  ({DISCORD_ASSET}x{DISCORD_ASSET})")
    print(f"Yazıldı: {cover_path}  ({DISCORD_COVER[0]}x{DISCORD_COVER[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
