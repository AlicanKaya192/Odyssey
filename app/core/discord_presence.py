"""Discord'da "Odyssey kullanıyor" yazısını gösterir.

Discord masaüstü uygulaması, bilgisayarda bir **adlandırılmış boru** açıyor
(`\\\\.\\pipe\\discord-ipc-0`). O boruya bağlanan bir program, kullanıcının
profilinde ne yaptığını yazdırabiliyor. Sunucu, hesap, ağ bağlantısı yok:
her şey aynı bilgisayarın içinde kalıyor.

Protokol küçük olduğu için kütüphane eklenmedi. Bir çerçeve şöyle:

    [4 bayt işlem kodu][4 bayt uzunluk][UTF-8 JSON]

İkisi de küçük soncul (little-endian). İşlem kodları: 0 el sıkışma,
1 komut, 2 kapanış, 3 ping, 4 pong.

## Uygulamayı hiçbir koşulda bekletmiyor

Bütün iş ayrı bir iş parçacığında dönüyor ve **hiçbir hata dışarı
sızmıyor**. Discord kurulu değilse, kapalıysa, sonradan açılırsa ya da
kullanıcı ortasında kapatırsa uygulama bunu fark etmiyor bile:

- Boru yoksa bağlanma denemesi anında hata veriyor (dosya bulunamadı) ve
  otomatik olarak bir süre sonra tekrar deneniyor.
- Discord kapanınca ilk yazma hatası bağlantıyı düşürüyor; döngü yeniden
  bağlanmaya başlıyor.
- Okuma **hiçbir zaman bloklamıyor**: borudan yalnızca hazır bekleyen bayt
  kadar okunuyor (`PeekNamedPipe`). Cevaplar bize lazım değil, ama
  okunmazsa boru dolup Discord tarafını tıkıyor.

## Neden 15 saniye, neden 60 saniye

Discord `SET_ACTIVITY` çağrısını sınırlıyor. Kullanıcı hızlıca bölüm
değiştirdiğinde her değişikliği göndermiyoruz: **en son istenen durum**
saklanıp süre dolunca bir kez gönderiliyor (15 sn).

Durum hiç değişmese bile dakikada bir tazeleniyor (60 sn). Discord uzun
süre haber alamadığı bir etkinliği bayatlamış sayabiliyor; yazı ekranda
kalıyor ama geçen süre saymayı bırakıyor.
"""

from __future__ import annotations

import json
import os
import struct
import sys
import threading
import time

# Discord Developer Portal'daki uygulamanın kimliği. Gizli bir değer değil:
# Rich Presence kullanan her programda açıkta duruyor ve zaten her
# kullanıcının Discord istemcisine gönderiliyor. Gizli olanlar bot anahtarı
# ve istemci sırrı; onlar bu uygulamada hiç kullanılmıyor.
CLIENT_ID = "1545108575196684428"

# Developer Portal → Rich Presence → Art Assets altına yüklenen görselin adı.
LARGE_IMAGE = "odyssey"

# Durumun altındaki düğme.
#
# **Düğme kendi profilinde görünmüyor.** Discord onu yalnızca başkası
# profiline baktığında çiziyor; kendi etkinlik kartında hiç düğme alanı
# yok. Ölçüldü: Discord düğmeyi kabul edip geri yansıtıyor
# (`metadata.button_urls`), yani gönderim doğru.
#
# Etiket çevrilmiyor: "GitHub" bir marka adı ve iki dilde de aynı.
PROJECT_URL = "https://github.com/AlicanKaya192/Odyssey"
BUTTON_LABEL = "GitHub"

# İkinci düğme doğrudan son sürüme gidiyor: depo sayfasında sürümleri
# aramak bir tık daha uzun. Discord en fazla iki düğme çiziyor.
RELEASES_URL = PROJECT_URL + "/releases/latest"

PIPE_TEMPLATE = r"\\.\pipe\discord-ipc-{}"
PIPE_COUNT = 10

OP_HANDSHAKE = 0
OP_FRAME = 1
OP_CLOSE = 2

# Discord'un sınırı; altına inmek çağrıların sessizce düşmesine yol açıyor.
MIN_SEND_INTERVAL = 15.0
# Discord kapalıyken boşuna denememek için bekleme.
RECONNECT_INTERVAL = 20.0
# Durum değişmese bile bu aralıkla yeniden gönderiliyor.
#
# Discord, uzun süre haber alamadığı bir etkinliği bayatlamış sayabiliyor:
# yazı ekranda kalıyor ama geçen süre saymayı bırakıyor. Oyunlar da bu
# yüzden durumu düzenli olarak tazeliyor. Dakikada bir çerçeve, Discord'un
# sınırının çok altında.
HEARTBEAT_INTERVAL = 60.0
# Döngünün nabzı. Küçük tutuluyor ki kapanış isteği hemen görülsün.
TICK = 0.5

