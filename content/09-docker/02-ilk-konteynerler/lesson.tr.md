# İlk Konteynerler

Kurulumda `hello-world` ile ilk konteynerini çalıştırdın: açıldı, bir mesaj
yazdı, kapandı. Bu bölümde konteynerlerle gerçekten oynayacağız: içine
gireceğiz, arka planda çalıştıracağız, durdurup yeniden başlatacağız ve
sileceğiz.

Bu bölümün komutlarını PowerShell'de kendin de çalıştır. Konteynerler
bilgisayarına zarar vermiyor; en kötü ihtimalle silip yeniden başlarsın.

## Bir konteynere komut vermek

`docker run`'a imajın adından sonra bir komut yazarsan konteyner o komutu
çalıştırıyor:

```text
docker run alpine:3.22 echo "Merhaba konteyner"
```

```text
Merhaba konteyner
```

Olan şu: Docker `alpine:3.22` imajından yeni bir konteyner oluşturdu,
içinde `echo` komutunu çalıştırdı, komut bitti ve konteyner de bitti.

**Konteyner, içindeki program çalıştığı sürece yaşar.** Program bitince
konteyner de durur. Bu bölümün en önemli cümlesi bu.

İmajın adından sonra gelen her şey konteynerin içinde çalışacak komut:

```text
docker run alpine:3.22 ls /
docker run alpine:3.22 cat /etc/os-release
docker run python:3.13-slim python -c "print(2 ** 10)"
```

## Konteynerleri listelemek

Çalışan konteynerleri `docker ps` gösteriyor (ps: process status, süreç
durumu):

```text
docker ps
```

Az önce çalıştırdıkların listede yok; çünkü hepsi bitti. **Bitmiş olanlar
dahil hepsini** görmek için `-a` (all, hepsi):

```text
docker ps -a
```

```text
CONTAINER ID   IMAGE              STATUS                     NAMES
7c80c00c94a5   python:3.13-slim   Exited (0) 5 seconds ago   eager_hopper
3f1d2b9a6e44   alpine:3.22        Exited (0) 9 seconds ago   jolly_lamport
```

Gerçek çıktıda `COMMAND` (çalıştırılan komut), `CREATED` (ne zaman
oluşturuldu) ve `PORTS` sütunları da var; sığsın diye burada çıkardık.

- **CONTAINER ID**: konteynerin kimliği (ilk 12 karakteri).
- **STATUS**: `Exited (0)` → bitti, çıkış kodu 0 (sorunsuz). `Up 3 minutes`
  → çalışıyor.
- **NAMES**: ad. Sen vermezsen Docker iki rastgele kelime seçiyor.

Bitmiş konteynerler silinene kadar orada duruyor. Her `docker run` **yeni**
bir konteyner oluşturuyor; aynı komutu on kez çalıştırırsan listede on
konteyner olur.

## İsim vermek ve kendiliğinden silmek

Rastgele adlarla uğraşmamak için `--name`:

```text
docker run --name greeter alpine:3.22 echo hi
```

Aynı adla ikinci bir konteyner oluşturulamaz; eskisini silmeden aynı komutu
yeniden çalıştırırsan şu hatayı alırsın:

```text
docker: Error response from daemon: Conflict. The container name "/greeter"
is already in use by container "ed8f7979...". You have to remove (or rename)
that container to be able to reuse that name.
```

Denemelik konteynerlerin birikmesini istemiyorsan `--rm`: konteyner bitince
**kendiliğinden siliniyor**.

```text
docker run --rm alpine:3.22 echo "iz bırakmadan"
```

## İçine girmek: `-it`

Bir konteynerin içinde terminal açabilirsin. Alpine'da kabuk (komut
yorumlayıcı) programının adı `sh`:

```text
docker run -it --rm alpine:3.22 sh
```

- `-i` (interactive): klavyeden yazdıklarını konteynere ilet.
- `-t` (tty): ona bir terminal ver (komut satırı düzgün görünsün).
- İkisi hep birlikte kullanıldığı için `-it` diye yazılıyor.

Komut satırı değişiyor; artık konteynerin içindesin:

```text
/ # ls
bin    dev    etc    home   lib    media  mnt    opt    proc
root   run    sbin   srv    sys    tmp    usr    var
/ # cat /etc/os-release
NAME="Alpine Linux"
...
/ # exit
```

`exit` yazınca kabuk bitiyor, dolayısıyla konteyner de bitiyor (`--rm`
verdiğin için siliniyor da).

## Konteyner tek kullanımlık

Şunu dene:

```text
docker run -it --rm alpine:3.22 sh
/ # echo "not" > /note.txt
/ # cat /note.txt
not
/ # exit

docker run -it --rm alpine:3.22 sh
/ # cat /note.txt
cat: can't open '/note.txt': No such file or directory
```

