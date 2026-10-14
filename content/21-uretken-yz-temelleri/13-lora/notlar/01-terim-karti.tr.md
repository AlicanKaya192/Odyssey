| Terim | Anlamı |
|---|---|
| **LoRA** (düşük ranklı uyarlama) | Donuk ağırlığın yanına iki ince matrisin çarpımını ekleyip yalnızca onları eğitmek |
| **Rank** | Bir matrisin bağımsız yön sayısı |
| **Tekil değerler** | Bir matrisin yönlerinin büyüklükleri; kareleri "enerji" payını verir |
| **Adaptör** | Bir görev için eğitilen küçük ek parametreler (A, B, gerekiyorsa çıkış katmanı) |
| **Dondurmak** | Ağırlığı eğitimde güncellememek |
| **Birleştirmek** (merge) | W + AB'yi tek matrise çevirip ek hesap maliyetini kaldırmak |
| **r** | LoRA'nın rankı; parametre sayısı r × (d_giriş + d_çıkış) |

**Akılda tut:**

- B sıfırdan başlar: eğitim ön eğitimli modelin tam kendisinden başlar.
- Bölümde tam ince ayarın değişiminin ilk 8 yönü %99,6'sını taşıdı; r = 4
  LoRA 714 parametreyle %94, tam ince ayar 2410 parametreyle %93 verdi
  (üç tohumda aynı düzey).
- Ön eğitimli model değişmez; adaptör takılıp çıkarılır.
