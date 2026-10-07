**Yapman gerekenler:** `commands.sh` dosyasına iki komut yaz:

1. `app` imajını arka planda, `api` adıyla çalıştır: dosya sistemi salt
   okunur, bütün özel yetkiler kaldırılmış (`--cap-drop ALL`), bellek sınırı
   `512m`.
2. `app` imajında 1000 numaralı kullanıcıyla `id` komutunu çalıştır; bitince
   silinsin.

`--privileged` kullanma.
