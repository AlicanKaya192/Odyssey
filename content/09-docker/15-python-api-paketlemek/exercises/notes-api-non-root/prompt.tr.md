Bu Dockerfile çalışıyor ama program root ve veritabanını `/app`'e yazıyor.

**Yapman gerekenler:**

1. `ENV`'e `DB_PATH=/data/notes.db` ekle.
2. Tek bir `RUN`'da: `useradd --create-home --uid 1000 app`, `/data`
   klasörünü oluştur ve sahibini `app:app` yap.
3. Paket kurulumundan sonra `USER app`.

Odyssey konteyneri `/data`'ya bir volume bağlayarak **iki kez** çalıştıracak
ve `/stats`'a bakacak. Veri volume'da kaldığı için ikinci seferde program
iki kez başladığını biliyor:

```
{"notes": 0, "starts": 1}
{"notes": 0, "starts": 2}
```
