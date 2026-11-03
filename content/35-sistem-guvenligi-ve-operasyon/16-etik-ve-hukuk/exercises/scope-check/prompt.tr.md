`scope_check(target, day, scope, excluded, window)` hedef adresi
(metin), günü (ISO metin), kapsam ağlarını (CIDR listesi), hariç tutulan
adresleri ve pencereyi (`[başlangıç, bitiş]`, iki gün de dahil) alıyor.
Sırayla denetleyip `"outside the window"`, `"excluded"`, `"out of scope"`
ya da `"in scope"` döndürsün. Başlangıç kodunda bir denetim eksik.

**Beklenen çıktı:**

```
in scope
excluded
out of scope
```
