Bu Dockerfile bugün çalışıyor ama `latest` yüzünden yarın başka bir Python
sürümüyle kurulabilir.

**Yapman gereken:** `FROM` satırını, sürümü sabitlenmiş `python:3.13-slim`
imajını kullanacak şekilde değiştir. Odyssey imajı kurup çalıştıracak.

**Beklenen çıktı:**

```
pinned and ready
```
