Her çalıştırmada bütün paketler yeniden iniyor. Kurulumdan **önce** bir `actions/cache@v4` adımı ekle:

- `path`: `~/.cache/pip`
- `key`: `pip-`, işletim sistemi (`runner.os`) ve `requirements.txt`'nin özeti (`hashFiles`)
- `restore-keys`: tam anahtar yoksa `pip-<işletim sistemi>-` önekiyle en yeni önbellek
