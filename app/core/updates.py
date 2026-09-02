"""Yeni sürüm denetimi.

Uygulama kendini güncellemiyor: yalnızca "yeni bir sürüm yayınlanmış mı"
diye bakıyor ve varsa sürüm sayfasının bağlantısını gösteriyor. İndirmeyi,
açmayı ve eskisini silmeyi kullanıcı yapıyor.

**Neden kendi kendine güncellemiyor:** paket 690 MB'lık bir klasör ve
çalışırken kendi dosyalarının üstüne yazamıyor. Kendini güncelleyen bir
sürüm, yarıda kesilen bir indirmede uygulamayı çalışmaz hâle getirebilir.
Bağlantıyı gösterip kenara çekilmek dürüst ve kırılmaz olanı.

**Ağa çıkan tek yer burası.** Dersler, alıştırmalar, sınavlar ve ilerleme
tamamen çevrimdışı. Bu sorgu:

- yalnızca **GET** yapıyor, hiçbir şey göndermiyor (kimlik, ilerleme,
  kullanım verisi — hiçbiri);
- ayarlardan **kapatılabiliyor**;
- her açılışta bir kez, açık kalan bir oturumda da üç saatte bir
  çalışıyor;
- başarısız olduğunda **sessiz kalıyor**. İnternetin olmaması bu
  uygulamada bir hata değil, olağan durum.

Ağ erişimi olmayan bir kullanıcı hiçbir uyarı görmüyor; program aynı
şekilde çalışmaya devam ediyor.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
import time
from dataclasses import dataclass, field

from ..version import APP_VERSION

# Sürümlerin duyurulduğu adres. Depo public olduğunda kimlik doğrulaması
# istemeden okunuyor; private olduğu sürece 404 dönüyor ve denetim sessizce
# "bilinmiyor" diyor.
#
# **`/releases/latest` değil, liste.** İlk sürümde `latest` kullanılıyordu
# ve depo public yapıldığında 404 döndü: o uç nokta **ön sürüm işaretli**
# yayınları saymıyor, bizim yedi sürümümüzün de hepsi ön sürüm (uygulama
# 0.x, yani hepsi öyle). Liste hepsini veriyor; en yüksek numaralı olan
# seçiliyor.
RELEASES_API = "https://api.github.com/repos/AlicanKaya192/Odyssey/releases?per_page=5"

# Sürüm sayfası: denetim başarısız olsa bile kullanıcıya verilecek adres.
RELEASES_PAGE = "https://github.com/AlicanKaya192/Odyssey/releases"

# GitHub kimliksiz isteklerde bir `User-Agent` istiyor; olmayınca 403
# dönüyor. Sürüm numarası da burada — sunucuya giden tek bilgi bu.
USER_AGENT = f"Odyssey/{APP_VERSION}"

# Kısa tutuldu: açılışta yapılan bir denetim uzun sürerse arka planda
# bekleyen bir iş parçacığı kalıyor.
TIMEOUT_SEC = 6

# Açık kalan bir oturumda iki denetim arasındaki en kısa süre. Uygulama
# günlerce açık kalabiliyor; günde bir kez bakmak, sabah açıp akşama kadar
# çalışan birinin yeni sürümü ertesi güne kadar görmemesi demekti.
#
# Sıklık sınırı sorun değil: GitHub kimliksiz isteklerde aynı IP'ye saatte
# 60 istek veriyor, buradaki en yoğun kullanım günde birkaç tane.
CHECK_INTERVAL_SEC = 3 * 60 * 60

# Ayar anahtarları.
UPDATE_CHECK_KEY = "update_check"
LAST_CHECK_KEY = "update_last_check"

# Duyuru penceresinin gösterildiği son sürüm. Aynı sürüm için pencere bir
# kez açılıyor; her açılışta çıkan bir kutu okunmadan kapatılan bir engele
# dönüşüyor. Şeritteki satır ise kalıcı — orada durması rahatsız etmiyor.
NOTIFIED_KEY = "update_notified"

# Denetim varsayılan olarak **açık**. Kapatan biri hiç ağa çıkmıyor.
DEFAULT_ENABLED = True


@dataclass(frozen=True)
class UpdateInfo:
    """Denetimin sonucu.

    `status` değerleri:

    - `newer`   — daha yeni bir sürüm var, `version` ve `url` dolu
    - `current` — en güncel sürüm çalışıyor
    - `offline` — ağa çıkılamadı (internet yok, DNS yok, zaman aşımı)
    - `error`   — sunucu beklenen cevabı vermedi (404, bozuk JSON, 403)

    Son ikisi kullanıcıya hata olarak gösterilmiyor; yalnızca elle
    denetleyen birine "şu an bakılamadı" demek için ayrıldılar.
    """

    status: str
    version: str = ""
    url: str = RELEASES_PAGE
    # Sürümün indirilebilir dosyaları (ham JSON). Kurulumu yapan
    # `updater.py` buradan kendi paketini seçiyor.
    assets: tuple = ()
    detail: str = field(default="", repr=False)

    @property
    def has_update(self) -> bool:
        return self.status == "newer"


def parse_version(text: str) -> tuple[int, ...]:
    """`v0.6.0` → `(0, 6, 0)`.

    Sayı olmayan parçalar atılıyor: `0.7.0-beta` da `(0, 7, 0)` oluyor.
    Karşılaştırma için yeterli; bir ön sürümü kararlı sürümden ayırmak
    gerekseydi burası büyürdü, şimdilik gerekmiyor.
    """
    temiz = text.strip().lstrip("vV")
    parcalar: list[int] = []
    for parca in temiz.split("."):
        sayi = ""
        for karakter in parca:
            if not karakter.isdigit():
                break
            sayi += karakter
        if not sayi:
            break
        parcalar.append(int(sayi))
    return tuple(parcalar)


def is_newer(remote: str, local: str = APP_VERSION) -> bool:
    """Uzaktaki sürüm buradakinden yeni mi?

    Okunamayan bir sürüm numarası "yeni değil" sayılıyor: kullanıcıyı
    anlamsız bir bildirimle rahatsız etmektense sessiz kalmak iyi.
    """
    uzak = parse_version(remote)
    yerel = parse_version(local)
    if not uzak or not yerel:
        return False

    # Farklı uzunluktaki numaralar karşılaştırılabilsin diye sıfırla
    # dolduruluyor: `0.7` ile `0.7.0` aynı sürüm.
    boy = max(len(uzak), len(yerel))
    uzak += (0,) * (boy - len(uzak))
    yerel += (0,) * (boy - len(yerel))
    return uzak > yerel


def enabled(store) -> bool:
    """Kullanıcı denetimi açık bırakmış mı?"""
    kayit = store.setting(UPDATE_CHECK_KEY, "")
    if kayit == "":
        return DEFAULT_ENABLED
    return kayit == "1"


def set_enabled(store, value: bool) -> None:
    store.set_setting(UPDATE_CHECK_KEY, "1" if value else "0")


def seconds_since_check(store) -> float:
    """Son başarılı denetimden bu yana geçen saniye.

    Hiç bakılmadıysa (ya da kayıt okunamıyorsa) sonsuz: "hemen bak".
    """
    kayit = store.setting(LAST_CHECK_KEY, "")
    try:
        return time.time() - float(kayit)
    except (TypeError, ValueError):
        return float("inf")


def mark_checked(store) -> None:
    store.set_setting(LAST_CHECK_KEY, str(int(time.time())))


def already_notified(store, version: str) -> bool:
    """Bu sürümün duyuru penceresi daha önce açıldı mı?"""
    return bool(version) and store.setting(NOTIFIED_KEY, "") == version


def mark_notified(store, version: str) -> None:
    store.set_setting(NOTIFIED_KEY, version)


def fetch_latest(url: str = "", timeout: int = TIMEOUT_SEC) -> UpdateInfo:
    """Son yayınlanan sürümü sorar. **Hiçbir zaman hata fırlatmaz.**"""
    istek = urllib.request.Request(
        url or RELEASES_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(istek, timeout=timeout) as cevap:
            ham = cevap.read(64 * 1024)
    except urllib.error.HTTPError as hata:
        # 404: depo private ya da hiç sürüm yok. 403: istek sınırı.
        return UpdateInfo(status="error", detail=f"HTTP {hata.code}")
    except (urllib.error.URLError, TimeoutError, OSError) as hata:
        return UpdateInfo(status="offline", detail=str(hata))

    try:
        veri = json.loads(ham)
    except (ValueError, UnicodeDecodeError) as hata:
        return UpdateInfo(status="error", detail=str(hata))

    # Liste bekleniyor; tek bir sürüm dönen bir uca bakılırsa da çalışsın
    # diye sözlük de kabul ediliyor.
    if isinstance(veri, dict):
        veri = [veri]
    if not isinstance(veri, list):
        return UpdateInfo(status="error", detail="beklenmeyen cevap")

    en_iyi = None
    en_iyi_numara: tuple[int, ...] = ()
    for kayit in veri:
        if not isinstance(kayit, dict) or kayit.get("draft"):
            continue
        numara = parse_version(str(kayit.get("tag_name") or ""))
        if numara and numara > en_iyi_numara:
            en_iyi, en_iyi_numara = kayit, numara

    if en_iyi is None:
        return UpdateInfo(status="error", detail="yayınlanmış sürüm yok")

    etiket = str(en_iyi.get("tag_name") or "")
    sayfa = str(en_iyi.get("html_url") or RELEASES_PAGE)
    if not sayfa.startswith("https://github.com/"):
        # Cevaptan gelen bir adresi doğrudan tarayıcıya açmıyoruz.
        sayfa = RELEASES_PAGE

    dosyalar = en_iyi.get("assets")
    dosyalar = tuple(dosyalar) if isinstance(dosyalar, list) else ()

    surum = etiket.lstrip("vV")
    durum = "newer" if is_newer(etiket) else "current"
    return UpdateInfo(status=durum, version=surum, url=sayfa, assets=dosyalar)


# --- ayarla ağ arasındaki iş bölümü -----------------------------------
#
# `fetch_latest` ağa çıkıyor ve **ayrı bir iş parçacığında** çalışıyor;
# veritabanına oradan dokunulmuyor. Sebebi ölçüldü: `sqlite3` bağlantısı
# kendisini kuran iş parçacığına bağlı, başka bir yerden kullanılınca
#
#     SQLite objects created in a thread can only be used in that same thread
#
# hatası veriyor. Denetim bu yüzden üçe bölündü: **karar** (`should_check`)
# ve **kayıt** (`record`) arayüz iş parçacığında, **ağ** arkada.


def should_check(store, ignore_interval: bool = False) -> bool:
    """Şimdi bakılsın mı?

    `ignore_interval` iki yerde kullanılıyor: **açılışta** (program her
    açıldığında bir kez baksın diye) ve **elle denetlemede**. Aradaki
    süre kuralı yalnızca açık kalan bir oturumun kendi kendine yaptığı
    denetim için var.

    Ayar kapalıysa hiçbir durumda bakılmıyor.
    """
    if not enabled(store):
        return False
    if ignore_interval:
        return True
    return seconds_since_check(store) >= CHECK_INTERVAL_SEC


def record(store, info: UpdateInfo) -> None:
    """Denetimin sonucunu kaydeder.

    Yalnızca sunucuya gerçekten ulaşıldığında işaretleniyor; ağı kapalı
    olan biri ertesi gün değil, bir sonraki açılışta yeniden deniyor.
    """
    if info.status in ("newer", "current"):
        mark_checked(store)
