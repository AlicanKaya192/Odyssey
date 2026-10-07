`greet.py` kendisine verilen adı selamlıyor. Şu an `docker run app Ada`
programı değil `Ada` adlı bir komutu çalıştırmaya kalkıyor.

**Yapman gereken:** komutu sabitle, adı değişebilir yap:

1. `ENTRYPOINT` exec biçiminde `python greet.py`.
2. `CMD` exec biçiminde varsayılan ad: `world`.

Odyssey iki kez çalıştıracak:

```
docker run app      ->  hello world
docker run app Ada  ->  hello Ada
```
