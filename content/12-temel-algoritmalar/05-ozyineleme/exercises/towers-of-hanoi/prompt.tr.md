Üç çubuk var: `"A"`, `"B"`, `"C"`. `"A"`'da büyükten küçüğe dizilmiş `n`
disk duruyor. Hepsini `"C"`'ye taşıyacaksın; her hamlede **tek disk**
taşınır ve **büyük disk küçüğün üstüne konamaz**.

Özyinelemeli çözüm üç adım:

1. Üstteki `n − 1` diski yedek çubuğa taşı (hedefi yardımcı olarak kullan).
2. En büyük diski hedefe taşı.
3. Yedekteki `n − 1` diski hedefe, en büyüğün üstüne taşı.

`hanoi(n, source, target, spare)` fonksiyonunu yaz: hamleleri `(nereden,
nereye)` demetlerinin listesi olarak döndürsün. `n == 0` ise boş liste.

**Beklenen çıktı:**

```
A -> C
A -> B
C -> B
A -> C
B -> A
B -> C
A -> C
1023
```

10 disk 1023 hamle: `2ⁿ − 1`, üstel büyüme.
