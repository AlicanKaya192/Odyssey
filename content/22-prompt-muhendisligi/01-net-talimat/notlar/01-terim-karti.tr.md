| Terim | Anlamı |
|---|---|
| **Belirsiz talimat** | Uzunluğu, içeriği ya da biçimi modele bırakan talimat |
| **Net talimat** | Ne kadar, ne içersin, ne içermesin, kime, hangi biçimde sorularını cevaplayan talimat |
| **Ölçülebilir kural** | Kodla denetlenebilen kural: kelime sayısı, cümle sayısı, geçmesi gereken kelime |
| **Denetleyici** (checker) | Cevabın kurallara uyup uymadığını söyleyen fonksiyon |
| **Ayraç** (delimiter) | Veriyi talimattan ayıran işaret: `<review>` etiketleri, üç tırnak |
| **Kaçırma** (escaping) | Verideki özel işaretleri (`<`, `>`, `&`) zararsız biçime çevirmek |
| **Prompt injection** | Verinin içine gizlenmiş talimatla modelin davranışını değiştirme saldırısı |

**Akılda tut:**

- Net talimatın faydası yalnızca modele yol göstermek değil; programa
  **neyi reddedeceğini** de söyler. Derste dört örnek yanıtın biri bütün
  kuralları geçti, üçü en az bir kuralda kaldı.
- Prompt metnini ve denetleyiciyi aynı kural sözlüğünden üret.
- Saf sarmalayıcıda veri kapanış etiketini yazınca etiket sayısı 2 oldu;
  kaçıran sarmalayıcıda 1.
- Kaçırmada önce `&` işlenir; yoksa `&lt;` gibi kaçışlar bozulur.
