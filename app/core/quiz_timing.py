"""Sınav süresi ayarı.

Ayarlardan "sınav süresini kaldır" açıldığında sayaç çalışmıyor; bölümün
kendi süresi yerinde duruyor, ayar kapatılınca geri geliyor.

**Kural burada, tek yerde** — `app/core/unlock.py` ile aynı sebeple. Kilit
tarafında anahtar üç ayrı çağrı noktasında okunuyordu ve biri ayarı
unutunca o ekran kilidi uygulamaya devam ediyordu. Süre ayarı da aynı
tuzağa düştü: ayar okunduğu tek yer sınavın **açıldığı** an olduğu için,
sınav açıkken ayar değiştirildiğinde ekranda hiçbir şey olmuyordu.
"""

from __future__ import annotations

# Ayarlar penceresindeki "sınav süresini kaldır" anahtarı.
UNTIMED_QUIZ_KEY = "untimed_quiz"


def untimed_quiz(store) -> bool:
    """Kullanıcı sınav süresini kaldırmayı seçmiş mi?"""
    return store.setting(UNTIMED_QUIZ_KEY, "") == "1"
