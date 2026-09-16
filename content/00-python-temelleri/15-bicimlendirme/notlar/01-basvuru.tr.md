Biçim belirtecinin tamamı şu sırayla yazılıyor; parçaların hepsi isteğe
bağlı:

```
{değer:[doldurma][hizalama][işaret][genişlik][,][.basamak][tür]}
```

## Sık kullanılanlar

| Yazım | Sonuç | Ne işe yarar |
|---|---|---|
| `f"{3.14159:.2f}"` | `3.14` | İki ondalık basamak |
| `f"{12.5:.2f}"` | `12.50` | Eksik basamak sıfırla tamamlanır |
| `f"{1234567:,}"` | `1,234,567` | Binlik ayırıcı |
| `f"{1234567.891:,.2f}"` | `1,234,567.89` | Ayırıcı ve basamak birlikte |
| `f"{0.0725:.1%}"` | `7.2%` | Yüzde (yüzle çarpar) |
| `f"{7:03d}"` | `007` | Sıfırla doldurma |
| `f"{4.2:+.1f}"` | `+4.2` | Artı işaretini göster |
| `f"{'ada':<8}"` | `ada␣␣␣␣␣` | Sola yasla, sekiz karakter |
| `f"{'ada':>8}"` | `␣␣␣␣␣ada` | Sağa yasla |
| `f"{'ada':^8}"` | `␣␣ada␣␣␣` | Ortala |
| `f"{'ada':.^8}"` | `..ada...` | Noktayla doldurarak ortala |
| `f"{255:x}"` | `ff` | On altılık tabanda |
| `f"{255:b}"` | `11111111` | İkilik tabanda |
| `f"{12345.6789:.2e}"` | `1.23e+04` | Bilimsel gösterim |
| `f"{count = }"` | `count = 7` | Hata ayıklarken ad ve değer |

Tablodaki `␣` boşluk demek; gerçek çıktıda orada boşluk var.

## Türler

<figure class="fig anat">
  <div class="anat-row"><span><code>f</code></span><span>Ondalık sayı. Basamak sayısı verilmezse altı basamak.</span></div>
  <div class="anat-row"><span><code>d</code></span><span>Tam sayı. Ondalıklı bir değerle kullanılamaz.</span></div>
  <div class="anat-row"><span><code>%</code></span><span>Yüzde: yüzle çarpar, sonuna işaret koyar.</span></div>
  <div class="anat-row"><span><code>e</code></span><span>Bilimsel gösterim.</span></div>
  <div class="anat-row"><span><code>s</code></span><span>Metin. Varsayılan olduğu için genellikle yazılmıyor.</span></div>
</figure>

## Genişliği değişkenden almak

Sütun genişliği kodun içinde sabit olmak zorunda değil:

```python
width = 12
for name in ["Kalem", "Defter"]:
    print(f"{name:<{width}}|")
```

```
Kalem       |
Defter      |
```

İç içe süslü parantez, genişliği çalışma anında hesaplamana izin veriyor.
En uzun adı bulup ona göre hizalamak bu yolla oluyor.

## Sık yapılan üç hata

1. **Sıra karıştırmak.** `{x:.2f,}` çalışmıyor; ayırıcı basamaktan önce
   gelir: `{x:,.2f}`.
2. **`d` ile ondalık sayı.** `f"{12.5:d}"` hata veriyor; ondalıklı değer
   için `f` kullanılır ya da değer `int()` ile çevrilir.
3. **Yüzdeyi iki kez uygulamak.** `{rate * 100:.1%}` yüzde yediyi yedi yüz
   yapıyor. `%` çarpmayı zaten yapıyor.
