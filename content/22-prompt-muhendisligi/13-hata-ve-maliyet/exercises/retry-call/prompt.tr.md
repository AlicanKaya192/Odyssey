`retry(spec, attempts, window)` hazır `make_script` ile kurulan senaryoyu
(`"429"` ve `"503"` hata, geri kalanı cevap) `ChatClient(...,
context_window=window)` ile çağırsın (`MESSAGES`, `max_tokens=40`).
Geçici hatada `2.0 ** attempt` saniyelik beklemeyi listeye ekleyip yeniden
denesin; `[cevap, beklemeler]` döndürsün. Denemeler bitince `["gave up",
beklemeler]`, `ContextLengthError`'da hemen `["too long", beklemeler]`.

**Beklenen çıktı:**

```
['ok', [1.0, 2.0]]
['gave up', [1.0, 2.0]]
['too long', []]
```
