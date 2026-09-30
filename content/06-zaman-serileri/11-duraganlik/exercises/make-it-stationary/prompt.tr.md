Yolcu serisini adım adım dönüştür ve her adımda iki testin ne dediğine
bak.

**Yapman gerekenler:**

1. Dört seri hazırla ve bir sözlükte topla (anahtarlar bu sırayla):
   - `"level"`: `p`
   - `"diff"`: `p.diff()`
   - `"diff12"`: `p.diff(12)`
   - `"log diff12"`: `np.log(p).diff(12)`
2. Her biri için (`dropna()` sonrası) ADF ve KPSS p-değerlerini hesapla ve
   `ad adf_p kpss_p` biçiminde, p-değerleri üç ondalıkla, alt alta yazdır.
3. Son serinin (`"log diff12"`) kaç satır kaybettiğini ve standart sapmasını
   (üç ondalık) aynı satıra yazdır.
4. Bir adım daha atıp gereksiz bir fark al: `np.log(p).diff(12).diff()`.
   Standart sapmasını üç ondalığa yuvarlayıp yazdır.

**Beklenen çıktı:**

```
level 1.0 0.01
diff 0.537 0.1
diff12 0.982 0.01
log diff12 0.0 0.1
12 0.023
0.033
```

Düzeyde ve `diff12`'de iki test de "durağan değil" diyor. Düz farkta testler
çelişiyor: mevsim ve büyüyen varyans hâlâ orada. Logaritma + `diff(12)` ile
ikisi de "durağan" diyor. Üstüne bir fark daha almak standart sapmayı
**yükseltiyor**: gereken en az farkta dur.
