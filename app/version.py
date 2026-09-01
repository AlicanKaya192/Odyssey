"""Sürüm bilgileri.

Uygulama kodu ile müfredat içeriği ayrı ayrı sürümlenir. Böylece sadece bir
ders notu düzeltildiğinde kullanıcının tüm uygulamayı yeniden indirmesi
gerekmez; yalnızca değişen içerik paketi iner.
"""

# Sürüm numaraları BÜYÜK.ORTA.KÜÇÜK biçiminde ilerliyor:
#   küçük  — düzeltmeler ve küçük eklemeler (geliştirme boyunca çoğunlukla bu)
#   orta   — bir aşama tamamlandığında
#   büyük  — benden başkasının kullanabileceği ilk sürümde 1.0.0
# Ayrıntısı CHANGELOG.md'nin başında yazılı.

# Uygulama kodunun sürümü.
APP_VERSION = "0.4.0"

# Müfredat içeriğinin sürümü. content/manifest.json ile birlikte kullanılır.
CONTENT_VERSION = "0.4.0"

# Veritabanı şemasının sürümü. Bu sayı arttığında, açılışta eksik göçler
# sırayla uygulanır ve kullanıcının mevcut verisi korunur.
SCHEMA_VERSION = 1

# Uygulama verilerinin tutulduğu klasörün adı (%APPDATA% altında).
APP_DIR_NAME = "Odyssey"

# Eskiden kullanılmış klasör adları. Uygulamanın adı değişince kullanıcının
# ilerlemesi öksüz kalmasın diye ilk açılışta taşınıyor. Yeni bir ad
# değişikliği olursa buraya eklenir, listeden çıkarılmaz.
LEGACY_APP_DIR_NAMES = ("ProjeA",)
