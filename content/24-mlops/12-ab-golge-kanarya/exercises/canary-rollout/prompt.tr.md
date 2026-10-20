Kanaryanın günlük kararlarını işleyen `rollout(stages, decisions)` fonksiyonunu yaz:

- `stages`: paylar, örneğin `[1, 5, 25, 100]`. Yayın ilk paydan başlar.
- Her karar için: `"advance"` bir sonraki paya geçer (son paydaysa orada kalır), `"wait"` aynı payda kalır, `"rollback"` payı `0` yapar ve yayını bitirir (sonraki kararlar işlenmez).
- Her karardan sonraki payı bir listeye ekle ve listeyi döndür.

**Beklenen çıktı:**

```
[1, 5, 25, 100, 100]
[5, 0]
[]
```
