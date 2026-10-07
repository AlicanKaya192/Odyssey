`docker ps -a` konteyneri `Exited (127)` gösteriyor ve `docker run` şunu
yazıyor:

```text
exec: "pyhton": executable file not found in $PATH
```

**Yapman gereken:** çıkış kodu 127 "komut bulunamadı" demek. Komutu düzelt.

**Beklenen çıktı:**

```
debugged and running
```
