"""Arayüz ikonları.

İkonlar SVG yolu olarak gömülü tutuluyor: dosya bağımlılığı yok, internetten
bir şey çekilmiyor ve renk temaya göre çalışma anında değiştirilebiliyor.

Emoji kullanmıyoruz; emoji her Windows sürümünde farklı çiziliyor ve boyutu
kontrol edilemiyor.

Yol verileri Lucide ikon setinden (ISC lisansı, ticari kullanıma açık).
"""

from __future__ import annotations

from PySide6.QtCore import QByteArray, QSize, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

# Her ikon 24x24 tuval üzerine çizilmiş yollardan oluşuyor.
PATHS: dict[str, str] = {
    # --- tema ------------------------------------------------------------
    "sun": (
        '<circle cx="12" cy="12" r="4"/>'
        '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41'
        'M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>'
    ),
    "moon": (
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
    ),
    # --- rozet ikonları ---------------------------------------------
    "star": (
        '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'
    ),
    "flag": (
        '<path d="M4 22V3"/>'
        '<path d="M4 4h12l-2.5 4.5L16 13H4"/>'
    ),
    "trophy": (
        '<path d="M6 9H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h2"/>'
        '<path d="M18 9h2a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-2"/>'
        '<path d="M6 3h12v7a6 6 0 0 1-12 0V3z"/>'
        '<path d="M12 16v4"/>'
        '<path d="M8 20h8"/>'
    ),
    "calendar": (
        '<rect x="3" y="4" width="18" height="18" rx="2"/>'
        '<path d="M16 2v4M8 2v4M3 10h18"/>'
        '<path d="m9 16 2 2 4-4"/>'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "home": (
        '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>'
    ),
    "user": (
        '<circle cx="12" cy="8" r="4"/>'
        '<path d="M4 21c0-4 3.6-6 8-6s8 2 8 6"/>'
    ),
    # Megafon: gövde sola doğru açılan bir koni, altında tutamak. Önceki
    # çizim hoparlöre benziyordu; ses ikonuyla karışıyordu.
    "megaphone": (
        '<path d="m3 11 15-7v16L3 13z"/>'
        '<path d="M3 11H2.5A1.5 1.5 0 0 0 1 12.5v0A1.5 1.5 0 0 0 2.5 14H3z"/>'
        '<path d="M6 14v5a2 2 0 0 0 4 0v-3.6"/>'
        '<path d="M21 9v6"/>'
    ),
    "settings": (
        '<circle cx="12" cy="12" r="3"/>'
        '<path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-1.8-.3'
        '1.6 1.6 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1A1.6 1.6 0 0 0 9 19.4a1.6 1.6 0 0 0-1.8.3l-.1.1'
        'a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1'
        'A1.6 1.6 0 0 0 4.6 9a1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 1.8.3'
        'H9a1.6 1.6 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1'
        'a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8V9a1.6 1.6 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1'
        'a1.6 1.6 0 0 0-1.5 1z"/>'
    ),
    "arrow-left": '<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "play": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="10 8 16 12 10 16 10 8"/>'
    ),
    "check": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
        '<path d="m9 12 2 2 4-4"/>'
    ),
    "rotate": (
        '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>'
    ),
    "book": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "file-text": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<path d="M14 2v6h6"/><path d="M8 13h8"/><path d="M8 17h8"/>'
    ),
    "clipboard": (
        '<rect x="8" y="2" width="8" height="4" rx="1"/>'
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
    ),
    "code": (
        '<polyline points="16 18 22 12 16 6"/>'
        '<polyline points="8 6 2 12 8 18"/>'
        '<line x1="14" y1="4" x2="10" y2="20"/>'
    ),
    "lightbulb": (
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
        '<path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>'
    ),
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "flame": (
        '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>'
    ),
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    # Isaretli liste: butun bolumlerin ustunden bir kez daha gecmek.
    # SQL genel tekrar rozetinin simgesi.
    "list-checks": (
        '<path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/>'
        '<path d="M13 6h8"/><path d="M13 12h8"/><path d="M13 18h8"/>'
    ),
    # Tac: SQL patikasinin on alti bolumunun tamami.
    "crown": (
        '<path d="M11.562 3.266a.5.5 0 0 1 .876 0L15.39 8.87a1 1 0 0 0 1.516.294'
        'L21.183 5.5a.5.5 0 0 1 .798.519l-2.834 10.246a1 1 0 0 1-.956.734H5.81'
        'a1 1 0 0 1-.957-.734L2.02 6.02a.5.5 0 0 1 .798-.519l4.276 3.664'
        'a1 1 0 0 0 1.516-.294z"/><path d="M5 21h14"/>'
    ),
    # Yazili tomar: veritabaninda saklanan tarif. Gorunumler ve sakli
    # yordamlar rozetinin simgesi.
    "scroll-text": (
        '<path d="M15 12h-5"/><path d="M15 8h-5"/><path d="M19 17V5a2 2 0 0 0-2-2H4"/>'
        '<path d="M8 21h12a2 2 0 0 0 2-2v-1a1 1 0 0 0-1-1H11a1 1 0 0 0-1 1v1a2 2 0 1 1-4 0V5'
        'a2 2 0 1 0-4 0v2a1 1 0 0 0 1 1h3"/>'
    ),
    # A'dan Z'ye inen ok: dizin sirali bir listedir. Dizinler rozetinin
    # simgesi.
    "arrow-down-a-z": (
        '<path d="m3 16 4 4 4-4"/><path d="M7 20V4"/><path d="M20 8h-5"/>'
        '<path d="M15 10V6.5a2.5 2.5 0 0 1 5 0V10"/><path d="M15 14h5l-5 6h5"/>'
    ),
    # Girintili liste agaci: kademe kademe inen bir yonetim zinciri.
    # WITH ve ozyineleme rozetinin simgesi.
    "list-tree": (
        '<path d="M21 12h-8"/><path d="M21 6H8"/><path d="M21 18h-8"/>'
        '<path d="M3 6v4c0 1.1.9 2 2 2h3"/><path d="M3 10v6c0 1.1.9 2 2 2h3"/>'
    ),
    # Pencere cercevesi: satirlara bir pencereden bakmak. Pencere
    # fonksiyonlari rozetinin simgesi.
    "frame": (
        '<path d="M22 6H2"/><path d="M22 18H2"/>'
        '<path d="M6 2v20"/><path d="M18 2v20"/>'
    ),
    # Dalga: tekrar eden mevsim deseni. Ayristirma rozetinin simgesi.
    "wave": (
        '<path d="M2 12c1.7-6.5 3.3-6.5 5 0s3.3 6.5 5 0 3.3-6.5 5 0 3.3 6.5 5 0"/>'
    ),
    # Gecmis duz, gelecek kesik cizgi: ilk tahmin rozetinin simgesi.
    "forecast": (
        '<path d="M3 17l4-4.5 3.5 2.5 3.5-6"/><circle cx="14" cy="9" r="1.5"/>'
        '<path d="m15.5 8 5.5-4" stroke-dasharray="2 3"/>'
    ),
    # Kum saati: zamanla hesap yapmak. Zaman Serileri patikasinin tamami.
    "hourglass": (
        '<path d="M5 22h14"/><path d="M5 2h14"/>'
        '<path d="M17 22v-4.17a2 2 0 0 0-.59-1.42L12 12l-4.41 4.41A2 2 0 0 0 7 17.83V22"/>'
        '<path d="M7 2v4.17a2 2 0 0 0 .59 1.42L12 12l4.41-4.41A2 2 0 0 0 17 6.17V2"/>'
    ),
    # Basligi ve bir sutunu olan tablo: tabloyu kendin kurmak. Tablo tasarimi
    # rozetinin simgesi.
    "table-grid": (
        '<rect x="3" y="4" width="18" height="16" rx="2"/>'
        '<path d="M3 9.5h18"/><path d="M9.5 9.5V20"/>'
    ),
    # Kalem: veriyi okumaktan yazmaya gecis. Veri degistirme rozetinin simgesi.
    "pencil": (
        '<path d="M17 3a2.85 2.85 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>'
        '<path d="m15 5 4 4"/>'
    ),
    # Calisma kagidinin araclari (problem ekrani).
    "eraser": (
        '<path d="m7 21-4.3-4.3c-1-1-1-2.5 0-3.4l9.6-9.6c1-1 2.5-1 3.4 0l5.6 5.6c1 1 1 2.5 0 3.4L13 21"/>'
        '<path d="M22 21H7"/><path d="m5 11 9 9"/>'
    ),
    "undo": '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>',
    "redo": '<path d="m15 14 5-5-5-5"/><path d="M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/>',
    "trash": (
        '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/>'
        '<path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'
    ),
    # Kutu icinde kutu: sorgunun icindeki sorgu. Alt sorgu rozetinin simgesi.
    "nested-box": (
        '<rect x="3" y="3" width="18" height="18" rx="2"/>'
        '<rect x="8" y="8" width="8" height="8" rx="1"/>'
    ),
    # Kesisen iki halka: iki tablonun birlestigi yer.
    "link-rings": (
        '<circle cx="9" cy="12" r="6"/><circle cx="15" cy="12" r="6"/>'
    ),
    # Uc yatay cubuk, farkli uzunlukta: gruplarin dagilimi.
    "bars": (
        '<path d="M4 6h16"/><path d="M4 12h10"/><path d="M4 18h6"/>'
    ),
    # Uzeri cizili daire: bos kume isareti. NULL rozetinin simgesi.
    "circle-slash": '<circle cx="12" cy="12" r="9"/><path d="M5.6 18.4 18.4 5.6"/>',
    # Yukari ve asagi ok: siralama. `ORDER BY` rozetinin simgesi.
    "sort": (
        '<path d="m3 8 4-4 4 4"/><path d="M7 4v16"/>'
        '<path d="m21 16-4 4-4-4"/><path d="M17 20V4"/>'
    ),
    "bell": (
        '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'
    ),
    "check-circle": (
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/>'
    ),
    # Huni: SQL'de `WHERE` satirlari suzuyor, rozet de onu anlatiyor.
    "filter": '<path d="M3 4h18l-7 8.5V19l-4 2v-8.5L3 4z"/>',
    "link": (
        '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>'
        '<path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="9"/>'
        '<path d="M12 11v5"/><path d="M12 7.6v.1"/>'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 12 12 17 22 12"/>'
        '<polyline points="2 17 12 22 22 17"/>'
    ),
    "package": (
        '<path d="m12 2 9 5v10l-9 5-9-5V7z"/>'
        '<path d="m3 7 9 5 9-5"/><path d="M12 12v10"/>'
    ),
    # Git: bir daldan ayrılan ikinci dal.
    "git-branch": (
        '<path d="M6 3v12"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/>'
        '<path d="M18 9a9 9 0 0 1-9 9"/>'
    ),
    # --- patika simgeleri -------------------------------------------------
    # Python: iki iç içe geçmiş kıvrım, dilin logosuna gönderme.
    "python": (
        '<path d="M12 3c-3 0-4 1.4-4 3v2h8v1H6c-1.7 0-3 1.4-3 3.5S4.3 16 6 16h1.5"/>'
        '<path d="M12 21c3 0 4-1.4 4-3v-2H8v-1h10c1.7 0 3-1.4 3-3.5S19.7 8 18 8h-1.5"/>'
        '<circle cx="10" cy="6" r=".6" fill="currentColor"/>'
        '<circle cx="14" cy="18" r=".6" fill="currentColor"/>'
    ),
    # Veri bilimi: sütun grafiği.
    "chart": (
        '<path d="M3 21h18"/><path d="M6 21V10"/>'
        '<path d="M11 21V4"/><path d="M16 21v-7"/><path d="M21 21v-3"/>'
    ),
    # Makine öğrenmesi: birbirine bağlı düğümler.
    "network": (
        '<circle cx="5" cy="7" r="2"/><circle cx="5" cy="17" r="2"/>'
        '<circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>'
        '<path d="M7 8.2 10.2 11"/><path d="M7 15.8 10.2 13"/><path d="M14 12h3"/>'
    ),
    # SQL: veritabanı silindiri.
    "database": (
        '<ellipse cx="12" cy="5.5" rx="8" ry="3"/>'
        '<path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13"/>'
        '<path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>'
    ),
    # Kilit: içeriği henüz olmayan patikalarda.
    "lock": (
        '<rect x="4" y="10" width="16" height="10" rx="2"/>'
        '<path d="M8 10V7a4 4 0 0 1 8 0v3"/>'
    ),

    "scale": (
        '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M5 7h14"/>'
        '<path d="m5 7-3 7h6z"/><path d="m19 7-3 7h6z"/>'
    ),
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "cpu": (
        '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"/>'
        '<rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/>'
        '<line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/>'
        '<line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/>'
        '<line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/>'
        '<line x1="1" y1="14" x2="4" y2="14"/>'
    ),
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    "key": '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "award": '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "hexagon": '<polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/>',
    "box": (
        '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>'
        '<polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>'
    ),
    "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "crosshair": '<circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "anchor": '<circle cx="12" cy="5" r="3"/><line x1="12" y1="22" x2="12" y2="8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    # Patika simgeleri. Dördü eksikti ve yedek simgeye (chevron-right)
    # düşüyordu: ana ekranda dört patika "›" ile çiziliyordu.
    "sparkles": (
        '<path d="m12 3 1.9 5.8L20 10.7l-6.1 1.9L12 18.5l-1.9-5.9L4 10.7l6.1-1.9z"/>'
        '<path d="M19 3v4"/><path d="M17 5h4"/>'
    ),
    "calculator": (
        '<rect x="4" y="2" width="16" height="20" rx="2"/>'
        '<line x1="8" y1="6" x2="16" y2="6"/>'
        '<line x1="8" y1="11" x2="8.01" y2="11"/>'
        '<line x1="12" y1="11" x2="12.01" y2="11"/>'
        '<line x1="16" y1="11" x2="16.01" y2="11"/>'
        '<line x1="8" y1="15" x2="8.01" y2="15"/>'
        '<line x1="12" y1="15" x2="12.01" y2="15"/>'
        '<line x1="16" y1="15" x2="16.01" y2="18"/>'
    ),
    "library": (
        '<path d="M4 4v16"/><path d="M8 3v18"/>'
        '<rect x="11" y="4" width="4" height="16" rx="1"/>'
        '<path d="m18 5 3 14"/>'
    ),
    "server": (
        '<rect x="2" y="3" width="20" height="7" rx="2"/>'
        '<rect x="2" y="14" width="20" height="7" rx="2"/>'
        '<line x1="6" y1="6.5" x2="6.01" y2="6.5"/>'
        '<line x1="6" y1="17.5" x2="6.01" y2="17.5"/>'
    ),
    "clock": '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/>',
    # Alt şeritte kısayol listesini açan düğme.
    "keyboard": (
        '<rect x="2" y="6" width="20" height="12" rx="2"/>'
        '<path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>'
    ),
    # Rozet: ilk not ("Not Defteri") — üzerinde kalem olan defter.
    "notebook-pen": (
        '<path d="M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4"/>'
        '<path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/>'
        '<path d="M21.378 5.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854'
        'l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"/>'
    ),
    # Notlarım'da "Yeni klasör".
    "folder-plus": (
        '<path d="M12 10v6"/><path d="M9 13h6"/>'
        '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9'
        'A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>'
    ),
    # Şeritte Notlarım: sırtı çizgili bir defter.
    "notebook": (
        '<path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/>'
        '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M16 2v20"/>'
    ),
    # --- Python Temelleri rozetleri --------------------------------------
    # Döngüler: başa dönen ok.
    "repeat": (
        '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/>'
        '<path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>'
    ),
    # Fonksiyonlar: kendi yazdığın alet.
    "wrench": (
        '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77'
        'a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91'
        'a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>'
    ),
    # Nesne tabanlı programlama: aynı kalıptan çıkan şekiller.
    "shapes": (
        '<path d="M8.3 10a.7.7 0 0 1-.63-1.08L11.4 3a.7.7 0 0 1 1.2-.04L16.3 8.9'
        'A.7.7 0 0 1 15.73 10Z"/>'
        '<rect x="3" y="14" width="7" height="7" rx="1"/>'
        '<circle cx="17.5" cy="17.5" r="3.5"/>'
    ),
    # Patikanın tamamı: mezuniyet.
    "graduation-cap": (
        '<path d="m2 10 10-5 10 5-10 5z"/><path d="M22 10v6"/>'
        '<path d="M6 12v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/>'
    ),
    "message": (
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
    ),
    "route": (
        '<circle cx="6" cy="19" r="3"/>'
        '<path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/>'
        '<circle cx="18" cy="5" r="3"/>'
    ),
}


