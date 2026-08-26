"""Uygulama simgesini üretir.

`app/resources/appicon.py` içindeki SVG'yi alıp Windows'un beklediği `.ico`
dosyasını ve önizleme için bir PNG yazar. Tasarım değişince bu script tekrar
çalıştırılır.

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
from PySide6.QtGui import QImage, QPainter  # noqa: E402
from PySide6.QtSvg import QSvgRenderer  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from app.resources.appicon import icon_svg  # noqa: E402

# Windows'un kullandığı boyutlar. 256 görev çubuğunun büyük görünümü için.
SIZES = (16, 24, 32, 48, 64, 128, 256)

OUTPUT_DIR = PROJECT_ROOT / "app" / "resources"


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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
