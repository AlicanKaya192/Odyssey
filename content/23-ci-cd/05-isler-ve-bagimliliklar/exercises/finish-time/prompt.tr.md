`finish_time(job, needs, minutes)` fonksiyonunu yaz. Hat başladıktan kaç dakika sonra `job`'ın biteceğini döndürsün:

- Hiçbir şey beklemeyen iş 0. dakikada başlar.
- Bir iş, beklediği işlerden **en geç** biteninin bittiği anda başlar.
- Bitiş = başlangıç + kendi süresi (`minutes[job]`).

Beklenen işlerin bitişini aynı fonksiyonla hesaplayabilirsin (özyineleme).

**Beklenen çıktı:**

```
lint 2
test 5
build 8
deploy 9
```