# İki tonlu çizim için doldurulan "gövde" yolları.
#
# Yalnız çizgiden oluşan ikonlar şeritte cansız duruyordu. Her ikonun asıl
# gövdesi kendi renginde, düşük saydamlıkta doldurulunca simge ekrandan
# ayrılıyor ama tek renkli kalıyor — tema neyse ikon o.
#
# Kural basit: **çekirdek şekil dolu, gerisi çizgi.** Evin gövdesi, kişinin
# başı, megafonun konisi, dişlinin göbeği, bilgi dairesinin diski. Buraya
# yolu yazılmayan ikon eskisi gibi yalnızca çizgiyle çiziliyor.
DUOTONE: dict[str, str] = {
    "home": '<path d="M3 9.5 12 3l9 6.5V20a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "user": '<circle cx="12" cy="8" r="4"/>',
    "route": '<circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/>',
    "notebook": '<rect x="4" y="2" width="16" height="20" rx="2"/>',
    "megaphone": '<path d="m3 11 15-7v16L3 13z"/>',
    "info": '<circle cx="12" cy="12" r="9"/>',
    "settings": '<circle cx="12" cy="12" r="3"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/>',
    "scale": "",
}

# Dolgunun saydamlığı. Daha koyusu çizgiyi yutuyor, daha açığı fark
# edilmiyor; ikisi arasında ölçülerek seçildi.
DUOTONE_OPACITY = 0.24


