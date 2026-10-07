Sayaç `/data`'ya yazıyor ve imaj `app` kullanıcısıyla çalışıyor. Boş bir
volume ilk bağlandığında imajdaki klasörün sahibini alıyor; klasör root'a
aitse `app` yazamıyor.

**Yapman gereken:** `VOLUME` satırından önce, tek bir `RUN` ile `/data`'yı
oluştur ve sahibini `app` yap.

Odyssey iki ayrı konteyneri aynı volume'la çalıştıracak.

**Beklenen çıktılar:**

```
count: 1
count: 2
```
