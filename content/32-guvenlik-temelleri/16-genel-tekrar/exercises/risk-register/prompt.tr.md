Tehdit Modelleme ve Risk Değerlendirme bölümlerini birleştir. Her tehdit
`id`, `stride`, `likelihood` (1–5) ve `impact` (1–5) alanlı.

`risk_register(threats)` her tehdit için `[id, stride, puan, duzey]`
listesi döndürsün. Puan = olasılık × etki; düzey 1–4 `"low"`, 5–9
`"medium"`, 10–16 `"high"`, 17–25 `"critical"`. Sıra: puan büyükten
küçüğe, eşitlikte `id` abece sırasında.

**Beklenen çıktı:**

```
T0 E 20 critical
T1 S 20 critical
T3 D 9 medium
T2 I 8 medium
T4 R 2 low
```
