"""Profil fotoğrafı.

Kullanıcının seçtiği görsel `%APPDATA%\\Odyssey\\avatar.png` altına
**kopyalanıyor** — özgün dosyanın yolu saklanmıyor. Sebebi: yol saklansaydı
kullanıcı o dosyayı taşıdığında ya da sildiğinde fotoğraf kayboluyordu.
Kopya veri klasöründe durduğu için güncellemelerde de yerinde kalıyor.

Görsel kaydedilirken kareye kırpılıp küçültülüyor. Telefondan gelen bir
fotoğraf 5 MB olabiliyor; ekranda 96 pikselden büyük hiç gösterilmediği için
o boyutu taşımanın anlamı yok.

Hiçbir yere gönderilmiyor: dosya kullanıcının kendi bilgisayarında kalıyor.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap

from ..paths import user_data_dir

# Saklanan görselin kenar uzunluğu. Ekranda en büyük 96 piksel gösteriliyor;
# yüksek yoğunluklu ekranlar için iki katı yeter.
STORED_SIZE = 256

# Seçilebilecek dosya türleri. Qt bunların hepsini kendi okuyor, ek bir
# kütüphane gerekmiyor.
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".webp")


def avatar_path() -> Path:
    """Fotoğrafın saklandığı yer."""
    return user_data_dir() / "avatar.png"


def has_avatar() -> bool:
    return avatar_path().exists()


def load_avatar() -> QPixmap | None:
    """Kayıtlı fotoğrafı verir; yoksa `None`."""
    path = avatar_path()
    if not path.exists():
        return None
    pixmap = QPixmap(str(path))
    return None if pixmap.isNull() else pixmap


def save_avatar(source: str | Path) -> bool:
    """Seçilen görseli kareye kırpıp veri klasörüne kaydeder.

    Kırpma ortadan alınıyor: portre bir fotoğrafta yüz genelde ortada
    oluyor, üstten ya da alttan kesmek kafayı kırpıyor.

    Okunamayan bir dosyada `False` dönüyor; çağıran kullanıcıya bunu
    söylüyor.
    """
    image = QImage(str(source))
    if image.isNull():
        return False

    kenar = min(image.width(), image.height())
    kare = image.copy(
        (image.width() - kenar) // 2,
        (image.height() - kenar) // 2,
        kenar,
        kenar,
    )
    kucuk = kare.scaled(
        STORED_SIZE,
        STORED_SIZE,
        Qt.AspectRatioMode.IgnoreAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )

    hedef = avatar_path()
    hedef.parent.mkdir(parents=True, exist_ok=True)
    return bool(kucuk.save(str(hedef), "PNG"))


def clear_avatar() -> None:
    """Fotoğrafı siler; baş harfler geri geliyor."""
    path = avatar_path()
    if path.exists():
        path.unlink()
