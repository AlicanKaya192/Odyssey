"""Sürüm bilgileri.

Uygulama kodu ile müfredat içeriği ayrı ayrı sürümlenir. Böylece sadece bir
ders notu düzeltildiğinde kullanıcının tüm uygulamayı yeniden indirmesi
gerekmez; yalnızca değişen içerik paketi iner.
"""

# Uygulama kodunun sürümü.
APP_VERSION = "0.1.0"

# Müfredat içeriğinin sürümü. content/manifest.json ile birlikte kullanılır.
CONTENT_VERSION = "0.1.0"

# Veritabanı şemasının sürümü. Bu sayı arttığında, açılışta eksik göçler
# sırayla uygulanır ve kullanıcının mevcut verisi korunur.
SCHEMA_VERSION = 1

# Uygulama verilerinin tutulduğu klasörün adı (%APPDATA% altında).
APP_DIR_NAME = "ProjeA"
