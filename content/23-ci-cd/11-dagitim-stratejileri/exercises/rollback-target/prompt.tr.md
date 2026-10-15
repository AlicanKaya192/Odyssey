`rollback_target(history)` fonksiyonunu yaz. `history` dağıtımların listesi, eskiden yeniye; her öğe `[sürüm, durum]` ve durum `"ok"` ya da `"failed"`. **Son öğe şu an çalışan dağıtım.**

Geri dönülecek sürüm: ondan önceki dağıtımlar arasında, durumu `"ok"` olan ve **şu anki sürümden farklı** en yeni sürüm. Yoksa `None`.

Listeyi sondan başa gezmek için `reversed(...)` kullanılabilir.

**Beklenen çıktı:**

```
1.2.1
None
None
1.0.0
```
