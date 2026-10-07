Bu imaj programı root olarak çalıştırıyor.

**Yapman gerekenler:**

1. `useradd --create-home --uid 1000 app` ile `app` kullanıcısını oluştur.
2. Konteyner `app` kullanıcısıyla çalışsın (`USER`).

**Beklenen çıktı:**

```
running as app
```
