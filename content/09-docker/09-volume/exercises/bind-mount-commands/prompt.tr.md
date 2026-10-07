PowerShell'de şu anki klasör `${PWD}`.

**Yapman gerekenler:** `commands.sh` dosyasına sırayla üç komut yaz:

1. Şu anki klasörü `/app`'e bağla, konteynerin çalışma klasörü `/app` olsun
   (`-w`) ve `python:3.13-slim` imajında `python app.py` çalıştır; bitince
   silinsin.
2. `app` imajını, şu anki klasörün `config` alt klasörü `/config`'e **salt
   okunur** bağlı olarak çalıştır; bitince silinsin.
3. `notes` volume'unu `/data`'ya, şu anki klasörü `/backup`'a bağlayıp
   `alpine:3.22`'de `tar czf /backup/notes.tgz -C /data .` çalıştır; bitince
   silinsin. (Uzun satırı `` ` `` ile bölebilirsin.)