# --- 0.9.0 simge dili --------------------------------------------------
#
# İki tonlu yeni çizimler: her simge `(dolgu, çizgi)` çifti. Dolgu kendi
# renginde ve düşük saydamlıkta (`MODERN_FILL`), çizgi 1.8 px. Buradaki bir
# ad istendiğinde yeni çizim kullanılır; olmayanlar yukarıdaki eski yoldan
# çiziliyor. Yalnızca QSvgRenderer'ın çizebildiği öğeler var (path, circle,
# rect, ellipse); filtre ve maske yok.
MODERN: dict[str, tuple[str, str]] = {
    "user": ('<circle cx="12" cy="8" r="4"/><path d="M4 20c0-3.9 3.6-6 8-6s8 2.1 8 6z"/>',
             '<circle cx="12" cy="8" r="4"/><path d="M4 20c0-3.9 3.6-6 8-6s8 2.1 8 6"/>'),
    "compass": ('<circle cx="12" cy="12" r="9"/>',
                '<circle cx="12" cy="12" r="9"/><path d="m15.8 8.2-2.3 5.3-5.3 2.3 2.3-5.3z"/>'),
    "signpost": ('<path d="M12 5h6l2 2.5L18 10h-6zM12 12H6l-2 2.5L6 17h6z"/>',
                 '<path d="M12 3v18M12 5h6l2 2.5L18 10h-6M12 12H6l-2 2.5L6 17h6"/>'),
    "notebook": ('<rect x="5" y="3" width="14" height="18" rx="2.5"/>',
                 '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M9 3v18M12.5 8H16M12.5 12H16"/>'),
    "search": ('<circle cx="11" cy="11" r="7"/>',
               '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/>'),
    # Rotalar: başlangıçtan hedefe kıvrılan yol (tabela anlaşılmıyordu).
    "route": ('<circle cx="6" cy="18.5" r="2.8"/><circle cx="18" cy="5.5" r="2.8"/>',
              '<circle cx="6" cy="18.5" r="2.8"/><circle cx="18" cy="5.5" r="2.8"/>'
              '<path d="M8.8 18.5h7.7a3.25 3.25 0 0 0 0-6.5h-9a3.25 3.25 0 0 1 0-6.5h7.7"/>'),
    # Sürüm notları: parşömen tomarı (megafon bildirim gibi okunuyordu).
    "scroll-text": ('<path d="M7 5.5A2.5 2.5 0 0 0 4.5 3H16a2.5 2.5 0 0 1 2.5 2.5V16H9.5v2.5a2.5 2.5 0 0 1-2.5 2.5z"/>',
                    '<path d="M18.5 16V5.5A2.5 2.5 0 0 0 16 3H4.5A2.5 2.5 0 0 1 7 5.5v13A2.5 2.5 0 0 0 9.5 21H19a1.5 1.5 0 0 0 1.5-1.5V17a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1v1.5"/>'
                    '<path d="M4.5 3A2.5 2.5 0 0 0 2 5.5V7h5M11 8h4.5M11 11.5h4.5"/>'),
    "megaphone": ('<path d="M4 10v4a1 1 0 0 0 1 1h2l8 4V5L7 9H5a1 1 0 0 0-1 1z"/>',
                  '<path d="M4 10v4a1 1 0 0 0 1 1h2l8 4V5L7 9H5a1 1 0 0 0-1 1zM18.5 9.5a3.5 3.5 0 0 1 0 5M8 15l1.2 4.2"/>'),
    "info": ('<circle cx="12" cy="12" r="9"/>',
             '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 7.7v.01"/>'),
    "sliders": ('<circle cx="9" cy="7" r="2.4"/><circle cx="15" cy="12" r="2.4"/><circle cx="8" cy="17" r="2.4"/>',
                '<path d="M4 7h2.6M11.4 7H20M4 12h8.6M17.4 12H20M4 17h1.6M10.4 17H20"/>'
                '<circle cx="9" cy="7" r="2.4"/><circle cx="15" cy="12" r="2.4"/><circle cx="8" cy="17" r="2.4"/>'),
    "arrow-left": ("", '<path d="M19 12H5M11 6l-6 6 6 6"/>'),
    "arrow-right": ("", '<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "chevron-right": ("", '<path d="m9 6 6 6-6 6"/>'),
    "chevron-left": ("", '<path d="m15 6-6 6 6 6"/>'),
    "chevron-down": ("", '<path d="m6 9 6 6 6-6"/>'),
    # Adım adım izleme: basamaklar (düğme), başa / sona atlama.
    "steps": ("", '<path d="M3.5 19.5h5v-5h5v-5h5v-5h2"/>'),
    "skip-start": ("", '<path d="M7 6v12M17 6l-6 6 6 6"/>'),
    "skip-end": ("", '<path d="M17 6v12M7 6l6 6-6 6"/>'),
    # Sınav başlangıç kartının madalyonu: onaylı pano.
    "clipboard-check": ('<rect x="5" y="4.5" width="14" height="16.5" rx="2.5"/>',
                        '<rect x="5" y="4.5" width="14" height="16.5" rx="2.5"/>'
                        '<rect x="9" y="2.5" width="6" height="4" rx="1.2"/><path d="m9 13.5 2.2 2.2L15.5 11"/>'),
    # Sözlük terimi (arama sonucu): açık kitap.
    "book-open": ('<path d="M12 7v13c-2-1.6-4.6-2-8-2V5c3.4 0 6 .4 8 2zM12 7c2-1.6 4.6-2 8-2v13c-3.4 0-6 .4-8 2"/>',
                  '<path d="M12 7v13M12 7c-2-1.6-4.6-2-8-2v13c3.4 0 6 .4 8 2 2-1.6 4.6-2 8-2V5c-3.4 0-6 .4-8 2z"/>'),
    "lock": ('<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/>',
             '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5M12 14.5v2"/>'),
    "play": ('<path d="M8 5.6v12.8a1 1 0 0 0 1.5.9l10-6.4a1 1 0 0 0 0-1.8l-10-6.4A1 1 0 0 0 8 5.6z"/>',
             '<path d="M8 5.6v12.8a1 1 0 0 0 1.5.9l10-6.4a1 1 0 0 0 0-1.8l-10-6.4A1 1 0 0 0 8 5.6z"/>'),
    "pause": ('<rect x="6.5" y="5" width="4" height="14" rx="1.2"/><rect x="13.5" y="5" width="4" height="14" rx="1.2"/>',
              '<rect x="6.5" y="5" width="4" height="14" rx="1.2"/><rect x="13.5" y="5" width="4" height="14" rx="1.2"/>'),
    "check": ("", '<path d="m5 12.5 4.5 4.5L19 7.5"/>'),
    "x": ("", '<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>'),
    "plus": ("", '<path d="M12 5v14M5 12h14"/>'),
    "pencil": ('<path d="M15 5l4 4L9 19l-5 1 1-5z"/>', '<path d="M15 5l4 4L9 19l-5 1 1-5zM13 7l4 4"/>'),
    "eraser": ('<path d="M4.5 15.5 13 7l5 5-7.5 7.5H7z"/>',
               '<path d="M7 19.5h13M4.5 15.5 14 6a1.5 1.5 0 0 1 2 0l3 3a1.5 1.5 0 0 1 0 2l-8.5 8.5H7zM9.5 10.5l5 5"/>'),
    "undo": ("", '<path d="M9 14 4 9l5-5M4 9h10.5a5.5 5.5 0 0 1 0 11H11"/>'),
    "redo": ("", '<path d="m15 14 5-5-5-5M20 9H9.5a5.5 5.5 0 0 0 0 11H13"/>'),
    "trash": ('<path d="M6 7h12l-1 12.5a1.5 1.5 0 0 1-1.5 1.5h-7A1.5 1.5 0 0 1 7 19.5z"/>',
              '<path d="M4 7h16M9.5 7V4.5h5V7M6 7l1 12.5A1.5 1.5 0 0 0 8.5 21h7a1.5 1.5 0 0 0 1.5-1.5L18 7M10 11v6M14 11v6"/>'),
    "lightbulb": ('<path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z"/>',
                  '<path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2h5c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3zM9.5 19h5M10.5 21.5h3"/>'),
    "keyboard": ('<rect x="2.5" y="6" width="19" height="12" rx="3"/>',
                 '<rect x="2.5" y="6" width="19" height="12" rx="3"/><path d="M6.5 10h.01M10 10h.01M14 10h.01M17.5 10h.01M8 14h8"/>'),
    "star": ('<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
             '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>'),
    "folder": ('<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h4.3l2 2h8.7A1.5 1.5 0 0 1 21 9.5v8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5z"/>',
               '<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h4.3l2 2h8.7A1.5 1.5 0 0 1 21 9.5v8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5z"/>'),
    "folder-plus": ('<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h4.3l2 2h8.7A1.5 1.5 0 0 1 21 9.5v8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5z"/>',
                    '<path d="M3 7.5A1.5 1.5 0 0 1 4.5 6h4.3l2 2h8.7A1.5 1.5 0 0 1 21 9.5v8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17.5zM12 11v5M9.5 13.5h5"/>'),
    "download": ("", '<path d="M12 4v11M7 10.5l5 5 5-5M5 20h14"/>'),
    "upload": ("", '<path d="M12 16V5M7 9.5l5-5 5 5M5 20h14"/>'),
    "sun": ('<circle cx="12" cy="12" r="4.5"/>',
            '<circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>'),
    "moon": ('<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
             '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>'),
    "clock": ('<circle cx="12" cy="12" r="9"/>', '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'),
    "book": ('<path d="M3 5.5c3-1 6-1 9 1 3-2 6-2 9-1V19c-3-1-6-1-9 1-3-2-6-2-9-1z"/>',
             '<path d="M3 5.5c3-1 6-1 9 1 3-2 6-2 9-1V19c-3-1-6-1-9 1-3-2-6-2-9-1zM12 6.5V20"/>'),
    "file-text": ('<path d="M6 3h8l5 5v12a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/>',
                  '<path d="M6 3h8l5 5v12a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zM14 3v5h5M8.5 13h7M8.5 17h5"/>'),
    "clipboard": ('<rect x="5" y="4" width="14" height="17" rx="2.5"/>',
                  '<rect x="5" y="4" width="14" height="17" rx="2.5"/><path d="M9 4V3h6v1M8.5 13l2.5 2.5 4.5-5"/>'),
    "terminal": ('<rect x="3" y="4.5" width="18" height="15" rx="3"/>',
                 '<rect x="3" y="4.5" width="18" height="15" rx="3"/><path d="m7 10 3 2.5L7 15M12.5 15H17"/>'),
    "sigma": ('<rect x="3" y="3" width="18" height="18" rx="4"/>', '<path d="M16.5 7h-9l4.5 5-4.5 5h9"/>'),
    "globe": ('<circle cx="12" cy="12" r="9"/>',
              '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.7 5.6 3.7 9S14.5 18.4 12 21c-2.5-2.6-3.7-5.6-3.7-9S9.5 5.6 12 3z"/>'),
    "bell": ('<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/>', '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 21h4"/>'),
    "palette": ('<path d="M12 3a9 9 0 0 0 0 18c1.4 0 2-1 1.6-2.1-.5-1.3.4-2.4 1.8-2.4H18a3 3 0 0 0 3-3c0-5.6-4-10.5-9-10.5z"/>',
                '<path d="M12 3a9 9 0 0 0 0 18c1.4 0 2-1 1.6-2.1-.5-1.3.4-2.4 1.8-2.4H18a3 3 0 0 0 3-3c0-5.6-4-10.5-9-10.5zM7.5 11.5h.01M10 7.5h.01M14.5 7.5h.01"/>'),
    "graduation-cap": ('<path d="m12 4 10 5-10 5L2 9z"/>',
                       '<path d="m12 4 10 5-10 5L2 9zM6 11v5c3.5 2.7 8.5 2.7 12 0v-5M22 9v5"/>'),
    "refresh": ("", '<path d="M20 11a8 8 0 0 0-14.5-4.5L4 8M4 4v4h4M4 13a8 8 0 0 0 14.5 4.5L20 16M20 20v-4h-4"/>'),
    "database": ('<ellipse cx="12" cy="6" rx="7.5" ry="3"/>',
                 '<ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/>'),
    "sparkles": ('<path d="M12 3c.7 4.2 2.8 6.3 7 7-4.2.7-6.3 2.8-7 7-.7-4.2-2.8-6.3-7-7 4.2-.7 6.3-2.8 7-7z"/>',
                 '<path d="M12 3c.7 4.2 2.8 6.3 7 7-4.2.7-6.3 2.8-7 7-.7-4.2-2.8-6.3-7-7 4.2-.7 6.3-2.8 7-7z"/>'),
    "flame": ('<path d="M12 21.5c-4 0-7-2.8-7-6.7 0-3.5 2.5-5.6 3.9-7.5.3 2 1.3 3.4 2.6 3.9C11.1 7.8 12.2 4.6 15 2.5c.2 3.4 4 6.3 4 11.3 0 4.3-3 7.7-7 7.7z"/>',
              '<path d="M12 21.5c-4 0-7-2.8-7-6.7 0-3.5 2.5-5.6 3.9-7.5.3 2 1.3 3.4 2.6 3.9C11.1 7.8 12.2 4.6 15 2.5c.2 3.4 4 6.3 4 11.3 0 4.3-3 7.7-7 7.7z"/>'),
    "target": ('<circle cx="12" cy="12" r="9"/>',
               '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>'),
    "copy": ('<rect x="8" y="8" width="12" height="12" rx="2.5"/>',
             '<rect x="8" y="8" width="12" height="12" rx="2.5"/><path d="M16 8V5.5A1.5 1.5 0 0 0 14.5 4h-9A1.5 1.5 0 0 0 4 5.5v9A1.5 1.5 0 0 0 5.5 16H8"/>'),
}

# Yeni simgelerin dolgu saydamlığı ve çizgi kalınlığı (prototipte seçildi).
# Üzerine gelinen simgede `MODERN_FILL_HOVER`, seçilide `MODERN_FILL_ACTIVE`.
MODERN_FILL = 0.16
MODERN_FILL_HOVER = 0.30
MODERN_FILL_ACTIVE = 0.38
MODERN_STROKE = 1.8


def svg_markup(
    name: str,
    color: str,
    stroke: float = 2.0,
    filled: bool = False,
    duotone: bool = False,
    fill_opacity: float | None = None,
) -> str:
    """İkonu tam bir SVG belgesine sarar."""
    if name in MODERN:
        dolgu, cizgi = MODERN[name]
        kalinlik = MODERN_STROKE if stroke == 2.0 else stroke
        saydam = MODERN_FILL if fill_opacity is None else fill_opacity
        taban = (
            f'<g fill="{color}" fill-opacity="{saydam}" stroke="none">{dolgu}</g>'
            if dolgu and not filled else ""
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{taban}'
            f'<g fill="{color if filled else "none"}" stroke="{color}" '
            f'stroke-width="{kalinlik}" stroke-linecap="round" '
            f'stroke-linejoin="round">{cizgi}</g></svg>'
        )
    path = PATHS.get(name, PATHS["chevron-right"])
    fill = color if filled else "none"

    taban = ""
    if duotone and not filled:
        govde = DUOTONE.get(name, "")
        if govde:
            taban = (
                f'<g fill="{color}" fill-opacity="{DUOTONE_OPACITY}" '
                f'stroke="none">{govde}</g>'
            )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
        f"{taban}"
        f'<g fill="{fill}" stroke="{color}" stroke-width="{stroke}" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</g>'
        f"</svg>"
    )


def icon(
    name: str,
    color: str = "#666F7D",
    size: int = 22,
    filled: bool = False,
    stroke: float = 2.0,
    duotone: bool = False,
    fill_opacity: float | None = None,
) -> QIcon:
    """İkonu istenen renk, boyut ve çizgi kalınlığında bir QIcon olarak üretir."""
    renderer = QSvgRenderer(
        QByteArray(
            svg_markup(
                name, color, stroke=stroke, filled=filled, duotone=duotone,
                fill_opacity=fill_opacity,
            ).encode("utf-8")
        )
    )

    # Yüksek DPI ekranlarda bulanık görünmemesi için iki katı çözünürlükte
    # çizip ölçekliyoruz.
    pixmap = QPixmap(QSize(size * 2, size * 2))
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()

    pixmap.setDevicePixelRatio(2.0)
    return QIcon(pixmap)


def pixmap(name: str, color: str = "#666F7D", size: int = 22, filled: bool = False) -> QPixmap:
    """İkonu doğrudan QPixmap olarak verir (QLabel içinde kullanmak için)."""
    return icon(name, color, size, filled).pixmap(QSize(size, size))
