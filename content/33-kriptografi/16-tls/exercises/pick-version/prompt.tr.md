`pick_version(offered)` istemcinin önerdiği sürümlerden yalnızca güvenli
olanları kabul etsin: önce `"TLSv1.3"`, yoksa `"TLSv1.2"`; ikisi de yoksa
`"protocol_version"` hatası döndürsün. Başlangıç kodu en büyüğünü
alıyor, eski sürümler önerilince de kabul ediyor.

**Beklenen çıktı:**

```
TLSv1.3
TLSv1.2
protocol_version
```
