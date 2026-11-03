`advisories`'teki her duyuru `[paket, ortaya_cikti, duzeltildi, kimlik]`.
`affected(installed, advisories)` kurulu sürümü `ortaya_cikti <= surum <
duzeltildi` aralığında olan her paket için `"<paket> <surum>: <kimlik>"`
satırını abece sırasıyla döndürsün. Kurulu olmayan paket atlanır.
Sürümleri sayı demeti olarak karşılaştır.

**Beklenen çıktı:**

```
pool 0.4.2: ADV-3
web 2.3.1: ADV-1
```