İkinci konteyner **aynı imajdan ama yeni**; birincide yazdığın dosya onda
yok. İmaj değişmiyor; konteynerin içinde yaptığın değişiklik yalnızca o
konteynerde, o da silinince kayboluyor.

<figure class="fig">
  <div class="flow">
    <span class="node acc">İmaj: alpine:3.22<br><small>değişmez, salt okunur</small></span><span class="arrow">→</span>
    <span class="node">Konteyner 1<br><small>/note.txt yazıldı</small></span><span class="arrow">→ silindi →</span>
    <span class="node no">Not de gitti</span>
  </div>
  <figcaption>Her konteyner imajın üstüne kendi ince, yazılabilir katmanını ekliyor. Konteyner silinince o katman da gidiyor; imaj hep aynı kalıyor.</figcaption>
</figure>

Kalıcı veri nasıl saklanır? Volume bölümünde. Şimdilik kural şu:
**konteynere önemli bir şey yazma; konteyner her an silinip yeniden
oluşturulabilir olmalı.**

## Arka planda çalıştırmak: `-d`

Bazı programlar hiç bitmiyor: bir web sunucusu, bir veritabanı. Onları
terminali kilitlemeden arka planda çalıştırmak için `-d` (detached,
ayrık):

```text
docker run -d --name sleeper alpine:3.22 sleep 300
```

```text
3b8f6c1e0a9d4f27c5e1b2a3d4c5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3
```

Docker yalnızca konteynerin uzun kimliğini yazıp terminali sana geri
veriyor. `sleep 300` 300 saniye bekleyen bir komut; konteyner bu sürede
**çalışıyor**:

```text
docker ps
```

```text
CONTAINER ID   IMAGE         STATUS          NAMES
3b8f6c1e0a9d   alpine:3.22   Up 12 seconds   sleeper
```

## Çalışan konteynerle konuşmak

**Çıktısını görmek** (`logs`):

```text
docker logs sleeper
docker logs -f sleeper      # -f: canlı izle (Ctrl+C ile çık)
```

**İçinde komut çalıştırmak** (`exec`): çalışan konteynerin içinde ikinci bir
komut başlatıyor.

```text
docker exec sleeper ps
```

```text
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 300
    7 root      0:00 ps
```

Konteynerin içinde yalnızca iki program var: 1 numaralı süreç olarak
`sleep 300` (konteynerin asıl programı) ve senin çalıştırdığın `ps`.
Bilgisayarındaki yüzlerce program buradan görünmüyor; konteynerin "kendi
dünyası" bu.

İçine kabukla girmek de aynı yoldan:

```text
docker exec -it sleeper sh
```

`run` yeni bir konteyner oluşturuyor; `exec` **var olan, çalışan**
konteynerin içinde komut çalıştırıyor. Karıştırılan ikili bu.

## Durdurmak, başlatmak, silmek

```text
docker stop sleeper     # durdur (programa kapanması için en çok 10 sn verir)
docker start sleeper    # durmuş konteyneri yeniden başlat
docker rm sleeper       # sil (önce durdurulmuş olmalı)
docker rm -f sleeper    # çalışıyor olsa da zorla durdur ve sil
```

Çalışan bir konteyneri `-f` olmadan silmeye çalışırsan Docker durmanı
istiyor: `container is running: stop the container before removing or force
remove`.

Konteyneri adıyla ya da kimliğinin ilk birkaç harfiyle (`docker stop 3b8f`)
gösterebilirsin.

<figure class="fig">
  <div class="flow">
    <span class="node">İmaj</span><span class="arrow">→ run →</span>
    <span class="node ok">Çalışıyor<br><small>Up</small></span><span class="arrow">→ stop →</span>
    <span class="node">Durdu<br><small>Exited</small></span><span class="arrow">→ rm →</span>
    <span class="node no">Silindi</span>
  </div>
  <figcaption>Program kendisi bitince de konteyner durur. Durmuş konteyner <code>start</code> ile yeniden çalışır; <code>rm -f</code> çalışanı da doğrudan siler.</figcaption>
</figure>

## Toplu temizlik

Denemeler biriktiyse durmuş konteynerlerin hepsini silmek için:

```text
docker container prune
```

Docker neyi sileceğini söyleyip onay istiyor. Çalışan konteynerlere
dokunmuyor.

## Özet

- `docker run imaj komut` → yeni bir konteyner oluşturup komutu çalıştırır.
  **Program bitince konteyner de biter.**
- `docker ps` çalışanları, `docker ps -a` hepsini listeler.
- `--name ad` isim verir, `--rm` bitince siler, `-it` içine girer, `-d`
  arka planda çalıştırır.
- `logs` çıktıyı gösterir, `exec` çalışan konteynerde komut çalıştırır.
- `stop` / `start` / `rm` (`-f` zorla); `docker container prune` durmuşları
  temizler.
- Konteyner tek kullanımlık: içinde yazdığın şey konteyner silinince
  kaybolur, imaj değişmez.
