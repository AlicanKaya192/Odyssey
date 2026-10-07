**Yapman gerekenler:** `commands.sh` dosyasına sırayla dört komut yaz:

1. `site` imajını arka planda, `web` adıyla çalıştır; bilgisayarın 8080'i
   konteynerin 8000'ine gitsin.
2. `web`'in portlarının nereye yayınlandığını göster.
3. `site`'ı `local` adıyla çalıştır; port yalnızca bu bilgisayardan
   ulaşılsın: `127.0.0.1`'in 9000'i → konteynerin 8000'i.
4. `site`'ı `random` adıyla çalıştır; `EXPOSE` edilen portlar rastgele boş
   portlara yayınlansın.
