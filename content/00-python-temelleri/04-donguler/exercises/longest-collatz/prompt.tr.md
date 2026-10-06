Bir sayıyla başla ve şu kuralı uygula:

- Sayı **çiftse** ikiye böl.
- Sayı **tekse** üçle çarpıp bir ekle.

Sayı `1` olana kadar tekrarla. Örneğin `6`: 6 → 3 → 10 → 5 → 16 → 8 → 4 →
2 → 1. Bu yolculuk **8 adım** sürdü. Hangi sayıyla başlarsan başla hep
1'e varılıyor gibi görünüyor (buna Collatz sanısı denir; kimse hâlâ
kanıtlayamadı).

`1` ile `30` arasındaki (30 dahil) başlangıç sayılarından **hangisinin
yolculuğu en uzun**? Başlangıcı `best_start`, adım sayısını `best_steps`
değişkenine koy:

```
Longest: 27 with 111 steps
```

İki döngü iç içe:

- Dıştaki `for` döngüsü 1'den 30'a kadar her başlangıç sayısını deniyor.
- İçteki `while` döngüsü o sayının yolculuğunu yürütüp adımları sayıyor.
  Kaç kez döneceği önceden belli değil; `while` tam bunun için.

> Dikkat: İç döngüde başlangıç sayısını değiştirme; bir kopyasıyla
> (`n = start`) çalış. Yoksa dış döngü hangi sayıda olduğunu kaybeder.
> Adım sayacını da her yeni başlangıçta sıfırla.
