`installed` paket → kurulu sürüm; `advisories` listesindeki her öğe
`[paket, duzeltilen_surum]`. `patch_plan(installed, advisories)` kurulu
olup sürümü düzeltilenden **eski** olan her paket için
`"<paket>: <kurulu> -> <duzeltilen>"` satırını döndürsün, pakete göre
abece sırasıyla. Kurulu olmayan paket atlanır. Sürümleri sayı demeti
olarak karşılaştır.

**Beklenen çıktı:**

```
fetcher: 8.9.0 -> 8.10.0
tlslib: 3.0.9 -> 3.0.13
```
