Patika bitti; öğrendiklerin kalıcı olsun diye kendi başına yapabileceğin
işler ve sonraki adımlar.

## Kendi projelerinle pratik

1. Daha önce yazdığın bir Python programını (bir alıştırma, bir betik)
   paketle: Dockerfile, `.dockerignore`, root olmayan kullanıcı.
2. `docker history` ile katmanlarına bak; önbellek sırasını düzelt, kodu
   değiştirip yeniden kurunca hangi adımların `CACHED` olduğunu gör.
3. Programa bir volume ekle: konteyneri silip yeniden aç, veri yerinde mi?
4. İkinci bir servis ekle (bir API ve onu çağıran bir program) ve
   `compose.yaml` ile ikisini birlikte aç.

## Küçük bir proje fikri

Dersteki not API'sini büyüt:

- Notu silen bir uç nokta (`DELETE /notes/1`).
- Ayrı bir `worker` servisi: her dakika `/stats`'a bakıp sonucu günlüğe
  yazsın; `depends_on` + `service_healthy`.
- Veritabanının yedeğini alan tek satırlık bir komut (Volume bölümündeki
  `tar` yöntemi).
- İmajı çok aşamalı derlemeyle küçültmeyi dene ve boyutu ölç.

## Bundan sonra öğrenilecekler

- **Bir imaj deposuna göndermek:** `docker tag` ve `docker push` ile
  imajını Docker Hub'a (ya da GitHub'ın deposuna) koymak; başka bir
  bilgisayar `docker pull` ile alıyor.
- **Otomatik derleme:** her değişiklikte imajı bir CI hizmetinin (GitHub
  Actions gibi) kurması.
- **Sunucuda çalıştırmak:** aynı `compose.yaml`'ı bir sunucuda farklı
  `.env` ile açmak.
- **Çok sayıda konteyneri yönetmek:** Kubernetes gibi araçlar Compose'un
  yaptığını birçok bilgisayara yayıyor; temeli bu patikada öğrendiklerin.

## Sıradaki patikalar

- **FastAPI ile REST API yazmak:** kendi API'ni yazıp bu patikada
  öğrendiğin gibi paketleyeceksin.
- **Makine Öğrenmesi:** eğittiğin bir modeli bir API'nin arkasına koyup
  konteynerle dağıtmak, iki patikanın buluştuğu yer.

## Akılda kalsın

> Konteyner gelip geçici, imaj tekrar üretilebilir, veri volume'da kalıcı.
> Bir şey ters gidince önce aşamayı bul: kurulumda mı, çalışırken mi?
