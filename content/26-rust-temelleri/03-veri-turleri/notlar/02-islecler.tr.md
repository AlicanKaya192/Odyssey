## Sık kullanılan sayı metotları

| Metot | Örnek | Sonuç |
|---|---|---|
| `abs` | `(-5_i32).abs()` | 5 |
| `pow` | `2_i32.pow(10)` | 1024 |
| `min` / `max` | `3.min(9)` | 3 |
| `sqrt` | `9.0_f64.sqrt()` | 3.0 |
| `round` | `2.5_f64.round()` | 3.0 |
| `floor` / `ceil` | `2.5_f64.floor()` | 2.0 |

Metot çağırırken sayının türünü belirtmen gerekebilir: `9.0.sqrt()` derlenmez, çünkü derleyici `f32` mü `f64` mü bilemez. Bu yüzden `9.0_f64` yazılır.

Aritmetik, karşılaştırma ve mantık işleçleri bir sonraki bölümde.
