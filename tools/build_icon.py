"""Uygulama simgesini üretir.

`app/resources/appicon.py` içindeki çizimi (sentor, QPainter) alıp Windows'un
beklediği `.ico` dosyasını ve bildirimde kullanılan PNG'yi yazar. Tasarım
değişince bu script tekrar çalıştırılır.

**Ekransız kipte (`QT_QPA_PLATFORM=offscreen`) çalıştırılmaz:** orada yazı
tipleri yüklenmiyor ve Discord kapağındaki ODYSSEY yazısı kutu kutu
çıkıyordu.

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

import struct
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtCore import QBuffer, QIODevice, QSize, Qt  # noqa: E402
from PySide6.QtGui import QImage, QPainter  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from app.resources.appicon import paint_banner, paint_cover, paint_icon  # noqa: E402

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

# README'nin başındaki banner, iki dilde (README.md / README.tr.md).
BANNER_DIR = PROJECT_ROOT / "docs" / "media"
BANNER = (1600, 480)
BANNER_TEXT = {
    "en": ("Learn Python, Git, algorithms, data science, machine learning, SQL, "
           "APIs, Docker, big data and the mathematics behind them.",
           "12 paths  ·  353 sections  ·  Offline  ·  Open source  ·  Turkish & English"),
    "tr": ("Python, Git, algoritmalar, veri bilimi, makine öğrenmesi, SQL, API, "
           "Docker, büyük veri ve arkalarındaki matematik; adım adım.",
           "12 patika  ·  353 bölüm  ·  Çevrimdışı  ·  Açık kaynak  ·  Türkçe ve İngilizce"),
}


def render(size: int, rounded: bool = True) -> QImage:
    """Simgeyi istenen boyutta bir görüntüye çizer."""
    image = QImage(QSize(size, size), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    paint_icon(painter, size, rounded)
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


def render_cover(width: int, height: int) -> QImage:
    """16:9 kapak: açılış sahnesinin özeti (sentor, hedef, ODYSSEY)."""
    image = QImage(QSize(width, height), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    paint_cover(painter, width, height)
    painter.end()
    return image


def render_banner(tagline: str, subline: str) -> QImage:
    width, height = BANNER
    image = QImage(QSize(width, height), QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    paint_banner(painter, width, height, tagline, subline)
    painter.end()
    return image


def main() -> int:
    application = QApplication(sys.argv)  # noqa: F841 (Qt için gerekli)

    images = {size: to_png_bytes(render(size)) for size in SIZES}

    ico_path = OUTPUT_DIR / "icon.ico"
    write_ico(ico_path, images)

    png_path = OUTPUT_DIR / "icon.png"
    png_path.write_bytes(images[256])

    print(f"Yazıldı: {ico_path.name}  ({ico_path.stat().st_size:,} bayt, "
          f"{len(SIZES)} boyut: {', '.join(str(s) for s in SIZES)})")
    print(f"Yazıldı: {png_path.name}  ({png_path.stat().st_size:,} bayt)")

    # --- Discord Developer Portal'a elle yüklenecek dosyalar ------------
    DISCORD_DIR.mkdir(parents=True, exist_ok=True)

    asset_path = DISCORD_DIR / "discord-odyssey-1024.png"
    # Köşesiz: Discord kendisi yuvarlıyor.
    asset_path.write_bytes(to_png_bytes(render(DISCORD_ASSET, rounded=False)))

    cover_path = DISCORD_DIR / "discord-cover-1024x576.png"
    cover_path.write_bytes(to_png_bytes(render_cover(*DISCORD_COVER)))

    print(f"Yazıldı: {asset_path}  ({DISCORD_ASSET}x{DISCORD_ASSET})")
    print(f"Yazıldı: {cover_path}  ({DISCORD_COVER[0]}x{DISCORD_COVER[1]})")

    for lang, (tagline, subline) in BANNER_TEXT.items():
        banner_path = BANNER_DIR / f"banner_{lang}.png"
        banner_path.write_bytes(to_png_bytes(render_banner(tagline, subline)))
        print(f"Yazıldı: {banner_path.name}  ({BANNER[0]}x{BANNER[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
