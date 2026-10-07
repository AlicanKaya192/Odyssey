# CMD, ENTRYPOINT ve Argümanlar

Şimdiye kadar konteynerin ne çalıştıracağını `CMD` ile söyledin. Bu bölümde
konteyner açılırken çalışan komutun bütün ayrıntısına bakacağız: `CMD`'yi
dışarıdan değiştirmek, iki yazım biçimi arasındaki fark, `ENTRYPOINT` ile
konteyneri bir komut satırı aracına çevirmek ve `docker stop`'un programı
nasıl kapattığı.

## `CMD` yalnızca varsayılan

`CMD` konteynerin **varsayılan** komutu: `docker run`'a komut verilmezse
çalışan. Komut verilirse `CMD`'nin **tamamı** onunla değişiyor:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

```text
docker run --rm greeter                                  # python app.py
docker run --rm greeter python -c "print('başka iş')"    # CMD yok sayıldı
```

İkinci satırda `app.py` hiç çalışmadı: imajın adından sonra yazdığın her
şey `CMD`'nin yerine geçti.

## İki biçim: exec ve shell

`CMD` iki biçimde yazılabiliyor:

```dockerfile
CMD ["python", "app.py"]     # exec biçimi (köşeli parantez, JSON)
CMD python app.py            # shell biçimi
```

Fark görünenden büyük. Shell biçiminde Docker komutu kendisi bir kabuğa
veriyor; imajın içine yazılan aslında şu:

```text
docker image inspect demo --format "{{.Config.Cmd}}"
[/bin/sh -c python app.py]
```

Yani konteynerin asıl programı (1 numaralı süreç) **Python değil `sh`**;
Python onun altında çalışıyor. İki sonucu var:

**1. Değişkenler.** Kabuk `$AD` gibi değişkenleri açıyor; exec biçimi açmıyor.

```dockerfile
ENV NAME=Ada
CMD echo hi $NAME            # çıktı: hi Ada
CMD ["echo", "hi $NAME"]     # çıktı: hi $NAME  (olduğu gibi)
```

Exec biçiminde değişken gerekiyorsa kabuğu açıkça çağır:
`CMD ["sh", "-c", "echo hi $NAME"]`.

**2. Kapanış sinyali.** Bir sonraki başlıkta.

Kural: **varsayılan olarak exec biçimini kullan.** Shell biçimi yalnızca
gerçekten kabuk özelliği (değişken, `&&`, `|`) gerektiğinde ve o zaman da
`["sh", "-c", "..."]` olarak.

## `docker stop` nasıl kapatıyor?

`docker stop` konteynerin 1 numaralı sürecine **SIGTERM** gönderiyor:
"kapanman isteniyor, işini toparla". Bir süre bekliyor; program kapanmazsa
**SIGKILL** ile zorla öldürüyor (çıkış kodu 137).

Aynı programla üç deneme yaptık; program 600 saniye uyuyordu ve
`docker stop` çağrıldı:

| Nasıl çalıştı | `docker stop` süresi | Çıkış kodu |
|---|---|---|
| `CMD ["python", "app.py"]` | 3,8 sn | 137 (zorla öldürüldü) |
| `CMD python app.py` (shell) | 3,7 sn | 137 (zorla öldürüldü) |
| SIGTERM'i yakalayan Python | 0,6 sn | 0 (düzgün kapandı) |

- **Shell biçiminde** sinyal `sh`'a gidiyor ve Python'a hiç ulaşmıyor.
- **Exec biçiminde** sinyal Python'a ulaşıyor ama 1 numaralı süreç olan bir
  program sinyali **kendisi yakalamazsa** Linux onu görmezden geliyor.
  Çözüm: programın sinyali dinlemesi.

```python
import signal
import sys

def stop(signum, frame):
    print("kapanıyorum, işi kaydediyorum", flush=True)
    sys.exit(0)

signal.signal(signal.SIGTERM, stop)
```

Ya da hiç dokunmadan Docker'a küçük bir başlatıcı ekletmek:
`docker run --init ...` sinyalleri programa iletiyor (program 143 koduyla
kapanıyor). Web çatıları (FastAPI'yi çalıştıran uvicorn gibi) SIGTERM'i
zaten yakalıyor.

Neden önemli? Zorla öldürülen program yarım dosya bırakabiliyor,
veritabanına yazdığı kaydı bitiremiyor.

## `ENTRYPOINT`: değişmeyen komut

`ENTRYPOINT` konteynerin **her zaman** çalışan komutu. `docker run`'a
verdiğin şeyler onu değiştirmiyor; **arkasına argüman olarak ekleniyor**.
`CMD` ise bu durumda varsayılan argümanlar oluyor:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY greet.py .
ENTRYPOINT ["python", "greet.py"]
CMD ["World"]
```

```text
docker run --rm greet                 # python greet.py World
docker run --rm greet Ada Lovelace    # python greet.py Ada Lovelace
```

<figure class="fig">
  <div class="flow">
    <span class="node acc">ENTRYPOINT<br><small>python greet.py</small></span><span class="arrow">+</span>
    <span class="node">CMD (varsayılan)<br><small>World</small></span><span class="arrow">ya da</span>
    <span class="node ok">docker run'a yazılanlar<br><small>Ada Lovelace</small></span>
  </div>
  <figcaption><code>ENTRYPOINT</code> hep çalışıyor; arkasına ya <code>CMD</code> ya da <code>docker run</code>'a imajdan sonra yazılanlar ekleniyor.</figcaption>
</figure>

`greet.py` argümanları Python'un `sys.argv` listesinden okuyor;
`sys.argv[1:]` imajın adından sonra yazılanlar (ya da `CMD`).

```python
import sys

names = sys.argv[1:]
print("Hello,", " ".join(names) + "!")
```

Böylece imaj bir **komut satırı aracı** gibi kullanılıyor: `docker run
--rm greet Ada`.

`ENTRYPOINT`'i bir kerelik değiştirmek gerekirse (ör. içine bakmak için):

```text
docker run --rm -it --entrypoint sh greet
```

## Hangisi ne zaman?

| Durum | Yaz |
|---|---|
| Bir uygulama, kişi başka bir şey çalıştırmak isteyebilir | Yalnızca `CMD ["python", "app.py"]` |
| İmaj tek bir aracın kendisi, argüman alıyor | `ENTRYPOINT ["python", "tool.py"]` + varsayılan `CMD ["--help"]` |
| Değişken ya da `&&` gerekiyor | `CMD ["sh", "-c", "..."]` |

`ENTRYPOINT` ve `CMD` birlikte yazılacaksa **ikisi de exec biçiminde**
olmalı. Shell biçimli `ENTRYPOINT` `CMD`'yi yok sayıyor.

## Özet

- `CMD` varsayılan komut; `docker run imaj komut` onu tamamen değiştirir.
- Exec biçimi (`["python", "app.py"]`) programı doğrudan, shell biçimi
  `/bin/sh -c` ile çalıştırır. Shell biçimi değişkenleri açar ama sinyali
  programa iletmez. **Varsayılan: exec.**
- `docker stop` önce SIGTERM, sonra SIGKILL (137) gönderir. Program
  SIGTERM'i yakalamalı ya da `--init` kullanılmalı.
- `ENTRYPOINT` değişmeyen komut; `docker run`'a yazılanlar ve `CMD` onun
  argümanı olur. `--entrypoint` bir kerelik değiştirir.
- Python argümanları `sys.argv[1:]`'den okur.
