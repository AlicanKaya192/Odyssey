`worker.py` bir döngüde çalışıyor ve durdurulunca `saved, bye` yazıp
kapanmalı. Şu an SIGTERM'i yakalamıyor: sinyal gelince program anında ölüyor
ve son satır hiç yazılmıyor.

**Yapman gereken:** `worker.py`'de SIGTERM'i yakala:

1. `signal` modülünü içe aktar.
2. `running` değişkenini `False` yapan bir fonksiyon yaz (`global running`).
3. `signal.signal(signal.SIGTERM, fonksiyon)` ile bağla.

Odyssey programı başlatıp bir saniye sonra ona SIGTERM gönderecek ve programın
nasıl bittiğine bakacak.

**Beklenen çıktı:**

```
saved, bye
exit=0
```
