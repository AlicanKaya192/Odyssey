# Hata Ayıklama

Docker'la çalışırken iki tür hata var: **imaj kurulamıyor** ya da **imaj
kuruluyor ama konteyner çalışmıyor**. İkisinin ipuçları farklı yerlerde
duruyor. Bu bölüm sorunu nerede arayacağını ve hangi aracı kullanacağını
sırayla anlatıyor.

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>İmaj kurulamıyor</h4><p><code>docker build</code> çıktısının son satırları</p><p>Düşen adım: <code>[3/5] RUN ...</code></p><p><code>--progress=plain --no-cache</code></p></div>
    <div class="dim"><h4>Konteyner çalışmıyor</h4><p><code>docker ps -a</code> → çıkış kodu</p><p><code>docker logs</code> → son sözler</p><p><code>--entrypoint sh</code> → içine bak</p></div>
  </div>
  <figcaption>Önce hatanın hangi aşamada olduğunu belirle; ipuçları farklı yerlerde.</figcaption>
</figure>

## 1. Derleme hataları

Derleme düşünce Docker son satırlarda **hangi adımın** düştüğünü yazıyor.
Önce ona bak.

**Yazım hatası:**

```text
ERROR: failed to build: failed to solve: dockerfile parse error on line 1:
unknown instruction: FORM (did you mean FROM?)
```

Satır numarası ve öneri birlikte geliyor.

**Bağlamda olmayan dosya:**

```text
failed to calculate checksum of ref ...: "/app.pyy": not found
```

Dosyanın adı yanlış ya da `.dockerignore` onu dışarıda bırakıyor.

**Bir `RUN` komutunun düşmesi:**

```text
ERROR: failed to build: failed to solve: process "/bin/sh -c false"
did not complete successfully: exit code: 1
```

Çalışan komut tırnak içinde. Asıl sebep genellikle bu satırın **üstünde**:
komutun kendi yazdığı hata (pip'in "No matching distribution", bir Python
hatası...). Çıktının tamamını görmek için:

```text
docker build --progress=plain --no-cache -t app .
```

`--progress=plain` her adımın bütün çıktısını düz metin yazıyor,
`--no-cache` adımı önbellekten getirmeyip gerçekten çalıştırıyor.

## 2. Çalışma hataları

İmaj kuruldu, konteyner başlıyor ama hemen bitiyor ya da yanlış çalışıyor.

**Adım 1: Konteynerin durumu.**

```text
docker ps -a
```

`Exited (1) Less than a second ago` → program hatayla bitti. Çıkış koduna
göre (İlk Konteynerler bölümünün notu): 1 program hatası, 125 Docker
başlatamadı, 127 komut bulunamadı, 137 öldürüldü.

**Adım 2: Programın son sözleri.**

```text
docker logs web
```

```text
Traceback (most recent call last):
  File "/app/main.py", line 1, in <module>
    from helpers import greet
ModuleNotFoundError: No module named 'helpers'
```

Python'un hata çıktısı burada da aynı. `helpers.py` imajda yok: Dockerfile
yalnızca `main.py`'yi kopyalamış.

**Adım 3: İmajın içine bak.** Konteyner çok çabuk bittiği için içine
`exec` ile girilemiyor. Aynı imajdan, komutu değiştirerek **yeni** bir
konteyner aç:

```text
docker run --rm -it --entrypoint sh app
# ls -la /app
```

ya da tek komutla:

```text
docker run --rm --entrypoint ls app -la /app
-rwxr-xr-x 1 root root   41 Oct  6 20:26 main.py
```

Yalnızca `main.py` var; tahmin doğrulandı.

## 3. Daha fazla araç

| Komut | Ne gösterir? |
|---|---|
| `docker inspect web` | Konteynerin bütün ayarları (komut, ortam, bağlamalar, çıkış kodu) |
| `docker logs --tail 50 -f web` | Son 50 satır ve sonrası canlı |
| `docker exec -it web sh` | Çalışan konteynerin içinde kabuk |
| `docker cp web:/app ./copied` | Konteynerden bilgisayara dosya kopyalar (durmuş olsa da) |
| `docker diff web` | Konteynerin imaja göre eklediği (A) ve değiştirdiği (C) dosyalar |
| `docker image inspect app` | İmajın ayarları (CMD, ENV, WORKDIR, USER) |

## 4. Sık karşılaşılan durumlar

| Belirti | Büyük ihtimalle | Bak |
|---|---|---|
| `No module named 'x'` | Dosya kopyalanmamış ya da paket kurulmamış | `ls /app`, requirements.txt |
| `can't open file '/app/app.py'` | Dosya başka klasöre kopyalanmış; WORKDIR ile COPY uyuşmuyor | `ls` ile dosyanın yeri |
| `exec: "pyhton": executable file not found` (127) | Komutta yazım hatası | `CMD` satırı |
| Konteyner hemen `Exited (0)` | Program işini bitirdi (sunucu değil) ya da CMD yanlış | `docker inspect` → Cmd |
| `Permission denied` | `USER` sonrası root'un klasörüne yazılıyor | `chown` (Güvenlik) |
| Sayfa açılmıyor | Port, 0.0.0.0 ya da program çökmüş | Portlar bölümü notu |
| Değişiklik görünmüyor | Eski imaj çalışıyor; yeniden kurulmadı | `docker build`, `up --build` |

## 5. Yöntem

1. **Hangi aşama?** Derleme mi, çalışma mı?
2. **Son satırları oku.** Hata neredeyse her zaman son on satırda.
3. **Tahmin et, doğrula.** "Dosya yok" diyorsa içine bak (`ls`), "port"
   diyorsa `docker port`.
4. **Bir şeyi değiştir, yeniden dene.** Aynı anda üç şeyi değiştirirsen
   hangisinin düzelttiğini bilemezsin.

## Özet

- Derleme hatasında düşen adıma ve üstündeki satırlara bak;
  `--progress=plain --no-cache` bütün çıktıyı gösterir.
- Çalışma hatasında sıra: `docker ps -a` (çıkış kodu) → `docker logs` →
  imajın içine `--entrypoint sh` ile bak.
- `inspect`, `exec`, `cp`, `diff` konteyneri incelemek için.
- Tahmin et, tek bir şeyi değiştir, doğrula.
