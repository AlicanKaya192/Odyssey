Bir konteyner her an durdurulabiliyor: sen `docker stop` diyorsun, sunucu
yeniden başlıyor, yeni sürüm geliyor. Programın bu anda işini düzgün
bitirmesi gerekiyor.

## Durdurmanın sırası

1. Docker 1 numaralı sürece **SIGTERM** gönderiyor.
2. Bekliyor (varsayılan süre; `docker stop -t 30` ile 30 saniye).
3. Program hâlâ çalışıyorsa **SIGKILL**: program anında ölüyor, çıkış kodu
   137.

SIGKILL yakalanamıyor; program son sözünü söyleyemiyor. Amaç, programın
SIGTERM'de kendisi kapanması.

## Python'da SIGTERM'i yakalamak

```python
import signal
import sys
import time

running = True

def stop(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, stop)

while running:
    print("working", flush=True)
    time.sleep(1)

print("saved, bye", flush=True)
```

Döngü her turda `running`'e bakıyor; SIGTERM gelince döngü biter, son iş
yapılır ve program 0 koduyla çıkar.

## `flush=True` neden?

Python ekrana yazdıklarını önce bir ara belleğe koyuyor ve topluca
gönderiyor. Terminal olmadan (konteynerde `-d` ile) bu ara bellek
**dolana kadar** hiçbir şey görünmeyebiliyor; `docker logs` boş görünür.
İki çözüm:

- `print(..., flush=True)`,
- ya da imajda `ENV PYTHONUNBUFFERED=1` (Ortam Değişkenleri bölümü).

## `--init` ne yapıyor?

`docker run --init` konteynerde programdan önce çok küçük bir başlatıcı
(`tini`) çalıştırıyor. 1 numaralı süreç o oluyor; sinyalleri programa
iletiyor ve programın bıraktığı "yetim" süreçleri topluyor. Programına
dokunamıyorsan iyi bir çözüm. Compose'da `init: true` yazılıyor.

## Kontrol listesi

- [ ] `CMD` / `ENTRYPOINT` exec biçiminde.
- [ ] Program SIGTERM'i yakalıyor (ya da `--init` var).
- [ ] Uzun işler küçük parçalara bölünmüş; kapanış isteği parça aralarında
      denetleniyor.
- [ ] Çıktılar `flush` ediliyor.
