Docker Desktop yalnızca motoru çalıştıran pencere değil; terminalde
yazdığın komutların sonucunu görsel olarak da gösteriyor. Patika boyunca
komutla yaptığın her şeyi burada da izleyebilirsin.

## Sol menü

| Bölüm | Ne gösteriyor? | Terminaldeki karşılığı |
|---|---|---|
| **Containers** | Çalışan ve durmuş konteynerler: ad, imaj, durum, portlar. | `docker ps -a` |
| **Images** | Bilgisayardaki imajlar ve boyutları. | `docker images` |
| **Volumes** | Konteyner silinse de kalan veri alanları. | `docker volume ls` |
| **Builds** | `docker build` geçmişi: hangi adım ne kadar sürdü, hangisi önbellekten geldi. | `docker build` çıktısı |

## Konteyner satırı

Containers listesinde her konteynerin satırında:

- **Name**: konteynerin adı (sen vermezsen Docker iki rastgele kelime
  seçiyor, ör. `happy_turing`).
- **Image**: hangi imajdan çalıştırıldığı.
- **Status**: `Running` (çalışıyor) ya da `Exited` (bitti).
- **Port(s)**: dışarıya açılan port varsa tıklanabilir bağlantı.
- Sağda **durdur / başlat / sil** düğmeleri.

Satıra tıklayınca konteynerin **Logs** (çıktısı), **Inspect** (ayarları),
**Exec** (içinde komut çalıştırma) ve **Files** (dosyaları) sekmeleri
açılıyor. Hata ayıklarken çok işe yarıyor; Hata Ayıklama bölümünde terminal
karşılıklarını göreceğiz.

## Alt çubuk

- Sol altta **Engine running** ve yeşil nokta: motor çalışıyor.
- Yanında bellek ve işlemci kullanımı.

## Ayarlar (sağ üstteki dişli)

- **General › Start Docker Desktop when you sign in**: bilgisayar açılınca
  kendiliğinden başlasın.
- **Resources**: Docker'ın kullanabileceği bellek ve işlemci (WSL 2
  kullanırken bu sınırları Windows yönetiyor).
- **Docker Engine**: motorun ayar dosyası. Ne yaptığını bilmeden
  değiştirme.

## Görev çubuğundaki balina

Görev çubuğunun sağında küçük bir balina simgesi var. Sağ tıklayınca:

- **Quit Docker Desktop**: motoru durdurup kapatır.
- **Restart**: motoru yeniden başlatır.
- **Dashboard**: pencereyi açar.

Docker Desktop penceresini çarpıdan kapatmak motoru **durdurmuyor**;
konteynerlerin çalışmaya devam ediyor.

## Komut mu, pencere mi?

İkisi aynı işi yapıyor. Bu patikada **komutları** öğreniyoruz, çünkü:

- sunucularda pencere yok, yalnızca terminal var,
- komutlar bir dosyaya yazılıp tekrarlanabiliyor,
- hata mesajları terminalde daha açık.

Docker Desktop'ı ise "ne oldu?" sorusuna hızlı bakmak için kullan.
