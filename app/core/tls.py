"""HTTPS bağlantıları için sertifika deposu.

Windows'ta Python sistemin sertifika deposunu kendisi okuyor. Paketlenmiş
macOS programında okuyamıyor: Mac denemesinde (13 Kasım) sürüm denetimi
`CERTIFICATE_VERIFY_FAILED` ile düştü. Orada pakete giren `certifi`'nin
listesi kullanılıyor.
"""

from __future__ import annotations

import ssl
import sys


def context() -> ssl.SSLContext | None:
    """`urlopen(..., context=...)` için; None ise Python'un varsayılanı."""
    if sys.platform != "darwin":
        return None
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())