SETTING_KEY = "discord_presence"


def enabled(store) -> bool:
    """Ayar açık mı? Varsayılan **açık**.

    Discord'un kendi ayarlarında da "etkinliği durum olarak göster"
    anahtarı var; kullanıcı orada kapattığında burası ne derse desin
    hiçbir şey görünmüyor. Yani karar iki yerden birden verilebiliyor.
    """
    return store.setting(SETTING_KEY, "1") != "0"


def set_enabled(store, value: bool) -> None:
    store.set_setting(SETTING_KEY, "1" if value else "0")


class _Pipe:
    """Discord'un borusuna açılan bağlantı.

    Bütün hataları `OSError` olarak dışarı bırakıyor; onları döngü
    yakalayıp bağlantıyı düşürüyor.
    """

    def __init__(self, handle) -> None:
        self._file = handle
        self._peek = None
        if sys.platform == "win32":
            try:
                import ctypes
                import msvcrt
                from ctypes import wintypes

                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                peek = kernel32.PeekNamedPipe
                # Argüman tipleri **bildirilmek zorunda**. Bildirilmezse
                # ctypes Python tam sayısını C `int` sanıyor ve 64 bitlik
                # tanıtıcıyı 32 bite kırpıyor. Küçük tanıtıcılarda tesadüfen
                # çalışıyor, büyüklerinde sessizce bozuluyor.
                peek.argtypes = [
                    wintypes.HANDLE,
                    ctypes.c_void_p,
                    wintypes.DWORD,
                    ctypes.POINTER(wintypes.DWORD),
                    ctypes.POINTER(wintypes.DWORD),
                    ctypes.POINTER(wintypes.DWORD),
                ]
                peek.restype = wintypes.BOOL
                self._peek = peek
                self._osf = wintypes.HANDLE(msvcrt.get_osfhandle(handle.fileno()))
                self._ctypes = ctypes
                self._wintypes = wintypes
            except Exception:
                # Yoklama kurulamadıysa okuma hiç yapılmıyor; yazma yine
                # çalışıyor ve kopukluk oradan anlaşılıyor.
                self._peek = None

    @classmethod
    def connect(cls) -> "_Pipe | None":
        """Sırayla boruları deniyor. Discord yoksa None dönüyor."""
        if sys.platform != "win32":
            return None
        for index in range(PIPE_COUNT):
            try:
                handle = open(PIPE_TEMPLATE.format(index), "r+b", buffering=0)
            except OSError:
                continue
            return cls(handle)
        return None

    def send(self, opcode: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self._file.write(struct.pack("<II", opcode, len(body)) + body)
        self._file.flush()

    def drain(self) -> None:
        """Borudaki cevapları atıyor.

        Okumadan bırakmak boruyu dolduruyor ve Discord tarafındaki yazma
        tıkanıyor. Cevapların içeriği bize lazım değil, yalnızca yer
        açılması gerekiyor.

        **Bloklamıyor:** önce kaç bayt hazır olduğu soruluyor, yalnızca o
        kadar okunuyor.
        """
        if self._peek is None:
            return
        available = self._wintypes.DWORD(0)
        ok = self._peek(
            self._osf, None, 0, None, self._ctypes.byref(available), None
        )
        if not ok:
            raise OSError("boru yoklanamadı")
        if available.value:
            self._file.read(available.value)

    def close(self) -> None:
        try:
            self._file.close()
        except OSError:
            pass


class DiscordPresence:
    """Arka planda Discord'a durum gönderen iş parçacığı.

    Kullanımı üç çağrı:

        presence = DiscordPresence(store)
        presence.start()
        presence.set_activity("Makine Öğrenmesi", "Karar Ağaçları")
        presence.stop()

    Hiçbiri hata fırlatmıyor ve hiçbiri beklemiyor.
    """

    def __init__(self, store, *, client_id: str = CLIENT_ID) -> None:
        self._store = store
        self._client_id = client_id
        self._thread: threading.Thread | None = None
        self._wake = threading.Event()
        self._stopping = False
        self._lock = threading.Lock()
        self._details = ""
        self._state = ""
        self._large_text = ""
        self._buttons: list[dict] = []
        self._dirty = False
        self._started_at = int(time.time())
        self._pipe: _Pipe | None = None
        self._last_send = 0.0
        self._next_connect = 0.0

    # --- dışarıya açık -----------------------------------------------

    def start(self) -> None:
        """İş parçacığını başlatır. Ayar kapalıysa hiçbir şey yapmıyor."""
        if self._thread is not None or not enabled(self._store):
            return
        self._thread = threading.Thread(
            target=self._loop, name="discord-presence", daemon=True
        )
        self._thread.start()

    def set_activity(
        self,
        details: str,
        state: str,
        *,
        large_text: str = "",
        buttons: list[dict] | None = None,
    ) -> None:
        """Gösterilecek metni günceller.

        Hemen gönderilmeyebilir: Discord'un sınırı dolduysa en son istenen
        durum saklanıp süre dolunca gönderiliyor.
        """
        with self._lock:
            if (details, state) == (self._details, self._state):
                return
            self._details = details
            self._state = state
            if large_text:
                self._large_text = large_text
            if buttons is not None:
                self._buttons = buttons
            self._dirty = True
        self._wake.set()

    def stop(self) -> None:
        """Durumu temizleyip bağlantıyı kapatır."""
        if self._thread is None:
            self._stopping = True
            return
        self._stopping = True
        self._wake.set()
        self._thread.join(timeout=2.0)
        self._thread = None

    def refresh_setting(self) -> None:
        """Ayar değiştiğinde çağrılıyor: açıldıysa başlat, kapandıysa durdur."""
        if enabled(self._store):
            self._stopping = False
            self.start()
            with self._lock:
                self._dirty = True
            self._wake.set()
        else:
            self.stop()

    # --- iç işleyiş ---------------------------------------------------

    def _loop(self) -> None:
        while not self._stopping:
            try:
                self._tick()
            except Exception:
                # Presence bir süs; hiçbir hatası uygulamayı ilgilendirmiyor.
                self._drop()
            self._wake.wait(TICK)
            self._wake.clear()

        self._clear_and_close()

    def _tick(self) -> None:
        now = time.monotonic()

        if self._pipe is None:
            if now < self._next_connect:
                return
            self._next_connect = now + RECONNECT_INTERVAL
            pipe = _Pipe.connect()
            if pipe is None:
                return
            try:
                pipe.send(OP_HANDSHAKE, {"v": 1, "client_id": self._client_id})
            except OSError:
                pipe.close()
                return
            self._pipe = pipe
            self._last_send = 0.0
            with self._lock:
                self._dirty = True

        self._pipe.drain()

        with self._lock:
            dirty = self._dirty
        # Değişiklik yoksa da belli aralıklarla tazeleniyor.
        bayat = self._last_send and now - self._last_send >= HEARTBEAT_INTERVAL
        if not dirty and not bayat:
            return
        if self._last_send and now - self._last_send < MIN_SEND_INTERVAL:
            return

        self._pipe.send(OP_FRAME, self._activity_payload())
        self._last_send = now
        with self._lock:
            self._dirty = False

    def _activity_payload(self) -> dict:
        with self._lock:
            activity = {
                "details": self._details or "Odyssey",
                "state": self._state,
                "timestamps": {"start": self._started_at},
                "assets": {
                    "large_image": LARGE_IMAGE,
                    "large_text": self._large_text or "Odyssey",
                },
            }
            if self._buttons:
                activity["buttons"] = self._buttons[:2]
        if not activity["state"]:
            del activity["state"]
        return {
            "cmd": "SET_ACTIVITY",
            "args": {"pid": os.getpid(), "activity": activity},
            "nonce": f"odyssey-{time.time_ns()}",
        }

    def _drop(self) -> None:
        if self._pipe is not None:
            self._pipe.close()
            self._pipe = None
        self._next_connect = time.monotonic() + RECONNECT_INTERVAL

    def _clear_and_close(self) -> None:
        """Uygulama kapanırken Discord'daki yazıyı siliyor.

        Gönderilmezse Discord bağlantı kopana kadar eski durumu göstermeye
        devam ediyor ve kullanıcı kapattığı uygulamayı kullanıyor gibi
        görünüyor.
        """
        if self._pipe is None:
            return
        try:
            self._pipe.send(
                OP_FRAME,
                {
                    "cmd": "SET_ACTIVITY",
                    "args": {"pid": os.getpid(), "activity": None},
                    "nonce": f"odyssey-clear-{time.time_ns()}",
                },
            )
            self._pipe.send(OP_CLOSE, {})
        except OSError:
            pass
        self._pipe.close()
        self._pipe = None
