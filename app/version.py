"""Sürüm bilgileri.

Uygulama kodu ile müfredat içeriği ayrı ayrı sürümlenir. Böylece sadece bir
ders notu düzeltildiğinde kullanıcının tüm uygulamayı yeniden indirmesi
gerekmez; yalnızca değişen içerik paketi iner.
"""

# Sürüm numaraları BÜYÜK.ORTA.KÜÇÜK biçiminde ilerliyor. 1.0.0 açık betadan
# çıkılan ilk tam sürüm; ondan sonra:
#   küçük  — yalnızca hata düzeltmeleri (1.0.0 → 1.0.1)
#   orta   — yeni patika ya da büyük özellik (1.0.x → 1.1.0)
#   büyük  — programın büyük ölçüde yeniden kurulduğu bir sürüm (2.0.0)
# Ayrıntısı CHANGELOG.md'nin başında yazılı.

# Uygulama kodunun sürümü.
APP_VERSION = "1.0.0"

# Müfredat içeriğinin sürümü. Uygulama kodundan ayrı ilerliyor.
CONTENT_VERSION = "0.7.0"

# Veritabanı şemasının sürümü. Bu sayı arttığında, açılışta eksik göçler
# sırayla uygulanır ve kullanıcının mevcut verisi korunur. Gerçek göç
# `app/core/progress.py` içindeki `MIGRATIONS` listesinden geliyor; burası
# onunla aynı sayıda tutulur.
SCHEMA_VERSION = 11

# Uygulama verilerinin tutulduğu klasörün adı (%APPDATA% altında).
APP_DIR_NAME = "Odyssey"

# Eskiden kullanılmış klasör adları. Uygulamanın adı değişince kullanıcının
# ilerlemesi öksüz kalmasın diye ilk açılışta taşınıyor. Yeni bir ad
# değişikliği olursa buraya eklenir, listeden çıkarılmaz.
LEGACY_APP_DIR_NAMES = ("ProjeA",)
