`same_twice` Dropout'lu bir modele aynı girdiyi iki kez verip çıktıların aynı
olup olmadığına bakıyor; ikinci karşılaştırmanın değerlendirme kipinde yapılması
gerekiyor ama model hâlâ eğitim kipinde. Düzelt: `[False, True]` basmalı.

**Beklenen çıktı:**

```
[False, True]
```
